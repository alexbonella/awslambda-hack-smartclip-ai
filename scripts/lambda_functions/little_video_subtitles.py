import boto3
import json
import os
import time


s3 = boto3.client('s3', region_name='us-east-1')
transcribe = boto3.client('transcribe')
mediaconvert_client = boto3.client('mediaconvert', region_name='us-east-1')
media_conv_role = os.environ['MEDIA_CONV_ROLE']

def check_transcription_status(job_name):
    while True:
        response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        status = response['TranscriptionJob']['TranscriptionJobStatus']
        if status in ['COMPLETED', 'FAILED']:
            break
        print(f"Job status: {status}")
        time.sleep(5)

    if status == 'COMPLETED':
        print("Transcription job completed successfully.")
        return response
    else:
        print("Transcription job failed.")
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
    s3_source_key = f"video-output{event['output_file'].split('video-output')[1]}"
    
    job_name = s3_source_key.split('.')[0].split('/')[-1]
    input_file = event['output_file']
    output_file = f's3://{bucket}/video-output/{job_name}/{job_name}_subtitles'
    subtitles = F"s3://{bucket}/subtitles/{job_name}/{job_name}.srt"
    
    transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': input_file},
            MediaFormat='mp4',
            IdentifyLanguage=True,
            LanguageOptions=['en-US', 'es-ES', 'fr-FR'],
            OutputBucketName=bucket,
            OutputKey=f'subtitles/{job_name}/',
            Subtitles={ 
              "Formats": [ "srt" ],
              "OutputStartIndex": 1
            }
        )
    
    time.sleep(30) 
    transcription_response = check_transcription_status(job_name)

    print(f'TRANSCRIBE RUN SUCCESFULLY. {transcription_response}')
    
    # Define the job settings for MediaConvert
    job_settings = {
            'Inputs': [
            {
                'FileInput': input_file,
                'VideoSelector': {},
                'AudioSelectors': {
                    'Audio Selector 1': {
                        'DefaultSelection': 'DEFAULT'
                    }
                },
                'CaptionSelectors': {
                    'Caption Selector 1': {
                        'SourceSettings': {
                            'SourceType': 'SRT',
                            'FileSourceSettings': {
                                'SourceFile': subtitles
                            }
                        }
                    },
                }
            }
            ],
            'OutputGroups': [
                {
                    'Name': 'File Group',
                    'Outputs': [
                        {
                            'ContainerSettings': {
                                'Container': 'MP4'
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
                            ],
                            'CaptionDescriptions': [
                                {
                                    'CaptionSelectorName': 'Caption Selector 1',
                                    'DestinationSettings': {
                                        'DestinationType': 'BURN_IN',
                                        'BurninDestinationSettings': {
                                            'FontSize': 24,
                                            'OutlineColor': 'BLACK',
                                            'ShadowColor': 'NONE',
                                            'TeletextSpacing': 'FIXED_GRID',
                                            'FontColor': 'WHITE',
                                            'FontOpacity': 255,
                                            'OutlineSize': 2
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
        "status": "created"
        
    }

    return metadata_file
