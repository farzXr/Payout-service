FROM hashicorp/vault:1.21

RUN apk update && \
    apk add --no-cache make && \
    apk add --no-cache openssl ca-certificates && \
    mkdir -p /deploy/vault/logs/vault.log