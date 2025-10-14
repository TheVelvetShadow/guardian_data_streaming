#### Project Vars #####

variable "project_name" {
  description = "Guardian API"
  type        = string
  default     = "guardian-streaming"
}


##### SQS Vars #####

variable "sqs_retention_seconds" {
  description = "SQS message retention period in seconds (3 days as per brief)"
  type        = number
  default     = 259200 # 3 days (72 hours * 3600 seconds)

  validation {
    condition     = var.sqs_retention_seconds >= 60 && var.sqs_retention_seconds <= 1209600
    error_message = "SQS retention must be between 60 seconds and 1209600 seconds (14 days)."
  }
}

variable "sqs_queue_name" {
  description = "Name of the SQS queue - prefixed with project name"
  type        = string
  default     = "guardian-articles-queue"
}




##### Lambda Vars #####

#  lambda_timeout (number) - Function timeout in seconds (default 300)
variable "lambda_timeout" {
  description = "Lambda function timeout in seconds"
  type        = number
  default     = 300
}

#  lambda_memory (number) - Memory allocation in MB (default 512)
variable "lambda_memory" {
  description = "Lambda function memory in MB"
  type        = number
  default     = 512
}

#  lambda_runtime (string) - Python version "python3.9"
variable "lambda_runtime" {
  description = "Python runtime version for Lambda functions"
  type        = string
  default     = "python3.9"
}



##### API Variables #####

variable "guardian_api_key" {
  description = "The Guardian API key"
  type        = string
  sensitive   = true
}

# api_rate_limit - Max requests per day (500)
variable "guardian_api_rate_limit" {
  description = "Guardian API daily call limit"
  type        = number
  default     = 500
}


##### Cloudwatch ######
# SQS messaging logs

variable "sqs_message_age_threshold" {
  description = "Maximum age (seconds) for messages in queue before alarm"
  type        = number
  default     = 600
}

variable "sqs_queue_depth_threshold" {
  description = "Maximum number of messages in queue before alarm"
  type        = number
  default     = 100
}

# SNS error log email
variable "sns_subscription_email" {
  description = "email address for SNS subscription"
  type        = string
  sensitive   = true
}

