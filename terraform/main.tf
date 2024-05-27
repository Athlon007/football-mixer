provider "azurerm" {
  features {}
}

data "azurerm_resource_group" "existing_rg" {
  name = "PDP_Showcase"
}

# Create an App Service Plan
resource "azurerm_app_service_plan" "app_service_plan" {
  name                = "flask-app-service-plan"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku {
    tier = "Free"
    size = "F1"
  }
}
