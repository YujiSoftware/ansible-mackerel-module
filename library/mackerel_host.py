#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import re
import urllib2

from ansible.module_utils.basic import AnsibleModule

def get_host(host, api_key):
    url = "https://api.mackerelio.com/api/v0/hosts/%s" % host
    req = urllib2.Request(url)
    req.add_header("X-Api-Key", api_key)

    res = urllib2.urlopen(req)
    body = res.read()
    
    return json.loads(body)

def main():
    module = AnsibleModule(
        argument_spec=dict(
            host=dict(type='str'),
            status=dict(type='str', default=None, choices=['standby', 'working', 'maintenance', 'poweroff']),
            role_fullnames=dict(type='list', default=[]),
        )
    )
    args = module.params

    host = args.get('host')
    status = args.get('status')
    role_fullnames = args.get('role_fullnames')

    roles = {}
    for fullname in role_fullnames:
        key, value = fullname.split(':')
        if key in roles:
            roles[key].append(value)
        else:
            roles[key] = [value]

    if host is None:
        with open("/var/lib/mackerel-agent/id") as file:
            host = file.read()

    api_key_re = re.compile(r'apikey = "(\w+)"')
    with open("/etc/mackerel-agent/mackerel-agent.conf") as file:
        for line in file:
            match = api_key_re.match(line)
            if match:
                api_key = match.group(1)
                break
   
    try:
        data = get_host(host, api_key)
        changed = False

        if status is not None and data["host"]["status"] != status:
            url = "https://api.mackerelio.com/api/v0/hosts/%s/status" % host
            values = {'status' : status }
            req = urllib2.Request(url, json.dumps(values))
            req.add_header("X-Api-Key", api_key)
            req.add_header("Content-Type", "application/json")
            urllib2.urlopen(req)

            data["host"]["status"] = status
            changed = True
            
        if len(role_fullnames) > 0 and data["host"]["roles"] != roles:
            url = "https://api.mackerelio.com/api/v0/hosts/%s/role-fullnames" % host
            values = {'roleFullnames' : role_fullnames }
            req = urllib2.Request(url, json.dumps(values))
            req.get_method = lambda: 'PUT'
            req.add_header("X-Api-Key", api_key)
            req.add_header("Content-Type", "application/json")
            urllib2.urlopen(req)

            data["host"]["roles"] = roles
            changed = True
            
        module.exit_json(data=data, changed=changed)
    except urllib2.HTTPError as e:
        module.fail_json(msg="%s: %s (%s)" % (e.code, json.loads(e.read())["error"], url))

if __name__ == '__main__':
    main()
