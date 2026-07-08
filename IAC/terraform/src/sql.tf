resource "azurerm_mssql_server" "sql_server" {
  name                = var.sql_server_name
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  version             = "12.0"

  administrator_login          = var.sql_admin_username
  administrator_login_password = var.sql_admin_password

  minimum_tls_version = "1.2"

  tags = var.tags
}

resource "azurerm_mssql_database" "sql_db" {
  name      = var.sql_database_name
  server_id = azurerm_mssql_server.sql_server.id

  sku_name    = "Basic" # This gives 5 DTU automatically
  max_size_gb = 2       # Basic tier supports up to 2GB

  zone_redundant = false

  tags = var.tags
}

# Allow the Web App (and other Azure services) to reach the SQL server
# resource "azurerm_mssql_firewall_rule" "allow_azure_services" {
#   name             = "AllowAzureServices"
#   server_id        = azurerm_mssql_server.sql_server.id
#   start_ip_address = "0.0.0.0"
#   end_ip_address   = "0.0.0.0"
# }