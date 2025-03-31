# 🚀 Blog Generator App using AWS Bedrock

## 🌟 Project Overview
The **Blog Generator App** utilizes AWS services to dynamically create and store blogs. It leverages:
- 🟢 **API Gateway**: Receives POST requests with a blog topic.
- 🟢 **Lambda Function**: Generates a blog based on the topic using AWS Bedrock.
- 🟢 **Amazon S3**: Stores the generated blog in a .txt file.

## 🌐 API Endpoint
**Base URL:**
`https://2rt5d39.execute-api.us-east-2.amazonaws.com/dev/blog-generation`

## 📝 Testing with Postman
Send a POST request with the following payload:
```json
{
    "blog_topic": "Machine Learning And Generative AI"
}
```
✅ **Expected Response:**
```json
{
    "message": "Blog successfully generated and stored in S3",
    "s3_path": "s3://your-bucket-name/generated-blogs/Machine_Learning_And_Generative_AI.txt"
}
```

## ⚙️ What It Does
- Receives blog topic via API request
- Generates content using AWS Bedrock
- Saves the blog in a .txt file in S3

---
👨‍💻 **Shubham Murtadak (AI Engineer)**

