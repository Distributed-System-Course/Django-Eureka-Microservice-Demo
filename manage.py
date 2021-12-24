#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

import py_eureka_client.eureka_client as eureka_client

def eureka_init():
    # The flowing code will register your server to eureka server and also start to send heartbeat every 30 seconds
    # 将目前的服务器注册到 Eureka 服务器
    eureka_client.init(
        # Eureka Server 所在的地址
        eureka_server="http://10.151.102.74:8761",
        app_name="MyApplication",
        # instance_host 不填则自动取得当前机器在网络上的一个 IP 地址
        instance_host="10.151.102.74",
        instance_port=8000,
    )


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eurekatest.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    eureka_init()
    main()
