import minicli
from usine import run, sudo, put, config, template, connect, exists


@minicli.cli
def addok(cmd):
    with sudo(user='geozone'):
        run(f'/srv/geozone/venv/bin/addok {cmd}')


@minicli.cli
def pip(command):
    """Run a pip command on the remote server.

    :command: the pip command to run.
    """
    with sudo(user='geozone'):
        run('/srv/geozone/venv/bin/pip {}'.format(command))


@minicli.cli
def system():
    run('apt update')
    run('apt install redis-server build-essential git nginx python3-dev '
        'wget tar software-properties-common gcc xz-utils python3-venv --yes')
    # run('add-apt-repository --yes --update ppa:jonathonf/python-3.6')
    # run('apt-get install --yes python3.6 python3.6-dev python3.6-venv')
    run('mkdir -p /etc/addok')
    run('mkdir -p /var/log/addok')
    run('useradd -N geozone -m -d /srv/geozone/ || exit 0')
    run('chown geozone:users /var/log/addok')
    run('chsh -s /bin/bash geozone')


@minicli.cli
def venv():
    """Setup the python virtualenv."""
    path = '/srv/geozone/venv/'
    if not exists(path):
        with sudo(user='geozone'):
            run(f'python3 -m venv {path}')
    pip('install pip -U')


@minicli.cli
def http():
    conf = template('remote/gunicorn.conf', workers=config.workers)
    with sudo():
        put(conf, '/srv/geozone/gunicorn.conf')
    nginx_conf = template('remote/nginx.conf', domain=config.domain)
    with sudo():
        put(nginx_conf, '/etc/nginx/sites-enabled/geozone')
    # On LXC containers, somaxconn cannot be changed. This must be done on the
    # host machine.
    run(f'sudo sysctl -w net.core.somaxconn={config.connections} || exit 0')
    restart()


@minicli.cli
def bootstrap():
    system()
    venv()
    settings()
    deploy()
    http()


@minicli.cli
def service():
    """Deploy/update the geozone systemd service."""
    put('remote/geozone.service', '/etc/systemd/system/geozone.service')
    systemctl('enable geozone.service')


@minicli.cli
def fetch():
    run(f'wget {config.data_uri} --output-document=/tmp/data.tar.xz --quiet')
    run('tar xf /tmp/data.tar.xz --directory /tmp')


@minicli.cli
def batch():
    run('redis-cli config set save ""')
    addok('batch /tmp/zones.msgpack')
    run('redis-cli save')


@minicli.cli
def reload():
    fetch()
    run('sudo systemctl stop geozone')
    addok('reset')
    batch()
    restart()


@minicli.cli
def deploy():
    pip('install addok addok-trigrams gunicorn --upgrade')
    pip('install git+https://github.com/addok/addok-geozones --upgrade')
    put('remote/addok.conf', '/etc/addok/addok.conf')
    restart()


@minicli.cli
def restart():
    run('sudo systemctl restart geozone nginx')


@minicli.cli
def systemctl(*args):
    """Run a systemctl command on the remote server.

    :command: the systemctl command to run.
    """
    run(f'systemctl {" ".join(args)}')


@minicli.cli
def logs(lines=50):
    """Display the geozone logs.

    :lines: number of lines to retrieve
    """
    run(f'journalctl --lines {lines} --unit geozone --follow')


@minicli.wrap
def wrapper(hostname, configpath):
    with connect(hostname=hostname, configpath=configpath):
        yield


if __name__ == '__main__':
    minicli.run(hostname='root@51.15.197.154', configpath='remote/config.yml')
