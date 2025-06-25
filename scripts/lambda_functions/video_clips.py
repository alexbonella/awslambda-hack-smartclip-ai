import json
import time
import pandas as pd
from utils_video import *
import boto3
import os
import re


s3 = boto3.client('s3')
mediaconvert_client = boto3.client('mediaconvert', region_name='us-east-1')
media_conv_role = os.environ['MEDIA_CONV_ROLE']

def read_json_from_s3(bucket_name, file_key):
    try:
        
        response = s3.get_object(Bucket=bucket_name, Key=file_key)

        content = response['Body'].read().decode('utf-8')

        json_content = json.loads(content)

        return json_content
    
    except Exception as e:
        print(f"Error reading the file: {e}")
        return None
        
def check_media_convert_status(job_id):
    while True:
        response = mediaconvert_client.get_job(Id=job_id)
        status = response['Job']['Status']
        print(f"Job status: {status}")

        if status == 'COMPLETE':
            print("MediaConvert job completed successfully.")
            return response
        elif status == 'ERROR':
            print("MediaConvert job failed.")
            return None

        time.sleep(5)

def lambda_handler(event, context):
    
    bucket = event['bucket_destiny']
    job_name = event['job_name']
    input_file = f"s3://{event['bucket_origin']}/video-input/{event['job_name']}.mp4"
    output_file = f's3://{bucket}/video-output/{job_name}/{job_name}_little'
    file_key = event['transcribe_path']
    object_key = event['bedrock_phrases']

    json_content = read_json_from_s3(bucket, file_key)
    json_content = json.dumps(json_content, indent=4)
    data = json.loads(json_content) 

    items = data['results']['items']

    df = get_items(items)
    df = df[df['type'] != 'punctuation']
    if df is not None:
        df = df.reset_index(drop=True)
    else:
        print("The DataFrame is None. Please check the data source.")

    tmp_file_path = f'/tmp/{job_name}.txt'
    s3.download_file(bucket, object_key, tmp_file_path)

    phrases = []
    with open(tmp_file_path, 'r') as file:
        for line in file:
            clean_text = clean_line(line)
            if clean_text.strip():
               phrases.append(clean_text.strip())

    df_phrases_f = get_slot_times(phrases,df)

    if df_phrases_f.empty:
        match_phrases = "No coincidences, please retry the Bedrock answer step"
        clips = "Null"
        metadata_file =  {
            
          "bucket_origin": event['bucket_origin'],
          "bucket_destiny": bucket,
          "video_uploaded": f"video-input/{event['job_name']}.mp4",
          "subtiltes_path": f"subtitles/{event['job_name']}/{event['job_name']}.srt",
          "transcribe_path": f"subtitles/{event['job_name']}/{event['job_name']}.json",
          "match_status":match_phrases,
          "clips_finded":clips,
          "status": "retry bedrock answer"
        
        }
   
    else:
        match_phrases = 'SUCCESS'

        clips = get_clips(df_phrases_f)

        job_settings = {
            'Inputs': [
                {
                    'TimecodeSource': 'ZEROBASED',
                    'VideoSelector': {},
                    'AudioSelectors': {
                        'Audio Selector 1': {
                            'DefaultSelection': 'DEFAULT'
                        }
                    },
                    'FileInput': input_file,
                    'InputClippings': clips
                }
            ],
            'OutputGroups': [
                {
                    'Name': 'File Group',
                    'Outputs': [
                        {
                            'ContainerSettings': {
                                'Container': 'MP4',
                            },
                            'VideoDescription': {
                                'CodecSettings': {
                                    'Codec': 'H_264',
                                    'H264Settings': {
                                        'MaxBitrate': 5000000,
                                        'RateControlMode': 'QVBR',
                                        'QualityTuningLevel': 'SINGLE_PASS',
                                        'QvbrSettings': {
                                            'QvbrQualityLevel': 8
                                        }
                                    }
                                },
                                'Width': 1920,
                                'Height': 1080
                            },
                            'AudioDescriptions': [
                                {
                                    'CodecSettings': {
                                        'Codec': 'AAC',
                                        'AacSettings': {
                                            'Bitrate': 96000,
                                            'CodingMode': 'CODING_MODE_2_0',
                                            'SampleRate': 48000
                                        }
                                    }
                                }
                            ]
                        }
                    ],
                    'OutputGroupSettings': {
                        'Type': 'FILE_GROUP_SETTINGS',
                        'FileGroupSettings': {
                            'Destination': output_file
                        }
                    }
                }
            ]
        }

        response_video_job = mediaconvert_client.create_job(
            Role=media_conv_role, 
            Settings=job_settings
        )

        time.sleep(30) 
        transcription_response_convert = check_media_convert_status(response_video_job['Job']['Id']) 
        print(f'TRANSCRIBE RUN SUCCESFULLY. {transcription_response_convert}')

        metadata_file = {
            
            "bucket_origin": event['bucket_origin'],
            "bucket_destiny":bucket,
            "job_name":job_name,
            "input_file":input_file,
            "output_file":f"{output_file}.mp4",
            "match_status":match_phrases,
            "clips_finded":clips,
            "status": "created"
            
        }

    return metadata_file
