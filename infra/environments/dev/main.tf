module "unity_catalog" {
  source = "../../modules/unity_catalog"

  catalog_name = "bank_acme"

  schemas = [
    "bronze",
    "silver",
    "gold",
    "ai"
  ]
}