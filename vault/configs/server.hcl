ui = true
disable_mlock = true
api_addr = "http://127.0.0.1:8200"
cluster_addr = "https://127.0.0.1:8201"

storage "raft" {
  path = "./data"
  node_id = "node1"
}

max_lease_ttl = "768h"      # 32 дня максимум для lease
default_lease_ttl = "768h"  # По умолчанию