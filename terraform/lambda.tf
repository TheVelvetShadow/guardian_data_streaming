#################### ZIP THE LAMBDA FUNCTIONS ##############################################

data "archive_file" "extract_lambda" {
  type        = "zip"
  source_file = "${path.module}/../src/extract.py"
  output_path = "${path.module}/../deploy/lambdas/extract_lambda.zip"
}

data "archive_file" "transform_lambda" {
  type        = "zip"
  source_file = "${path.module}/../src/transform.py"
  output_path = "${path.module}/../deploy/lambdas/transform_lambda.zip"
}

data "archive_file" "load_lambda" {
  type = "zip"
  source_file = "${path.module}/../src/load.py"
  output_path = "${path.module}/../deploy/lambdas/load_lambda.zip"
} 


#################### CREATE THE LAMBDA FUNCTIONS ########################################

# Extract_lambda (writes to Kinesis)



# Transform_lambda (reads from Kinesis, triggered by events)


# Load_lambda (destination for transformed data)



# Each lambda needs:
# filename (from archive_file)
# function_name (use variables)
# role (from iam.tf)  
# handler (extract.lambda_handler, transform.lambda_handler, load.lambda_handler)
# runtime = var.lambda_runtime
# timeout = var.lambda_timeout
# memory_size = var.lambda_memory
# environment variables 