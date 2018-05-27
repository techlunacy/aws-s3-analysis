variable "public_key_path" {
  default = "~/.ssh/id_rsa.pub"
}

variable "key_name" {
  default = "aws-s3-analysis-key"
}

variable "tags" {
  type = "map"
  default = {
    Repo = "https://gitlab.com/techlunacy/aws-s3-analysis/"
    Terraform = true
  }
}
