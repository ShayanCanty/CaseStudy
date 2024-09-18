import boto3
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

# Initialize AWS S3 client
s3 = boto3.client('s3')

# Specify your S3 bucket and folder containing reports
BUCKET_NAME = 'your-bucket-name'
FOLDER_NAME = 'reports-folder/'


def list_files_in_s3(bucket_name, folder_name):
    """List all files in the S3 bucket folder."""
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)
    files = [content['Key'] for content in response.get('Contents', [])]
    return files


def download_file_from_s3(bucket_name, file_key, local_file_name):
    """Download a file from S3 bucket."""
    s3.download_file(bucket_name, file_key, local_file_name)


def read_file(file_path):
    """Read a text file."""
    with open(file_path, 'r') as file:
        return file.read()


def generate_recommendations(text, model_name='facebook/bart-large-cnn'):
    """Generate recommendations using a language model."""
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    summarization_pipeline = pipeline("summarization", model=model, tokenizer=tokenizer)

    # Summarize the report text to extract key points
    summary = summarization_pipeline(text, max_length=200, min_length=30, do_sample=False)[0]['summary_text']

    # Here, you can add specific prompt-tuning or strategy generation rules
    recommendation_prompt = f"Based on this report and previous reports: {summary}. What are the key strategic recommendations for the health insurance industry?"

    # Generate recommendation
    model_name = "gpt2"  # You can use other LLMs like GPT-3, or even fine-tuned models
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    input_ids = tokenizer.encode(recommendation_prompt, return_tensors="pt")

    # Generate a recommendation response
    outputs = model.generate(input_ids, max_length=150, num_return_sequences=1, do_sample=True)

    recommendation = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return recommendation


if __name__ == "__main__":
    # List and download files from S3
    files = list_files_in_s3(BUCKET_NAME, FOLDER_NAME)
    
    for file_key in files:
        local_file_name = file_key.split('/')[-1]  # Extract file name
        download_file_from_s3(BUCKET_NAME, file_key, local_file_name)

        # Read the report content
        report_content = read_file(local_file_name)

        # Generate recommendations based on the report
        recommendations = generate_recommendations(report_content)
        
        print(f"Recommendations for {local_file_name}:\n{recommendations}\n")
        
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b