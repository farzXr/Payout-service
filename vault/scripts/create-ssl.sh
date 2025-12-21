#!/bin/bash

openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout ./configs/tls/vault.key -out ./configs/tls/vault.crt \
  -subj "/CN=localhost" -days 365 -addext "subjectAltName=IP:127.0.0.1"

sudo mkdir -p /usr/local/share/ca-certificates/vault/

sudo cp ./configs/tls/vault.crt /usr/local/share/ca-certificates/vault/

sudo update-ca-certificates