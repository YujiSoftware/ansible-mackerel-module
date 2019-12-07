#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import re

import ansible.module_utils.six.moves.urllib.error as urllib_error

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url

def fetch_mackerel(module, api_key, path, data={}, method="GET"):
    url = "https://api.mackerelio.com/api/v0/%s" % path
    headers = {
        'Content-type': 'application/json',
        "X-Api-Key": api_key,
    }
    resp, info = fetch_url(module, url, json.dumps(data), headers, method)
    if info["status"] != 200:
        raise urllib_error.HTTPError(url, info["status"], info["body"], headers, None)

    body = resp.read()
    
    return json.loads(body)

def main():
    module = AnsibleModule(
        argument_spec=dict(
            host=dict(type='str'),
            status=dict(type='str', default=None, choices=['standby', 'working', 'maintenance', 'poweroff']),
            role_fullnames=dict(type='list', default=[]),
            apikey=dict(type='str'),
            conf=dict(type='str', default='/etc/mackerel-agent/mackerel-agent.conf'),
            root=dict(type='str', default='/var/lib/mackerel-agent'),
        ),
        supports_check_mode=True,
    )
    args = module.params

    host = args.get('host')
    status = args.get('status')
    role_fullnames = args.get('role_fullnames')
    apikey = args.get('apikey')
    conf = args.get('conf')
    root = args.get('root')

    if host is None:
        with open("%s/id" % root) as file:
            host = file.read()

    if apikey is None:
        # TODO: Reading TOML in a better way
        apikey_re = re.compile(r'^\s*apikey\s*=\s*"(\w+)"$')
        with open(conf) as file:
            for line in file:
                match = apikey_re.match(line)
                if match:
                    apikey = match.group(1)
                    break
        if apikey is None:
            msg = "Could not read mackerel api key from '%s'" % conf
            module.fail_json(msg=msg)

    roles = {}
    for fullname in role_fullnames:
        key, value = fullname.split(':')
        if key in roles:
            roles[key].append(value)
        else:
            roles[key] = [value]

    data = fetch_mackerel(module, apikey, "hosts/%s" % host)
    changed = False

    if status is not None and data["host"]["status"] != status:
        url = "hosts/%s/status" % host
        values = {'status' : status }
        if not module.check_mode:
            fetch_mackerel(module, apikey, url, values, "POST")

        data["host"]["status"] = status
        changed = True

    if len(role_fullnames) > 0 and data["host"]["roles"] != roles:
        url = "hosts/%s/role-fullnames" % host
        values = {'roleFullnames' : role_fullnames }
        if not module.check_mode:
            fetch_mackerel(module, apikey, url, values, "PUT")

        data["host"]["roles"] = roles
        changed = True

    module.exit_json(host=data["host"], changed=changed)

if __name__ == '__main__':
    main()
