path "secret/data/dev/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

path "secret/data/prod/*" {
  capabilities = ["read", "list"]
}

path "sys/*" {
  capabilities = ["deny"]
}