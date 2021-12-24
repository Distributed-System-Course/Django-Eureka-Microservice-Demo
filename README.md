# Python Django Eureka Microservice

This repo tries demostrating the process of registering django services into a Eureka server, with the help of [Python Eureka Client][py-eureka-client].

## Steps

### Get Eureka server running

First of all, a running Eureka server is needed. 

One can try getting a Eureka server running on somemachine following this guide: [Spring Boot - Eureka Server](https://www.tutorialspoint.com/spring_boot/spring_boot_eureka_server.htm). 

Basically you can initialize a Spring Boot Project with Eureka server dependency on [Spring Initializer Homepage](https://start.spring.io/). After that, you may need to make some configurations in `src/main/resources/application.properties`.

Then you can build and run this Spring Boot project. And you should be able to visit the Eureka server (for example `localhost:8761`) if success.

### Start a Django Project

Then you should have a ruuning Django site, which should be able to handle some HTTP requests.

Request from other machines should be able to access this Django site. That means if you are using Django's development server, you should add your host name to `ALLOWED_HOSTS` in `settings.py`, and run server with command like:

```console
$ python3 manage.py runserver 0.0.0.0:8000
```

Assume that the machine which the server is running at has an IP address of `10.151.102.74`. Also notice that our server is listening on port `8000`.

In this demo, the **root url** is mapped to a function which returns the string `'Hello!'`. You can check this in [services/urls.py](./services/urls.py) and [services/views.py](./services/views.py).

### Register to Eureka Server

Assume the server can access Eureka server at `http://10.151.102.74:8761`, then we can register our server to Eureka using [Python Eureka Client][py-eureka-client] with following command.

```python
import py_eureka_client.eureka_client as eureka_client

eureka_client.init(
    # Where the Eureka server is:
    eureka_server="http://10.151.102.74:8761",
    app_name="MyApplication",
    instance_host="10.151.102.74",
    instance_port=8000,
)
```

Argument `app_name` is used to identify a app on Eureka server, which means we can refer to this server (or simmilar server instances, if any) by this name. In this demo, the name is `MyApplication`.

It is necessary to assign `instance_host` as the IP address by which other machines can find this server. Otherwise, the program would find any available IP address of the current machine among all the network adapters to which it has connected to.

Needless to say, we should also assign `instance_port` as the port number which our server is listening on.

You should say a new instance named `MYAPPLICATION` on Eureka if success.

To automatically register the server to Eureka, one can put the code into [manage.py](./manage.py) like the demo did. Be sure to run it before `main` function in [manage.py](./manage.py). You can also refer to commit `610965db` in this repository.

[py-eureka-client]: https://github.com/keijack/python-eureka-client/

### Call Services

Until now we have successfully publish our server to Eureka server. We should be able to access the server by `app_name`.

First, we need to init Eureka client. Say, we can open a Python REPL:

```python
>>> import py_eureka_client.eureka_client as eureka_client
>>> eureka_client.init(eureka_server="http://localhost:8761/", app_name="User", instance_host='10.151.102.74')
<py_eureka_client.eureka_client.EurekaClient object at 0x0000017C16A93310>
>>> eureka_client.do_service('MyApplication', '')
'Hello!'
```

Notice that after initializing Eureka client, we are able to call `do_service` method. And we successfully recevied the returned string `'Hello!'`.

By the way, for now you should see an new instance named `USER` on Eureka, since we register current client with the `app_name` of `User`.

## Where to step further

For more information, one can check [Python Eureka Client][py-eureka-client].

