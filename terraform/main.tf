provider "aws" {
  region = "eu-west-2"
  default_tags {
    tags = {
      ProjectName  = "guardian_api"
      DeployedFrom = "Terraform"
      Repository   = "guardian_data_streaming"
    }
  }
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

## call account id 
data "aws_caller_identity" "current" {}

data "aws_region" "current" {}