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


#################### LAMBDA FUNCTIONS ########################################

# Extract_lambda (writes to SQS)
resource "aws_lambda_function" "guardian_lambda" {
  filename         = data.archive_file.extract_lambda.output_path
  function_name    = "${var.project_name}"
  role            = aws_iam_role.extract_lambda_role.arn
  handler         = "extract.lambda_handler"
  # Changes hash so Terraform detects and deploys code changes
  source_code_hash = data.archive_file.extract_lambda.output_base64sha256
  runtime         = var.lambda_runtime
  timeout         = var.lambda_timeout
  memory_size     = var.lambda_memory

  environment {
    variables = {
      SQS_QUEUE_URL    = aws_sqs_queue.guardian_articles_queue.url
      GUARDIAN_API_KEY = var.guardian_api_key
      AWS_REGION_NAME  = data.aws_region.current.name
    }
  }

  tags = {
    Name        = "Guardian API to SQS"
    Project     = var.project_name
  }

   depends_on = [
    aws_iam_role_policy_attachment.guardian_lambda_logging,
    aws_iam_role_policy_attachment.guardian_lambda_sqs_send
  ]

}

 # CloudWatch