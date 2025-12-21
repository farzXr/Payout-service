#!/bin/bash



VARS_FILE="./../ansible/group_vars/all/vars.yml"
SECRETS_FILE="./../ansible/group_vars/all/secrets.yml"

vault write auth/approle/role/gitlab-runner \
  token_ttl=1h \
  token_max_ttl=4h \
  policies="gitlab-runner" \
  secret_id_ttl=8760h

ROLE_ID=$(vault read -field=role_id auth/approle/role/gitlab-runner-role/role-id)
cat > "$VARS_FILE" << EOF
hashicorp-vault_role-id: "$ROLE_ID"
EOF

SECRET_ID=$(vault write -f -field=secret_id auth/approle/role/gitlab-runner-role/secret-id)
cat > "$SECRETS_FILE" << EOF
vault_secret_id: $ROLE_ID
EOF