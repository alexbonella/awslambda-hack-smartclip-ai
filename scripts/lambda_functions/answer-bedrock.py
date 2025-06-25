import boto3
import json
from botocore.exceptions import ClientError
import random


s3 = boto3.client('s3')
client = boto3.client("bedrock-runtime", region_name="us-east-1")

def read_json_from_s3(bucket_name, file_key):
    try:        
        response = s3.get_object(Bucket=bucket_name, Key=file_key)    
        content = response['Body'].read().decode('utf-8')
        json_content = json.loads(content)

        return json_content

    except Exception as e:
        print(f"Error reading the file: {e}")
        return None

def get_anthropic_answer(prompt):

    model_id = "anthropic.claude-3-haiku-20240307-v1:0"

    conversation = [
        {
            "role": "user",
            "content": [{"text": prompt}],
        }
    ]
    
    try:
        # Send the message to the model, using a basic inference configuration.
        response = client.converse(
            modelId="anthropic.claude-3-haiku-20240307-v1:0",
            messages=conversation,
            inferenceConfig={"maxTokens":4096,"temperature":0},
            additionalModelRequestFields={"top_k":250}
        )
 
        # Extract the response text.
        response_text = response["output"]["message"]["content"][0]["text"]

    
    except (ClientError, Exception) as e:
        response_text = f"ERROR: Can't invoke '{model_id}'. Reason: {e} and {ClientError}"
        
    
    return response_text


def get_bedrock_answer(prompt,temp):
    
    model_id = "amazon.titan-text-express-v1"

    native_request = {
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": 8192,
            "temperature": temp,
            "topP":0.85,
        },
    }

    request = json.dumps(native_request)
    
    try:

        response = client.invoke_model(modelId=model_id, body=request)# Decode the response body.
        model_response = json.loads(response["body"].read())
        response_text = model_response["results"][0]["outputText"]

    except (ClientError, Exception) as e:
        response_text = f"ERROR: Can't invoke '{model_id}'. Reason: {e}"
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")       

    return response_text


def lambda_handler(event, context):
    bucket = event['bucket_destiny']
    folder_destiny = 'subtitles'
    key = event['video_uploaded']
    job_name = key.split('.')[0].split('/')[-1]
    file_key = f'{folder_destiny}/{job_name}/{job_name}.json'
    
    # Read the JSON file
    json_content = read_json_from_s3(bucket, file_key)
    json_content = json.dumps(json_content, indent=4)
    data = json.loads(json_content) 
    transcript = data['results']['transcripts'][0]['transcript']
    audience_objectives = event['video_uploaded'].split('_audience-')[1].split('.mp4')[0]
    
    # Prompt Phrases 
    prompt = f"""You are an AI assistant specialized in summarizing and extracting key information. Identify the 8 most important phrases from the following transcript, considering "{audience_objectives}" as the audience objective.

    The phrases should:
    1. Strictly adhere to the exact wording of the transcript.
    2. Capture the essence of the talk, highlighting the most significant points, statements, or themes.
    3. Be clear, concise, and representative of the overall content.
    4. Each phrase must not exceed 250 characters.
    
    Present the selected phrases without adding or modifying any words. Here is the transcript:
    
    {transcript}
    """   
    choose_function = random.choice([get_bedrock_answer, get_anthropic_answer])
    temperature = random.choice([0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9])

    if choose_function == get_bedrock_answer:
        
        model_id = "amazon.titan-text-express-v1"
        phrases = get_bedrock_answer(prompt, temperature)
        file_content = phrases.encode('utf-8')  # Assuming response_text is a string
        s3.put_object(Body=file_content, Bucket=bucket, Key=f"bedrock_answer/{job_name}/{job_name}.txt")
        print(f'answer Titan phrases: \n\n {phrases}\n\n')
 
        prompt_hash = f"""You are an AI assistant specialized in generating social media hashtags. \n
                      Your task is to create a single hashtag that captures the essence of the following 5 important phrases extracted from an interview, considering {audience_objectives[4]} as the audience objective. \n
                      The hashtag should be clear, concise, and compelling. After the keyword "hashtag:", \n
                      please provide only 1 hashtag without any explanation. Here are the phrases:\n\n
                      {phrases}"""
                      
        hashtag = get_bedrock_answer(prompt_hash,temperature)
        file_content_h = hashtag.encode('utf-8')  
        s3.put_object(Body=file_content_h, Bucket=bucket, Key=f"bedrock_answer/{job_name}/{job_name}_hastag.txt")
        print(f'answer Titan hash: \n {hashtag}')
    else:
        
        model_id = "anthropic.claude-3-haiku-20240307-v1:0"
        phrases = get_anthropic_answer(prompt)
        file_content = phrases.encode('utf-8')
        s3.put_object(Body=file_content, Bucket=bucket, Key=f"bedrock_answer/{job_name}/{job_name}.txt")
        print(f'answer Anthropic phrases: \n\n {phrases}\n\n')
        
        
        prompt_hash = f"""You are an AI assistant specialized in generating social media hashtags. \n
                      Your task is to create a single hashtag that captures the essence of the following 5 important phrases extracted from an interview, considering {audience_objectives[4]} as the audience objective. \n
                      The hashtag should be clear, concise, and compelling. After the keyword "hashtag:", \n
                      please provide only 1 hashtag without any explanation. Here are the phrases:\n\n
                      {phrases}"""
        
        hashtag = get_anthropic_answer(prompt_hash)
        print(f'answer Anthropic hash: \n {hashtag}')
        file_content_h = hashtag.encode('utf-8')
        s3.put_object(Body=file_content_h, Bucket=bucket, Key=f"bedrock_answer/{job_name}/{job_name}_hastag.txt")
    

    metadata_file = {
        
        "bucket_origin": event['bucket_origin'],
        "bucket_destiny":bucket,
        "job_name":job_name,
        "subtiltes_path":f'subtitles/{job_name}/{job_name}.srt',
        "transcribe_path":f'subtitles/{job_name}/{job_name}.json',
        "bedrock_phrases":f"bedrock_answer/{job_name}/{job_name}.txt",
        "bedrock_hashtag":f"bedrock_answer/{job_name}/{job_name}_hashtag.txt",
        "bedrock_model":model_id,
        "status": "created"
        
    }

    # TODO implement
    return metadata_file
