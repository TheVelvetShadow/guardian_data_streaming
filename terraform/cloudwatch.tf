# To monitor:
# can i capture API calls as a threshold?


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
  
  # double check this pattern in cloudwatch
  pattern        = "Making Guardian API request"
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
  period              = 86400  # 24 hours
  statistic           = "Sum"
  threshold           = var.guardian_api_rate_limit
  alarm_description   = "Guardian API daily limit reached"
  alarm_actions       = [aws_sns_topic.lambda_alerts.arn]
  treat_missing_data  = "notBreaching"

  tags = {
    Project = "Guardian Data Streaming"
  }
}