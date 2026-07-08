#common variables
variable "tags" {
  type        = map(string)
  description = "Tags to be applied to all resources"
  default = {
    ManagedBy   = "Terraform"
    Application = "ArulSimpleWebApp"
  }
}

variable "location" {
  type        = string
  description = "Azure region for resources"
  default     = "South India"
}


variable "resource_group_name" {
  type        = string
  description = "Name of the Resource Group that contains all Web App resources"
}


#sql server
variable "sql_server_name" {
  type        = string
  description = "Name of the SQL server"
}

variable "sql_database_name" {
  type        = string
  description = "Name of the SQL database"
}

variable "sql_admin_username" {
  description = "Administrator username for SQL Server"
  type        = string
  default     = "xxxx"
}

variable "sql_admin_password" {
  description = "Administrator password for SQL Server"
  type        = string
  sensitive   = true
  default     = "xxxx"
}


#app service
variable "app_service_plan_name" {
  type        = string
  description = "Name of the App Service Plan"
}

variable "app_service_plan_sku" {
  type        = string
  description = "SKU for the App Service Plan"
  default     = "B1"
}

variable "web_app_name" {
  type        = string
  description = "Name of the Web App (must be globally unique)"
}

variable "python_version" {
  type        = string
  description = "Python runtime version for the Web App"
  default     = "3.11"
}


#key vault
variable "key_vault_name" {
  type        = string
  description = "Name of the Key Vault (must be globally unique, 3-24 chars)"
}


#creds
variable "tenant_id" {
  type    = string
  default = "XXXX"
}

variable "subscription_id" {
  type    = string
  default = "XXXX"
}

variable "client_id" {
  type    = string
  default = "XXXX"
}

variable "client_secret" {
  type    = string
  default = "XXXX"
}