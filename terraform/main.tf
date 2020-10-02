terraform {
    required_providers {
        aws = {
          source  = "hashicorp/aws"
          version = "~> 2.70"
        }
    }
    backend "s3" {
        bucket = "sensat_backend_challenge"
        key    = "state/terraform.tfstate"
        region = var.aws_region
    }
}

provider "aws" {
    region     = var.aws_region
    version = "~> 2.70"
    access_key = var.aws_access_key_id
    secret_key = var.aws_secret_access_key
}

resource "aws_instance" "example" {
  ami           = "ami-01d30e82c07w65a1a"
  instance_type = "t2.micro"
}