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
  default     = 259200  # 3 days (72 hours * 3600 seconds)
  
  validation {
    condition     = var.sqs_retention_seconds >= 60 && var.sqs_retention_seconds <= 1209600
    error_message = "SQS retention must be between 60 seconds (1 min) and 1209600 seconds (14 days)."
  }
}

variable "sqs_queue_name" {
  description = "Name of the SQS queue (will be prefixed with project name)"
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

# guardian_api_key (string, sensitive) - Guardian API key

variable "guardian_api_key" {
  description = "The Guardian API key"
  type        = string
  sensitive   = true
}

# api_rate_limit (number) - Max requests per day (50)
variable "guardian_api_rate_limit" {
  description = "Guardian API daily call limit"
  type        = number
  default     = 50
}


##### Cloudwatch ######

# log_retention_days (number) - CloudWatch log retention (14 days)
# enable_detailed_monitoring (bool) - Enable/disable detailed metrics