
resource "aws_sqs_queue" "guardian_articles_queue" {
  name                       = "${var.project_name}_articles"
  message_retention_seconds  = var.sqs_retention_seconds # 3 days (259200 seconds)
  visibility_timeout_seconds = var.lambda_timeout        # Match Lambda timeout
  max_message_size           = 262144                    # 256KB (max allowed)
  delay_seconds              = 0                         # No delay
  receive_wait_time_seconds  = 0                         # Short polling (can use 20 for long polling)

  tags = {
    Name      = "${var.project_name}_articles_queue"
    Project   = var.project_name
    Retention = "3_days"
  }
}

output "sqs_queue_url" {
  value       = aws_sqs_queue.guardian_articles_queue.url
  description = "URL of SQS queue for Guardian articles"
}

output "sqs_queue_arn" {
  value       = aws_sqs_queue.guardian_articles_queue.arn
  description = "ARN of SQS queue"
}

# CloudWatch