import boto3 
import json 


prompt="""
Acts as a poet and wirte a poem on Genrative ai 
"""

bedrock=boto3.client(service_name="bedrock-runtime")

payload={
    "prompt":"[INST]"+ prompt +"[/INST]",
    "max_tokens":512,
    "temperature":0.5,
    "top_p":0.9
}


body=json.dumps(payload)

model_id="mistral.mistral-small-2402-v1:0"

response=bedrock.invoke_model(
    body=body,
    modelId=model_id,
    accept="application/json",
    contentType="application/json"
)


response_body=json.loads(response.get("body").read())

print("response body is :",response_body)

response_text=response_body['outputs'][0]['text']

print("response text is :",response_text)

print("heelo word")