resource "databricks_catalog" "this" {
  name    = var.catalog_name
  comment = "Banco ACME - BankAssist AI-Ready Data Engineering POC"

  properties = {
    project = "bankassist"
    domain  = "collections"
  }

  lifecycle {
    ignore_changes = [
      storage_root
    ]
  }
}

resource "databricks_schema" "this" {
  for_each = var.schemas

  catalog_name = databricks_catalog.this.name
  name         = each.value
  comment      = "Banco ACME ${each.value} schema"
}