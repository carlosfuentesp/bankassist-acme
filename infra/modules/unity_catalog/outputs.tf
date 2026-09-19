output "catalog_name" {
  description = "Created Unity Catalog catalog"
  value       = databricks_catalog.this.name
}

output "schemas" {
  description = "Created schemas"
  value = {
    for key, schema in databricks_schema.this :
    key => schema.name
  }
}