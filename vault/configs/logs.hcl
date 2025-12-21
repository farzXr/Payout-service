log_file = "./logs/vault.log"
log_level = "info"
log_format = "json"

log_rotate_bytes = 104857600   # 100MB макс размер файла
log_rotate_duration = "24h"    # Ротация каждые 24 часа
log_rotate_max_files = 10      # Хранить последние 10 файлов