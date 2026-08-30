# AWS Terraform Infrastructure-as-Code Definition
# Deploys Agentic ERP Platform on AWS App Runner, ECS, and RDS PostgreSQL

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  default     = "us-east-1"
  description = "AWS deployment region"
}

variable "environment" {
  default     = "production"
  description = "Deployment environment name"
}

# 1. AWS VPC & Security Groups
resource "aws_vpc" "erp_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "Agentic-ERP-VPC"
    Environment = var.environment
  }
}

# 2. AWS ECR Repository for Docker Containers
resource "aws_ecr_repository" "api_repo" {
  name                 = "agentic-erp-api"
  image_tag_mutability = "MUTABLE"
}

resource "aws_ecr_repository" "web_repo" {
  name                 = "agentic-erp-web"
  image_tag_mutability = "MUTABLE"
}

# 3. AWS App Runner Service (FastAPI Backend)
resource "aws_apprunner_service" "backend_service" {
  service_name = "agentic-erp-backend-api"

  source_configuration {
    image_repository {
      image_identifier      = "${aws_ecr_repository.api_repo.repository_url}:latest"
      image_repository_type = "ECR"
      image_configuration {
        port = "8000"
      }
    }
    auto_deployments_enabled = true
  }

  tags = {
    Environment = var.environment
  }
}

# 4. Outputs
output "aws_ecr_api_url" {
  value       = aws_ecr_repository.api_repo.repository_url
  description = "AWS ECR Registry URL for Python API"
}

output "aws_app_runner_url" {
  value       = aws_apprunner_service.backend_service.service_url
  description = "AWS Live Production Backend URL"
}
