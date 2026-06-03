terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.116"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = "71406c77-43f9-4b7b-9a73-bd27ca9881cf"
}

# Istniejąca grupa zasobów i rejestr ACR (Terraform tylko je odczytuje)
data "azurerm_resource_group" "iot" {
  name = "iot-rg"
}

data "azurerm_container_registry" "acr" {
  name                = "iotcdv2026"
  resource_group_name = data.azurerm_resource_group.iot.name
}

# NOWY plan App Service tworzony przez Terraform
resource "azurerm_service_plan" "tf_plan" {
  name                = "iot-plan-tf"
  resource_group_name = data.azurerm_resource_group.iot.name
  location            = "polandcentral"
  os_type             = "Linux"
  sku_name            = "B1"
}

# NOWA aplikacja webowa tworzona przez Terraform, ciągnąca obraz z ACR
resource "azurerm_linux_web_app" "tf_app" {
  name                = "iot-maja-asia-tf"
  resource_group_name = data.azurerm_resource_group.iot.name
  location            = "polandcentral"
  service_plan_id     = azurerm_service_plan.tf_plan.id

  identity {
    type = "SystemAssigned"
  }

  site_config {
    container_registry_use_managed_identity = true
    application_stack {
      docker_image_name   = "iot-app:v1"
      docker_registry_url = "https://${data.azurerm_container_registry.acr.login_server}"
    }
  }

  app_settings = {
    "WEBSITES_PORT" = "80"
  }
}

# Nadanie nowej aplikacji prawa pobierania obrazów z ACR (bez hasła – Managed Identity)
resource "azurerm_role_assignment" "tf_acrpull" {
  scope                = data.azurerm_container_registry.acr.id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_linux_web_app.tf_app.identity[0].principal_id
}

# Adres nowej aplikacji – wyświetli się po wdrożeniu
output "adres_aplikacji_tf" {
  value = "https://${azurerm_linux_web_app.tf_app.default_hostname}"
}
