resource "aws_kinesis_stream" "test_stream" {
  name             = var.kinesis_stream_name
  shard_count      = var.kinesis_shard_count
  retention_period = var.kinesis_retention_hours
# metrics for Cloudwatch to monitor
  shard_level_metrics = [
    "IncomingBytes",
    "IncomingRecords", 
    "OutgoingBytes",
    "OutgoingRecords"
  ]
}