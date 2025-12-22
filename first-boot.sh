#!/bin/bash
    mkdir -p ./deploy/vault/logs && \
    touch ./deploy/vault/logs/vault.log && chmod 777 ./deploy/vault/logs/vault.log && \
    touch ./deploy/vault/logs/audit.log && chmod 777 ./deploy/vault/logs/audit.log && \
    mkdir -p ./deploy/vault/data && chmod 777 ./deploy/vault/data
    mkdir -p ./deploy/ansible/group_vars/all