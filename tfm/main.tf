provider "aws" {
  region = "us-east-2"
}

# S3 Module
module "s3" {
  source      = "./modules/s3"
  bucket_name = "casestudy-trigger-bucket"
  acl         = "private"
  tags = {
    Name        = "LambdaTriggerBucket"
    Environment = "Production"
  }
  
}

# Lambda Module
module "lambda" {
  source                = "./modules/lambda"
  function_name         = "casestudy_function"
  handler               = "index.handler"
  runtime               = "python3.9"
  environment_variables = {
    ENVIRONMENT = "production"
  }
  s3_bucket_arn = module.s3.bucket_id

  tags = {
    Name        = "MyLambdaFunction"
    Environment = "Production"
  }
}