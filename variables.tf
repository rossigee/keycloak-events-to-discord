variable "discord_url" {
  description = "Discord channel URL"
  type        = string
}

variable "additional_tags" {
  description = "Additional resource tags"
  type        = map(string)
  default     = {}
}
