telemetry {
  prometheus_retention_time = "30s"

  unauthenticated_metrics_access = true

  # Отключаем hostname в метриках (чтобы не менялось при перезапуске)
  disable_hostname = true

  # Фильтрация метрик для экономии памяти
  enable_high_cardinality_metrics = false  # Отключаем метрики с уникальными labels

}