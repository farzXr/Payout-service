#!/bin/bash
set -e

if [ ! -f /etc/gitlab-runner/config.toml ]; then
    echo "Creating default config.toml..."
     if [ -n "$REGISTRATION_TOKEN" ]; then
        echo "Registering runner..."
        gitlab-runner register \
          --url https://gitlab.com \
          --registration-token "$REGISTRATION_TOKEN" \
          --executor shell \
          --name "main-runner"
    else
      echo "WARNING: No registration variables found."
    fi
fi



exec "$@"
