# coding:utf-8

import requests
import json
import config


def get_token():
    token_url = '{}://{}:5000/{}/v3/auth/tokens'.format(config.protocal, config.host, config.proxy_id)
    # token_url = '{}://{}:35357/{}/v3/auth/tokens'.format(config.protocal, config.host, config.proxy_id)
    # token_url = '{}://{}:31943/{}/v3/auth/tokens'.format(config.protocal, config.host, config.proxy_id)
    # token_url = 'https://[2409:8080:5a0a:6033::b]:5000/NFV-RP-HNGZ-00A-HW-01/v3/auth/tokens'
    auth_data = {
        "auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "domain": {
                            "name": config.domain
                        },
                        "name": config.user,
                        "password": config.passwd
                    }
                }
            },
            "scope": {
                "project": {
                    "name": config.tenant,
                    "domain": {
                        "name": config.domain
                    }
                }
            }
        }
    }

    print('begin alloc token, url={}, data={}'.format(token_url, auth_data))
    r = requests.post(token_url, json.dumps(auth_data), verify=False)
    print('alloc token ret_code={}, token={}'.format(r.status_code, r.headers['X-Subject-Token']))

    token = r.headers['X-Subject-Token']
    catalog = json.loads(r.content)['token']['catalog']
    return token, catalog


def get_endpoint(catalog, type):
    for item in catalog:
        if item['type'] == type:
            for endpoint in item['endpoints']:
                if endpoint['interface'] == 'public':
                    return endpoint['url']


def list(server_type, path, res_name):
    token, catalog = get_token()
    url = get_endpoint(catalog, server_type)
    headers = {
        "X-Auth-Token": token
    }
    r = requests.get('{}/{}'.format(url, path), headers=headers, verify=False)
    print('list {} ret_code={}'.format(res_name, r.status_code))
    res_list = []
    for item in json.loads(r.content)[res_name]:
        res = {
            "id": item["id"],
            "name": item["name"]
        }
        res_list.append(res)
    print('list {} ret={}'.format(res_name, json.dumps(res_list, indent=2)))


def get(id, server_type, path, res_name):
    token, catalog = get_token()
    url = get_endpoint(catalog, server_type)
    headers = {
        "X-Auth-Token": token
    }
    r = requests.get('{}/{}/{}'.format(url, path, id), headers=headers, verify=False)
    print('get {} ret_code={}'.format(res_name, r.status_code))
    res = json.loads(r.content)[res_name]
    print('get ret={}'.format(json.dumps(res, indent=2)))


def delete(id, server_type, path):
    token, catalog = get_token()
    url = get_endpoint(catalog, server_type)
    headers = {
        "X-Auth-Token": token
    }
    r = requests.delete('{}/{}/{}'.format(url, path, id), headers=headers, verify=False)
    print('del ret_code={}'.format(r.status_code))


def deleteall(server_type, path, res_name):
    token, catalog = get_token()
    url = get_endpoint(catalog, server_type)
    headers = {
        "X-Auth-Token": token
    }
    r = requests.get('{}/{}'.format(url, path), headers=headers, verify=False)
    print('list {} ret_code={}'.format(res_name, r.status_code))

    for item in json.loads(r.content)[res_name]:
        res = {
            "id": item["id"],
            "name": item["name"]
        }
        r = requests.delete('{}/{}/{}'.format(url, path, item["id"]), headers=headers, verify=False)
        print('del {} ret_code={}'.format(item["name"], r.status_code))


def list_name(server_type, path, res_name, name):
    token, catalog = get_token()
    url = get_endpoint(catalog, server_type)
    headers = {
        "X-Auth-Token": token
    }
    r = requests.get('{}/{}'.format(url, path), headers=headers, verify=False)
    print('list {} ret_code={}'.format(res_name, r.status_code))
    res_list = []
    for item in json.loads(r.content)[res_name]:
        res = {
            "id": item["id"],
            "name": item["name"]
        }
        if name in item["name"]:
            res_list.append(res)
    print('list {} ret={}'.format(res_name, json.dumps(res_list, indent=2)))


def delete_name(server_type, path, res_name, name):
    token, catalog = get_token()
    url = get_endpoint(catalog, server_type)
    headers = {
        "X-Auth-Token": token
    }
    r = requests.get('{}/{}'.format(url, path), headers=headers, verify=False)
    print('list {} ret_code={}'.format(res_name, r.status_code))

    for item in json.loads(r.content)[res_name]:
        if name in item["name"]:
            r = requests.delete('{}/{}/{}'.format(url, path, item["id"]), headers=headers, verify=False)
            print('del {} ret_code={}'.format(item["name"], r.status_code))


while True:
    prom = """
    动作: d:删除 l:查询所有 g:指定ID查询 c:删除所有 ll:列出指定name（模糊匹配）的资源 dd：删除指定name（模糊匹配）的资源
    资源: 0:vm   1:net   2:subnet    3:port    4:flavor   5:volume   6:volume_type    7:volume_qos-spec    8:server_group     9:image
    例子: 查询所有VM : l 0
          查询指定VM : g 0 62d77465-06b5-47ab-8430-8b49b1fa7a20
          删除指定VM : d 0 62d77465-06b5-47ab-8430-8b49b1fa7a20
          删除所有VM : c 0
          查询指定VM ：ll 0 NFV
          删除指定VM ：dd 0 NFV
    """
    # inputTmp = raw_input(prom)   raw_input（）函数存在于Python 2.x中。 它与Python 3.x的input（）函数相同。
    inputTmp = raw_input(prom)
    if inputTmp == 'q':
        break
    param = inputTmp.split(' ')
    print(param)
    count = len(param)

    if count != 2 and count != 3:
        print('参数长度错误!')
        continue
    if (param[0] == 'g' or param[0] == 'd') and count != 3:
        print('参数错误!')
        continue

    if param[1] == '0':
        if param[0] == 'l':
            list('compute', 'servers', 'servers')
        if param[0] == 'g':
            get(param[2], 'compute', 'servers', 'server')
        if param[0] == 'd':
            delete(param[2], 'compute', 'servers')
        if param[0] == 'c':
            deleteall('compute', 'servers', 'servers')
        if param[0] == 'll':
            list_name('compute', 'servers', 'servers', param[2])
        if param[0] == 'dd':
            delete_name('compute', 'servers', 'servers', param[2])

    if param[1] == '1':
        if param[0] == 'l':
            list('network', 'v2.0/networks', 'networks')
        if param[0] == 'g':
            get(param[2], 'network', 'v2.0/networks', 'network')
        if param[0] == 'd':
            delete(param[2], 'network', 'v2.0/networks')
        if param[0] == 'c':
            deleteall('network', 'v2.0/networks', 'networks')
        if param[0] == 'll':
            list_name('network', 'v2.0/networks', 'networks', param[2])
        if param[0] == 'dd':
            delete_name('network', 'v2.0/networks', 'networks', param[2])

    if param[1] == '2':
        if param[0] == 'l':
            list('network', 'v2.0/subnets', 'subnets')
        if param[0] == 'g':
            get(param[2], 'network', 'v2.0/subnets', 'subnet')
        if param[0] == 'd':
            delete(param[2], 'network', 'v2.0/subnets')
        if param[0] == 'c':
            deleteall('network', 'v2.0/subnets', 'subnets')
        if param[0] == 'll':
            list_name('network', 'v2.0/subnets', 'subnets', param[2])
        if param[0] == 'dd':
            delete_name('network', 'v2.0/subnets', 'subnets', param[2])

    if param[1] == '3':
        if param[0] == 'l':
            list('network', 'v2.0/ports', 'ports')
        if param[0] == 'g':
            get(param[2], 'network', 'v2.0/ports', 'port')
        if param[0] == 'd':
            delete(param[2], 'network', 'v2.0/ports')
        if param[0] == 'c':
            deleteall('network', 'v2.0/ports', 'ports')
        if param[0] == 'll':
            list_name('network', 'v2.0/ports', 'ports', param[2])
        if param[0] == 'dd':
            delete_name('network', 'v2.0/ports', 'ports', param[2])

    if param[1] == '4':
        if param[0] == 'l':
            list('compute', 'flavors', 'flavors')
        if param[0] == 'g':
            get(param[2], 'compute', 'flavors', 'flavor')
        if param[0] == 'd':
            delete(param[2], 'compute', 'flavors')
        if param[0] == 'c':
            deleteall('compute', 'flavors', 'flavors')
        if param[0] == 'll':
            list_name('compute', 'flavors', 'flavors', param[2])
        if param[0] == 'dd':
            delete_name('compute', 'flavors', 'flavors', param[2])

    if param[1] == '5':
        if param[0] == 'l':
            list('volumev2', 'volumes', 'volumes')
        if param[0] == 'g':
            get(param[2], 'volumev2', 'volumes', 'volume')
        if param[0] == 'd':
            delete(param[2], 'volumev2', 'volumes')
        if param[0] == 'c':
            deleteall('volumev2', 'volumes', 'volumes')
        if param[0] == 'll':
            list_name('volumev2', 'volumes', 'volumes', param[2])
        if param[0] == 'dd':
            delete_name('volumev2', 'volumes', 'volumes', param[2])

    if param[1] == '6':
        if param[0] == 'l':
            list('volumev2', 'types', 'volume_types')
        if param[0] == 'g':
            get(param[2], 'volumev2', 'types', 'volume_type')
        if param[0] == 'd':
            delete(param[2], 'volumev2', 'types')
        if param[0] == 'c':
            deleteall('volumev2', 'types', 'volume_types')
        if param[0] == 'll':
            list_name('volumev2', 'types', 'volume_types', param[2])
        if param[0] == 'dd':
            delete_name('volumev2', 'types', 'volume_types', param[2])

    if param[1] == '7':
        if param[0] == 'l':
            list('volumev2', 'qos-specs', 'qos_specs')
        if param[0] == 'g':
            get(param[2], 'volumev2', 'qos_specs', 'qos_specs')
        if param[0] == 'd':
            delete(param[2], 'volumev2', 'qos_specs')
        if param[0] == 'c':
            deleteall('volumev2', 'qos-specs', 'qos_specs')
        if param[0] == 'll':
            list_name('volumev2', 'qos-specs', 'qos_specs', param[2])
        if param[0] == 'dd':
            delete_name('volumev2', 'qos-specs', 'qos_specs', param[2])

    if param[1] == '8':
        if param[0] == 'l':
            list('compute', 'os-server-groups', 'server_groups')
        if param[0] == 'g':
            get(param[2], 'compute', 'os-server-groups', 'server_group')
        if param[0] == 'd':
            delete(param[2], 'compute', 'os-server-groups')
        if param[0] == 'c':
            deleteall('compute', 'os-server-groups', 'server_groups')
        if param[0] == 'll':
            list_name('compute', 'os-server-groups', 'server_groups', param[2])
        if param[0] == 'dd':
            delete_name('compute', 'os-server-groups', 'server_groups', param[2])

    if param[1] == '9':
        if param[0] == 'l':
            list('image', 'v2/images', 'images')
        if param[0] == 'g':
            get(param[2], 'image', 'v2/images', 'status')
        if param[0] == 'd':
            delete(param[2], 'image', 'v2/images')
        if param[0] == 'c':
            deleteall('image', 'v2/images', 'images')
        if param[0] == 'll':
            list_name('image', 'v2/images', 'images', param[2])
        if param[0] == 'dd':
            delete_name('image', 'v2/images', 'images', param[2])
