variable "kinesis_retention_hours" {
  description = "Kinesis data retention in hours"
  type        = number
  default     = 72  # 3 days as per brief
}

variable "lambda_timeout" {
  description = "Lambda function timeout in seconds"
  type        = number
  default     = 300
}

variable "lambda_memory" {
  description = "Lambda function memory in MB"
  type        = number
  default     = 512
}