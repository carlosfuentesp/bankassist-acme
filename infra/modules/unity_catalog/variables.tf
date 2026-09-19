variable "catalog_name" {
  description = "Name of the Unity Catalog catalog"
  type        = string
}

variable "schemas" {
  description = "Schemas to create inside the catalog"
  type        = set(string)
}