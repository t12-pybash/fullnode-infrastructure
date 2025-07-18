terraform {
  backend "s3" {
    bucket = "op-stack-terraform-state-1234567890"  # Replace with your bucket name
    key    = "infrastructure/terraform.tfstate"
    region = "us-west-2"
  }
}
