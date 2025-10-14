
##### Lambda Roles #####

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
resource "aws_iam_role" "guardian_lambda_role" {
  name               = "${var.project_name}-extract-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role_policy.json
  # Terraform will automatically detach policies before deleting
  force_detach_policies = true

  tags = {
    Name    = "Guardian Lambda Role"
    Project = var.project_name
  }
}


##### SQS Roles #####

data "aws_iam_policy_document" "lambda_sqs_send" {
  statement {
    effect = "Allow"

    actions = [
      "sqs:SendMessage",
      "sqs:GetQueueUrl"
    ]

    resources = [
      aws_sqs_queue.guardian_articles_queue.arn
    ]
  }
}

resource "aws_iam_policy" "lambda_sqs_send" {
  name   = "${var.project_name}-lambda-sqs-send"
  policy = data.aws_iam_policy_document.lambda_sqs_send.json
}

resource "aws_iam_role_policy_attachment" "guardian_lambda_sqs_send" {
  role       = aws_iam_role.guardian_lambda_role.name
  policy_arn = aws_iam_policy.lambda_sqs_send.arn
}

