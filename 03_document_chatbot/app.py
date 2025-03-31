import os 
import json 
import sys 
import boto3 
import streamlit as st 
import numpy as np 
from langchain_community.llms import Bedrock
from langchain_aws import BedrockEmbeddings
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA 


## Bedrock client 
bedrock=boto3.client(service_name="bedrock-runtime")

## Titan Embeddings Model to do embedding 
bedrock_embeddings=BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0",client=bedrock)


# Data Ingestion 
def data_ingestion():
    loader=PyPDFDirectoryLoader("data")
    documents=loader.load()

    #chunking by using Recursivecharactertextsplitter 
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=10000,chunk_overlap=500)

    docs=text_splitter.split_documents(documents)

    return docs 


## Vector Embeddings and vector store 

def get_vector_store(docs):

    #crete instance of faiss vectordb
    vectordb=FAISS.from_documents(
        docs,
        bedrock_embeddings
    )

    #save vectorestore to local disk
    vectordb.save_local("vectordb")


def get_llma3_llm():
    #create instance of llm model 
    llm=Bedrock(model_id="meta.llama3-70b-instruct-v1:0",
                client=bedrock,
                model_kwargs={"max_gen_len":512,"temperature":0.5,"top_p":0.9}
                )
    return llm 


prompt_template = """
You are an expert Answer Provider based on provided context.Use the following pieces of context to provide a 
concise answer to the question at the end but use atleast summarize with 
250 words with detailed explaantions. If you don't know the answer, 
just say that you don't know, don't try to make up an answer.
<context>
{context}
</context

Question: {question}

Assistant:"""


PROMPT=PromptTemplate(
    template=prompt_template,
    input_variables=['context','question']
)


def get_response_llm(llm,vectorstore_faiss,query):
    qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore_faiss.as_retriever(
        search_type="similarity", search_kwargs={"k": 3}
    ),
    return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT}
)
    answer=qa({"query":query})
    return answer['result']




def main():
    st.set_page_config('Chat with PDF :')

    st.header("Chat with pdfs 💁")

    question=st.text_input("Ask Question based on pdf file :")

    with st.sidebar:
        st.title("Update or create Vector Store :")

        # File uploader for PDF 
        uploaded_file=st.file_uploader("Upload a PDF ",type=['pdf'])

        if uploaded_file is not None:
            save_path=os.path.join("data",uploaded_file.name)

            with open(save_path,"wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.success(f"FILE UPLOADED successfully : {uploaded_file.name}")
        

        if st.button("Vectors Update"):
            with st.spinner("Processing ..."):
                docs=data_ingestion()
                get_vector_store(docs) 
                st.success("Done")
        
    
    if st.button("Generate Output"):
        with st.spinner("Processing ..."):
            faiss_index=FAISS.load_local("vectordb",bedrock_embeddings,allow_dangerous_deserialization=True)

            llm=get_llma3_llm()

            st.write(get_response_llm(llm,faiss_index,question))

            st.success("Done")

            

if __name__=="__main__":
    main()
