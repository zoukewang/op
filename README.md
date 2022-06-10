## openstack资源操作脚本
### 使用方法
#### 配置openstack环境信息 config.py

```
user = 'admin'
passwd = 'aisware-nfvi'
tenant = 'admin'
domain = 'Default'
host = '10.21.70.12'
protocal = 'http'
proxy_id = ''
```
#### 执行脚本 python main.py

```
动作: d:删除 l:查询所有 g:指定ID查询 c:删除所有 ll:列出指定name（模糊匹配）的资源 dd：删除指定name（模糊匹配）的资源
资源: 0:vm   1:net   2:subnet    3:port    4:flavor   5:volume   6:volume_type    7:volume_qos-spec    8:server_group     9:image

例子: 查询所有VM : l 0
查询指定VM : g 0 62d77465-06b5-47ab-8430-8b49b1fa7a20
删除指定VM : d 0 62d77465-06b5-47ab-8430-8b49b1fa7a20
删除所有VM : c 0
查询指定VM ：ll 0 NFV
删除指定VM ：dd 0 NFV
```
