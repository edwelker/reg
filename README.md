# uwsgi zookeeper announcer

Designed to announce Python services to Zookeeper.  Used with Twitter's Finagle stack.
This packages integrates with `uwsgi`. Make sure that you use `uwsgi` for you production. 

## Installation

#### Install the package

```sh
pip install django-lbos
```

#### Update ini file

Add the following options to the uwsgi `.ini` file:

```txt
[uwsgi]
...
ini = :my-app
logto = uwsgi.log

[my-app]
...
; these values are required
mule=register.py
env = VERSION=1.0.0
env = APP_NAME=/gws/my-app
; these values are optional
env = LBOS_URL=http://lbos.url
env = PORT=8081
env = CHECK_URL=/check
```

Here is a table which explains what all the options mean

|Parameter name|Description|Default value|Required|Value example|
|:-------------|:----------|:------------|:-------|:------------|
|logto|log filename|prints to the stdout|no|uwsgi.log|
|mule|separate worker which runs registration script|-|yes|register.py|
|env = VERSION|version of the application|-|yes|1.0.0, 1.2.3.beta|
|env = APP_NAME|path in ZooKeeper for your application|-|yes|app, /app, /bla/my-app|
|env = LBOS_URL|custom URL for LBOS|value from /etc/ncbi/lbosresolver file|no|http://lbos.url:8080|
|env = PORT|custom application port|8080|no|8080, 7042|
|env = CHECK_URL|relative URL for the health check|/|no|/check|

For more information please go to the [lbos help page](http://lbos.prod.be-md.ncbi.nlm.nih.gov:8080/lbos).

## Running a project

Run your project using your *.ini file, for example:

```sh
uwsgi uwsgi.ini
```

If everything is setup correctly, in `uwsgi` logs you should see:

```txt
...
spawned uWSGI master process (pid: 114701)
spawned uWSGI worker 1 (pid: 114702, cores: 1)
spawned uWSGI worker 2 (pid: 114703, cores: 1)
...
*** Stats server enabled on :8081 fd: 22 ***
spawned uWSGI mule 1 (pid: 114704)
...
registering with http://lbos.dev.be-md.ncbi.nlm.nih.gov:8080/lbos/json from process 114704
Congratulations! Your announcement for 10.50.25.100:8081 was successful!
...
```