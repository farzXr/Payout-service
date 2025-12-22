#!/usr/bin/env python3
import json
import yaml
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
ansible_root = os.path.dirname(current_dir)
vars_file = os.path.join(ansible_root, "group_vars", "all", "vars.yml")

try:
    with open(vars_file, 'r') as f:
        variables = yaml.safe_load(f) or {}
except FileNotFoundError:
    print(f"Warning: {vars_file} not found", file=sys.stderr)
    variables = {}

ip_server = variables.get('ip_server_1')

inventory = {
    "_meta": {
        "hostvars": {}
    },
    "all": {
        "children": ["bootstrap", "prod"]
    },
    "bootstrap": {
        "hosts": ["server1-bootstrap"],
        "vars": {
            "ansible_user": "root",
            "ansible_ssh_private_key_file": "files/root_id_rsa",
            "ansible_python_interpreter": "/usr/bin/python3.12"
        }
    },
    "prod": {
        "hosts": ["server1-prod"],
        "vars": {
            "ansible_user": "root", 
            "ansible_ssh_private_key_file": "files/root_id_rsa",
            "ansible_python_interpreter": "/usr/bin/python3.12"
        }
    }
}

inventory["_meta"]["hostvars"]["server1-bootstrap"] = {
    "ansible_host": ip_server
}
inventory["_meta"]["hostvars"]["server1-prod"] = {
    "ansible_host": ip_server
}

print(json.dumps(inventory))