provider "aws" {
  region = "ap-south-1"
}

resource "aws_key_pair" "my-key" {
  key_name   = "my-key"
  public_key = file("~/.ssh/id_rsa.pub")
}

resource "aws_instance" "Nikhil-EC2-Instance" {
  ami           = "ami-0f8ca728008ff5af4"
  instance_type = "t2.micro"
  key_name      = "my-key"
  subnet_id     = aws_default_subnet.default.id
  vpc_security_group_ids = [
    aws_security_group.allow_ssh.id
  ]
  tags = {
    Name = "Nikhil's EC2 Instance"
  }
}

resource "aws_default_vpc" "default" {
  tags = {
    Name = "Default VPC"
  }
}

resource "aws_default_subnet" "default" {
  availability_zone = "ap-south-1a"
  tags = {
    Name = "Default subnet"
  }
}

locals {
  ports_in = [
    5000,
    80,
    22
  ]
  ports_out = [
    0
  ]
}

resource "aws_security_group" "allow_ssh" {
  name_prefix = "allow_ssh_"
  dynamic "ingress" {
    for_each = toset(local.ports_in)
    content {
      description = "HTTPS from VPC"
      from_port   = ingress.value
      to_port     = ingress.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }
  dynamic "egress" {
    for_each = toset(local.ports_out)
    content {
      from_port   = egress.value
      to_port     = egress.value
      protocol    = "-1"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }
}

output "ec2_global_ips" {
  value = ["${aws_instance.Nikhil-EC2-Instance.*.public_ip}"]
}
