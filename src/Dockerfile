FROM public.ecr.aws/lambda/python:3.8

# Install any necessary dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your Lambda function code
COPY app.py .

# Set the CMD to the handler function
CMD ["app.lambda_handler"]