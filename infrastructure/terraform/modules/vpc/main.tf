variable "name" { type = string }
variable "vpc_cidr" { type = string }
variable "availability_zones" { type = list(string) }
variable "project" { type = string }

locals {
  private_subnet_cidrs = [for index, _ in var.availability_zones : cidrsubnet(var.vpc_cidr, 4, index)]
  public_subnet_cidrs  = [for index, _ in var.availability_zones : cidrsubnet(var.vpc_cidr, 4, index + 8)]
}

resource "aws_internet_gateway" "this" {
  vpc_id = aws_vpc.this.id
  tags   = { Name = "${var.name}-igw" }
}

resource "aws_subnet" "public" {
  for_each                = toset(var.availability_zones)
  vpc_id                  = aws_vpc.this.id
  availability_zone       = each.value
  cidr_block              = local.public_subnet_cidrs[index(var.availability_zones, each.value)]
  map_public_ip_on_launch = false
  tags = {
    Name                     = "${var.name}-public-${each.value}"
    "kubernetes.io/role/elb" = "1"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.this.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.this.id
  }
  tags = { Name = "${var.name}-public" }
}

resource "aws_route_table_association" "public" {
  for_each       = aws_subnet.public
  subnet_id      = each.value.id
  route_table_id = aws_route_table.public.id
}

resource "aws_eip" "nat" {
  domain = "vpc"
}

resource "aws_nat_gateway" "this" {
  allocation_id = aws_eip.nat.id
  subnet_id     = values(aws_subnet.public)[0].id
  depends_on    = [aws_internet_gateway.this]
  tags          = { Name = "${var.name}-nat" }
}

resource "aws_vpc" "this" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true
  tags = {
    Name = var.name
  }
}

resource "aws_subnet" "private" {
  for_each                = toset(var.availability_zones)
  vpc_id                  = aws_vpc.this.id
  availability_zone       = each.value
  cidr_block              = local.private_subnet_cidrs[index(var.availability_zones, each.value)]
  map_public_ip_on_launch = false
  tags = {
    Name                                = "${var.name}-private-${each.value}"
    "kubernetes.io/role/internal-elb"   = "1"
    "kubernetes.io/cluster/${var.name}" = "shared"
  }
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.this.id
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.this.id
  }
  tags = { Name = "${var.name}-private" }
}

resource "aws_route_table_association" "private" {
  for_each       = aws_subnet.private
  subnet_id      = each.value.id
  route_table_id = aws_route_table.private.id
}

output "vpc_id" { value = aws_vpc.this.id }
output "private_subnet_ids" { value = [for subnet in aws_subnet.private : subnet.id] }
output "private_subnet_cidrs" { value = [for subnet in aws_subnet.private : subnet.cidr_block] }
