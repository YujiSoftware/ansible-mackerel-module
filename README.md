# ansible-mackerel-module

Ansible plugin for operating Mackerel.

## Install

Copy [`mackerel_host.py`](https://raw.githubusercontent.com/YujiSoftware/ansible-mackerel-module/master/library/mackerel_host.py) under the library folder of the playbook.

```
playbook/
 ├─ inventories/
 ├─ roles/
 ├─ library/
 │  └─ mackerel_host.py (Here!)
 └─ main.yml
```

Or, copy [`mackerel_host.py`](https://raw.githubusercontent.com/YujiSoftware/ansible-mackerel-module/master/library/mackerel_host.py) to these locations:

* ~/.ansible/plugins/modules/
* /usr/share/ansible/plugins/modules/

## Parameters

|Parameter|Choices/Defaults|Comments|
|---|---|---|
|status|**Choices:** <br/>・standby<br/>・working<br/>・maintenance<br/>・poweroff|Changes the host status to the specified value.|
|role_fullnames||The full names of roles are in this character string format: `<service name>:<role name>`.|
|host||Specify the target host ID. <br/>If not specified, use the value set in `/var/lib/mackerel-agent/id`.|
|apikey||Tthe API key of the organization to which targeted hosts and services belong.<br/>If not specified, use the value set  `mackerel-agent.conf`.|
|conf|`/etc/mackerel-agent/mackerel-agent.conf`|Specify the mackerel-agent configuration file path.<br/>|
|root|`/var/lib/mackerel-agent`|Specify the root directory of mackerel-agent.|

## Examples

### Set the Mackerel host status to standby while ansible is running and restore it when finished.

```yaml
- name: Set Mackerel Host Status
  mackerel_host:
    status: standby

# - Changing host settings -

- name: Set Mackerel Host Status
  mackerel_host:
    status: working
```

### Set Mackerel host role

```yaml
- name: Set Mackerel Host Role Fullnames
  mackerel_host:
    role_fullnames:
      - test_project:web
```

### Get Mackerel host configuration and branch processing

```yaml
- name: Get Mackerel host configuration
  mackerel_host:
  register: mackerel

- name: Copy file if roles has "service"
  copy:
    src: ../files/example.conf
    dest: /etc/httpd/conf.d/
  when: mackerel['host']['roles']['service'] is defined
```

## Return Values

See: https://mackerel.io/api-docs/entry/hosts#get  

### Sample
```yaml
{
    "changed": false,
    "failed": false,
    "host": {
        "createdAt": 1575716151,
        "displayName": null,
        "id": "3MZTJf2ARsq",
        "interfaces": [
            {
                "ipAddress": "10.0.2.15",
                "ipv4Addresses": [
                    "10.0.2.15"
                ],
                "ipv6Address": "fe80::5054:ff:fe47:4652",
                "ipv6Addresses": [
                    "fe80::5054:ff:fe47:4652"
                ],
                "macAddress": "52:54:00:47:46:52",
                "name": "eth0"
            }
        ],
        "isRetired": false,
        "memo": "",
        "meta": {
            "agent-name": "mackerel-agent/0.65.0 (Revision 4278ab6)",
            "agent-revision": "4278ab6",
            "agent-version": "0.65.0",
            "block_device": {
                "dm-0": {
                    "removable": "0",
                    "size": "78577664"
                },
                "dm-1": {
                    "removable": "0",
                    "size": "3145728"
                },
                "sda": {
                    "model": "VBOX HARDDISK",
                    "removable": "0",
                    "rev": "1.0",
                    "size": "83886080",
                    "state": "running",
                    "timeout": "30",
                    "vendor": "ATA"
                }
            },
            "cpu": [
                {
                    "cache_size": "8192 KB",
                    "core_id": "0",
                    "cores": "1",
                    "family": "6",
                    "mhz": "2673.296",
                    "model": "26",
                    "model_name": "Intel(R) Core(TM) i7 CPU         920  @ 2.67GHz",
                    "physical_id": "0",
                    "stepping": "4",
                    "vendor_id": "GenuineIntel"
                }
            ],
            "filesystem": {
                "/dev/mapper/VolGroup00-LogVol00": {
                    "kb_available": 38129256,
                    "kb_size": 39269648,
                    "kb_used": 1140392,
                    "mount": "/",
                    "percent_used": "3%"
                },
                "/dev/sda2": {
                    "kb_available": 971872,
                    "kb_size": 1038336,
                    "kb_used": 66464,
                    "mount": "/boot",
                    "percent_used": "7%"
                },
                "devtmpfs": {
                    "kb_available": 241480,
                    "kb_size": 241480,
                    "kb_used": 0,
                    "mount": "/dev",
                    "percent_used": "0%"
                },
                "tmpfs": {
                    "kb_available": 50040,
                    "kb_size": 50040,
                    "kb_used": 0,
                    "mount": "/run/user/1000",
                    "percent_used": "0%"
                }
            },
            "kernel": {
                "machine": "x86_64",
                "name": "Linux",
                "os": "GNU/Linux",
                "platform_name": "CentOS",
                "platform_version": "7.3.1611",
                "release": "3.10.0-514.26.2.el7.x86_64",
                "version": "#1 SMP Tue Jul 4 15:04:05 UTC 2017"
            },
            "memory": {
                "active": "108484kB",
                "anon_pages": "53940kB",
                "bounce": "0kB",
                "buffers": "76kB",
                "cached": "217192kB",
                "commit_limit": "1823052kB",
                "committed_as": "622088kB",
                "dirty": "0kB",
                "free": "83212kB",
                "inactive": "162716kB",
                "mapped": "28228kB",
                "nfs_unstable": "0kB",
                "page_tables": "4500kB",
                "slab": "112188kB",
                "slab_reclaimable": "85420kB",
                "slab_unreclaim": "26768kB",
                "swap_cached": "0kB",
                "swap_free": "1572860kB",
                "swap_total": "1572860kB",
                "total": "500384kB",
                "vmalloc_chunk": "34359731200kB",
                "vmalloc_total": "34359738367kB",
                "vmalloc_used": "4764kB",
                "writeback": "0kB"
            }
        },
        "name": "web_server",
        "roles": {
            "test": [
                "web"
            ]
        },
        "status": "working",
        "type": "agent"
    }
}
```