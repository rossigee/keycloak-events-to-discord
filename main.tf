module "lambda" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "2.23.0"

  function_name = "keycloak-events-to-discord"
  description   = "Sends Keycloak event notifications to Discord."
  handler       = "handler.lambda_handler"
  runtime       = "python3.9"
  timeout       = 15
  source_path   = "src"

  environment_variables = {
    "DISCORD_URL" = var.discord_url
  }

  allowed_triggers = {
    # "sns" = {
    #   principal  = "sns.amazonaws.com"
    #   source_arn = aws_sns_topic.sns-topic.arn
    # }
  }

  cloudwatch_logs_retention_in_days = 90

  publish = true

  tags = var.additional_tags
}
