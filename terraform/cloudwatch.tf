
##### Lambda #####

# filters for Lambda Error Alert Messages
resource "aws_cloudwatch_log_metric_filter" "lambda_errors" {
  name           = "guardian_lambda_errors"
  pattern        = "?ERROR ?Failed ?Exception"
  log_group_name = aws_cloudwatch_log_group.guardian_lambda_logs.name

  metric_transformation {
    name      = "LambdaErrors"
    namespace = "GuardianApp"
    value     = "1"
  }
}

# Alarm for Lambda Errors
resource "aws_cloudwatch_metric_alarm" "lambda_error_alarm" {
  alarm_name          = "guardian_lambda_errors"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = "LambdaErrors"
  namespace           = "GuardianApp"
  period              = 300
  statistic           = "Sum"
  threshold           = 1
  alarm_description   = "Alert when Lambda encounters errors"
  alarm_actions       = [aws_sns_topic.lambda_alerts.arn]

  tags = {
    Project = "Guardian Data Streaming"
  }
}

# SNS Topic for Alerts
resource "aws_sns_topic" "lambda_alerts" {
  name = "guardian-lambda-alerts"

  tags = {
    Project = "Guardian Data Streaming"
  }
}

resource "aws_sns_topic_subscription" "email_alert" {
  topic_arn = aws_sns_topic.lambda_alerts.arn
  protocol  = "email"
  endpoint  = var.sns_subscription_email
}


##### Guardian API Call Limit #####

# Log Metric Filter to count API calls
resource "aws_cloudwatch_log_metric_filter" "guardian_api_calls" {
  name           = "guardian_api_call_count"
  pattern        = "Making Guardian API call"
  log_group_name = aws_cloudwatch_log_group.guardian_lambda_logs.name

  metric_transformation {
    name      = "GuardianAPICallCount"
    namespace = "GuardianApp"
    value     = "1"
  }
}


# Alarm when limit API daily limit hit
resource "aws_cloudwatch_metric_alarm" "api_call_limit" {
  alarm_name          = "guardian_api_limit_reached"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = "GuardianAPICallCount"
  namespace           = "GuardianApp"
  period              = 86400 # 24 hours
  statistic           = "Sum"
  threshold           = var.guardian_api_rate_limit
  alarm_description   = "Guardian API daily limit reached"
  alarm_actions       = [aws_sns_topic.lambda_alerts.arn]
  treat_missing_data  = "notBreaching"

  tags = {
    Project = "Guardian Data Streaming"
  }
}


##### SQS Messaging logs #####

# Alarm: Messages stuck in queue too long
resource "aws_cloudwatch_metric_alarm" "sqs_message_age" {
  alarm_name          = "${var.project_name}_sqs_message_age"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "ApproximateAgeOfOldestMessage"
  namespace           = "AWS/SQS"
  period              = 300 # 5 minutes
  statistic           = "Maximum"
  threshold           = 600 # 10 minutes
  alarm_description   = "Alert when messages stuck in queue for >10 minutes"
  alarm_actions       = [aws_sns_topic.lambda_alerts.arn]

  dimensions = {
    QueueName = aws_sqs_queue.guardian_articles_queue.name
  }

  tags = {
    Project = var.project_name
  }
}

# Alarm: Queue has too many messages 
resource "aws_cloudwatch_metric_alarm" "sqs_queue_length" {
  alarm_name          = "${var.project_name}_sqs_queue_length"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "ApproximateNumberOfMessagesVisible"
  namespace           = "AWS/SQS"
  period              = 300
  statistic           = "Average"
  threshold           = 100
  alarm_description   = "Alert when queue has >100 messages waiting"
  alarm_actions       = [aws_sns_topic.lambda_alerts.arn]

  dimensions = {
    QueueName = aws_sqs_queue.guardian_articles_queue.name
  }

  tags = {
    Project = var.project_name
  }
}