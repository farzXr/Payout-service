#!/bin/sh

vault server \
  -config=./configs/server.hcl \
  -config=./configs/raft.hcl \
  -config=./configs/listener.hcl \
  -config=./configs/logs.hcl \
  -config=./configs/telemetry.hcl \ &

sleep 3

