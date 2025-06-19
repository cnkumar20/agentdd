#provider to read credentials from credential file
provider "aws" {
  shared_credentials_file = "~/.aws/credentials"
}
#local variable to store the region
locals {
  region = "us-east-1"
  vpc_name = "my-vpc"
  count = var.vpc_count
  flag = var.flag
}
#create count number of vpc and create only if flag is true
resource "aws_vpc" "my_vpc" {
  count = local.flag ? local.count : 0
  cidr_block = "10.0.${count.index}.0/24"
  enable_dns_support = true
  enable_dns_hostnames = true
  tags = {
    Name = "${local.vpc_name}-${count.index}"
  }
}


#create number of s3 buckets based on count variable
resource "aws_s3_bucket" "my_bucket" {
  count = local.flag ? local.count : 0
  bucket = "my-bucket-${count.index}"
  acl    = "private"

  tags = {
    Name = "my-bucket-${count.index}"
  }
}

#create security group for each vpc


resource "aws_security_group" "my_sg" {
  count = local.flag ? local.count : 0
  vpc_id = aws_vpc.my_vpc[count.index].id
  name   = "my-sg-${count.index}"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = [""]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [""]
  }
  tags = {
    Name = "my-sg-${count.index}"
  }
}
#create role and add to group "ssg" 
resource "aws_iam_role" "my_role" {
  count = local.flag ? local.count : 0
  name  = "my-role-${count.index}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      },
    ]
  })
}
#attach policy to role
resource "aws_iam_role_policy_attachment" "my_policy_attachment" {
  count = local.flag ? local.count : 0
  role       = aws_iam_role.my_role[count.index].name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}
# Create an IAM group and attach the role to it
resource "aws_iam_group" "my_group" {
  count = local.flag ? local.count : 0
  name  = "my-group-${count.index}"
}
resource "aws_iam_group_membership" "my_group_membership" {
  count = local.flag ? local.count : 0
  group = aws_iam_group.my_group[count.index].name
  users = [aws_iam_role.my_role[count.index].name]
}

# Create an IAM user and attach the group to it
resource "aws_iam_user" "my_user" {
  count = local.flag ? local.count : 0
  name  = "my-user-${count.index}"
}
resource "aws_iam_user_group_membership" "my_user_group_membership" {
  count = local.flag ? local.count : 0
  user  = aws_iam_user.my_user[count.index].name
  groups = [aws_iam_group.my_group[count.index].name]
}
# Create an IAM policy and attach it to the group
resource "aws_iam_policy" "my_policy" {
  count = local.flag ? local.count : 0
  name  = "my-policy-${count.index}"
  description = "My custom policy"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:ListBucket",
          "s3:GetObject",
          "s3:PutObject"
        ]
        Resource = "*"
      },
    ]
  })
}
resource "aws_iam_policy_attachment" "my_policy_attachment" {
  count = local.flag ? local.count : 0
  name       = "my-policy-attachment-${count.index}"
  policy_arn = aws_iam_policy.my_policy[count.index].arn
  groups     = [aws_iam_group.my_group[count.index].name]
}
# Create an IAM instance profile and attach the role to instance
resource "aws_iam_instance_profile" "my_instance_profile" {
  count = local.flag ? local.count : 0
  name  = "my-instance-profile-${count.index}"
  role  = aws_iam_role.my_role[count.index].name
}
# Create an EC2 instance in each VPC
resource "aws_instance" "my_instance" {
  count = local.flag ? local.count : 0
  ami           = "ami-0c55b159cbfafe1f0" # Replace with a valid AMI ID for your region
  instance_type = "t2.micro"
  vpc_security_group_ids = [aws_security_group.my_sg[count.index].id]
  subnet_id     = aws_vpc.my_vpc[count.index].default_subnet_id
  iam_instance_profile = aws_iam_instance_profile.my_instance_profile[count.index].name

  tags = {
    Name = "my-instance-${count.index}"
  }
}

