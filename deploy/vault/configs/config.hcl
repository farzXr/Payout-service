ui = true
disable_mlock = true
api_addr = "http://vault:8200"
cluster_addr = "https://vault:8201"

storage "raft" {
  path = "/deploy/vault/data"
  node_id = "node1"
}

/*retry_join {
  leader_api_addr = "https://vault2:8200"
}
retry_join {
  leader_api_addr = "https://vault3:8200"
}*/

max_lease_ttl = "768h"
default_lease_ttl = "768h"

listener "tcp" {
  address = "0.0.0.0:8200"
  tls_disable = true
}

log_file = "/deploy/vault/logs/vault.log"
log_level = "info"
log_format = "json"

log_rotate_bytes = 104857600   # 100MB макс размер файла
log_rotate_duration = "24h"    # Ротация каждые 24 часа
log_rotate_max_files = 10      # Хранить последние 10 файлов


telemetry {
  prometheus_retention_time = "30s"

  unauthenticated_metrics_access = true

  # Отключаем hostname в метриках (чтобы не менялось при перезапуске)
  disable_hostname = true

  # Фильтрация метрик для экономии памяти
  enable_high_cardinality_metrics = false  # Отключаем метрики с уникальными labels

}