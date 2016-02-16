# uwsgi zookeeper announcer

Designed to announce Python services to Zookeeper.  Used with Twitter's Finagle stack.
This packages integrates with `uwsgi`. Make sure that you use `uwsgi` for your production.

## Installation

#### Install the package

```sh
pip install django-lbos
```

This command installs all required packages and puts the script for announcement `register.py` into `<path_to_venv>/bin` folder.
You'll have to provide path to it in your `uwsgi.ini` (see example below).

#### Update ini file

Add the following options to the uwsgi `.ini` file (see also `example_uwsgi.ini` in this repo):

```txt
[uwsgi]
...
ini = :my-app
logto = uwsgi.log

[my-app]
...
; these values are required
env = VERSION=1.0.0
env = APP_NAME=/gws/my-app
; these values are optional
env = LBOS_URL=http://lbos.url
env = PORT=8081
env = CHECK_URL=/check
virtualenv = <path_to_venv>
mule = %(virtualenv)/bin/register.py
```

Here is a table which explains what all the options mean

|Parameter name|Description|Default value|Required|Value example|
|:-------------|:----------|:------------|:-------|:------------|
|logto|log filename|prints to the stdout|no|uwsgi.log|
|env = VERSION|version of the application|-|yes|1.0.0, 1.2.3.beta|
|env = APP_NAME|path in ZooKeeper for your application|-|yes|app, /app, /bla/my-app|
|env = LBOS_URL|custom URL for LBOS|value from lbos resolver file file|no|http://lbos.url:8080|
|env = PORT|custom application port|8080|no|8080, 7042|
|env = CHECK_URL|relative URL for the health check|/|no|/check|
|mule|separate worker which runs registration script|-|yes|register.py|

For more information please see `python-lbos` README file.

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
Registering to http://lbos.url from process 114704
Congratulations! Your announcement for 15.18.12.11:8081 was successful!
...
```
