#################### ZIP THE LAMBDA FUNCTION ##############################################

data "archive_file" "extract_lambda" {
  type        = "zip"
  source_file = "${path.module}/../src/extract.py"
  output_path = "${path.module}/../deploy/lambdas/guardian_lambda.zip"
}


####### LAMBDA FUNCTION #######

# Guardian_lambda (calls API and sends articles to SQS)
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

##### CloudWatch #####

 data "aws_iam_policy_document" "cloudwatch_policy" {
  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = [
      "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/*:*"
    ]
  }
}

resource "aws_iam_policy" "cloudwatch_policy" {
  name   = "guardian_cloudwatch_policy"
  policy = data.aws_iam_policy_document.cloudwatch_policy.json
}

# Attach to Lambda Role
resource "aws_iam_policy_attachment" "guardian_lambda_cloudwatch_attach" {
  name       = "guardian_lambda_cloudwatch_attach"
  roles      = [aws_iam_role.guardian_lambda_iam_role.name]
  policy_arn = aws_iam_policy.cloudwatch_policy.arn
}