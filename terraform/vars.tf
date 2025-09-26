
##### Kinesis Vars #####

variable "kinesis_retention_hours" {
  description = "Kinesis data retention in hours"
  type        = number
  default     = 72  # 3 days as per brief
}

variable "kinesis_stream_name" {
  description = "Name of the Kinesis data stream"
  type        = string
  default     = "guardian-articles-stream"
}

# Stream performance/cost
variable "kinesis_shard_count" {
  description = "Number of shards for the Kinesis stream"
  type        = number
  default     = 1  # Single shard handles up to 1,000 records/sec or 1MB/sec
  
  # Limit to avoid too many shards being set
  validation {
    condition     = var.kinesis_shard_count >= 1 && var.kinesis_shard_count <= 3
    error_message = "Shard count must be between 1 and 3 for cost control."
  }
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


#  extract_lambda_name (string) - Name for extract function


#  transform_lambda_name (string) - Name for transform function


#  load_lambda_name (string) - Name for load function


##### IAM Vars #####





##### API Variables #####

# guardian_api_key (string, sensitive) - Guardian API key
# api_rate_limit (number) - Max requests per day (50)



##### Cloudwatch ######

# log_retention_days (number) - CloudWatch log retention (14 days)
# enable_detailed_monitoring (bool) - Enable/disable detailed metrics