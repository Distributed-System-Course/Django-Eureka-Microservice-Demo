# Python Django Eureka Microservice

这个存储库尝试在 [Python Eureka Client][py-eureka-client] 的帮助下, 演示将 Django 服务注册到 Eureka 服务器的过程。

## 步骤

### 让 Eureka 服务器运行

首先, 需要一个正在运行的 Eureka 服务器. 

可以按照 [Spring Boot - Eureka Server](https://www.tutorialspoint.com/spring_boot/spring_boot_eureka_server.htm), 尝试在某台机器上运行Eureka服务器. 

基本上, 您可以使用 [Spring Initializer Homepage](https://start.spring.io/) 来初始化一个具有 Eureka 服务器依赖的 Spring Boot 项目. 之后, 您可能需要在 `src/main/resources/application.properties` 中进行一些配置.

然后, 您可以构建并运行此 Spring Boot 项目. 如果成功, 您应该能够访问这个运行起来的 Eureka 服务器 (比如 [`localhost:8761`](http://localhost:8761)).

### 启动一个 Django 项目

然后你应该准备一个运行着的 Django 站点, 它应该能够处理一些 HTTP 请求. 

来自其他机器的请求应该能够访问这个 Django 站点.

> 如果您使用的是 Django 的开发服务器, 则应将主机名添加到 `settings.py` 中的 `ALLOWED_HOSTS` 中, 并使用以下命令运行服务器:

```console
$ python3 manage.py runserver 0.0.0.0:8000
```

下面, 假设运行服务器的计算机的 IP 地址为 `10.151.102.74`. 另外需要注意, 该服务器正在侦听 `8000` 端口.

在此演示中, **根** URL 映射到一个返回字符串 `'Hello!'` 的函数. 您可以在 [services/urls.py](./services/urls.py) 和 [services/views.py](./services/views.py) 中查看相关的代码.

### 注册到 Eureka 服务器

假设我们的服务器可以在 `http://10.151.102.74:8761` 访问到 Eureka 服务器. 

我们可以使用 [Python Eureka Client][py-eureka-client], 通过以下命令将我们的服务器注册到 Eureka.

```python
import py_eureka_client.eureka_client as eureka_client
eureka_client.init(
    # 其中 Eureka 服务器的地址是:
    eureka_server=“http://10.151.102.74:8761”, 
    app_name=“MyApplication”, 
    instance_host=“10.151.102.74”, 
    instance_port=8000, 
)
```

参数 `app_name` 用于在 Eureka 服务器上标识每个应用, 其他程序可以使用此名称引用此服务器(或相似的服务器实例, 如果有). 在此演示中, 用于注册的名称为 `MyApplication`.

需要将 `instance_host` 参数指定为其他计算机可以找到此服务器的 IP 地址. 否则, 程序将在当前计算机连接到的所有网络中找到可用的任何一个 IP 地址.

毋庸置疑, 我们还应该指定 `instance_port` 参数为服务器正在侦听的端口号。

如果成功, 您应该在 Eureka 上发现一个名为 `MYAPPLICATION` 的新实例.

要自动将服务器注册到 Eureka, 可以像该演示程序一样将代码放入 [manage.py](./manage.py). 请务必在 [manage.py](./manage.py) 中的 `main` 函数之前运行用于注册的代码. 也可以参考此存储库中编号 `610965db` 的提交.

[py-eureka-client]: https://github.com/keijack/python-eureka-client/

### 调用服务

到目前为止, 我们已经成功地将我们的服务器发布到 Eureka 服务器. 理论上, 将能够通过 `app_name` 访问该服务器. 

首先, 需要初始化 Eureka 客户端. 

比方说, 可以打开一个 Python REPL:

```python
>>> import py_eureka_client.eureka_client as eureka_client
>>> eureka_client.init(eureka_server="http://localhost:8761/",  app_name="User", instance_host='10.151.102.74')
<py_eureka_client.eureka_client.EurekaClient object at 0x0000017C16A93310>
>>> eureka_client.do_service('MyApplication',  '')
'Hello!'
```

在初始化 (init) Eureka 客户端后, 便可以调用 `do_service` 方法. 在该例中, 我们成功地接收了服务器返回的字符串 `'Hello!'`.

顺便, 现在您应该能在 Eureka 上看到一个名为 `USER` 的新实例, 因为我们使用了 `User` 这一 `app_name` 注册了当前客户端. 

## 在哪里更进一步

有关更多信息, 可以查看[Python Eureka Client][py-eureka-client].
