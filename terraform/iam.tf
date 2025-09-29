data "aws_iam_policy_document" "lambda_assume_role_policy" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

# Extract Lambda Role (gets Guardian articles, sends to SQS)
resource "aws_iam_role" "extract_lambda_role" {
  name                  = "${var.project_name}-extract-lambda-role"
  assume_role_policy    = data.aws_iam_policy_document.lambda_assume_role_policy.json
  # Terraform will automatically detach policies before deleting
  force_detach_policies = true

  tags = {
    Name        = "Extract Lambda Role"
    Project     = var.project_name
  }
}

# Transform Lambda Role (reads from SQS, transforms data)
resource "aws_iam_role" "transform_lambda_role" {
  name                  = "${var.project_name}-transform-lambda-role"
  assume_role_policy    = data.aws_iam_policy_document.lambda_assume_role_policy.json
  force_detach_policies = true

  tags = {
    Name        = "Transform Lambda Role"
    Project     = var.project_name
  }
}

# Load Lambda Role (loads processed data to destination)
resource "aws_iam_role" "load_lambda_role" {
  name                  = "${var.project_name}-load-lambda"
  assume_role_policy    = data.aws_iam_policy_document.lambda_assume_role_policy.json
  force_detach_policies = true

  tags = {
    Name        = "Load Lambda Role"
    Project     = var.project_name
  }
}