import os
import base64
import boto3 
import json 


prompt="""
Generate an image of Boy celebrating his win after lots of struggles . He is standing on a mountain top, with a big smile on his face. The background is
"""

bedrock=boto3.client(service_name="bedrock-runtime")

text={'text':prompt}
config={"cfgScale":8,
        "seed":42,
        "quality":"standard",
        "width":1024,
        "height":1024,
        "numberOfImages":1
}

payload={
    "textToImageParams":text,
    "taskType":"TEXT_IMAGE",
    "imageGenerationConfig":config
}


body=json.dumps(payload)

model_id="amazon.titan-image-generator-v1"

response=bedrock.invoke_model(
    body=body,
    modelId=model_id,
    accept="application/json",
    contentType="application/json"
)


response_body=json.loads(response.get("body").read())

# print("response body is :",response_body)

# Save response body to a .txt file
output_dir = "output"
file_name_txt=f"{output_dir}/response_body.txt"
with open(file_name_txt, "w") as file:
    file.write(json.dumps(response_body, indent=4))  # Pretty print JSON


image = response_body.get("images")[0]
image_encoded = image.encode("utf-8")
image_bytes = base64.b64decode(image_encoded)

# Save image to a file in the output directory.
os.makedirs(output_dir, exist_ok=True)
file_name = f"{output_dir}/generated-img.png"
with open(file_name, "wb") as f:
    f.write(image_bytes)

print("image save to output directory successfully !")