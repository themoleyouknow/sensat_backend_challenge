// terraform/vars.tf
variable "aws_region" {
    type        = string
    description = "The region in which to deploy"
    default = "eu-west-2"
}
variable "aws_access_key_id" {
    type        = string
    description = "The name of the key"
}
variable "aws_secret_access_key" {
    type        = string
    description = "The key value"
}
variable "aws_zones" {
 type        = "list"
 description = "List of availability zones to use"
}