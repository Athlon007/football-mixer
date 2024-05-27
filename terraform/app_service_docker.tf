resource "azurerm_app_service" "app_service_docker" {
  name                = "flask-app-service-docker"
  location            = data.azurerm_resource_group.existing_rg.location
  resource_group_name = data.azurerm_resource_group.existing_rg.name
  app_service_plan_id = azurerm_app_service_plan.app_service_plan.id

  app_settings = {
    WEBSITES_ENABLE_APP_SERVICE_STORAGE = "false"
  }

  site_config {
    linux_fx_version = "DOCKER|${azurerm_container_registry.acr.login_server}/flaskapp:latest"
  }

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_role_assignment" "acr_pull" {
  principal_id           = azurerm_app_service.app_service_docker.identity[0].principal_id
  role_definition_name   = "AcrPull"
  scope                  = azurerm_container_registry.acr.id
}
