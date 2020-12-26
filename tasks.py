from logging import Logger

from invoke import task, Collection
import yaml

FAKE_API_KEY = 'd41d8cd98f00b204e9800998ecf8427e'
FAKE_API_PORT = 3000
FAKE_API_HOST = 'localhost'


def lambdas():
    return 'create_s3_bucket', 'upload_to_s3_bucket', 'list_s3_bucket'


def log(severity, message):
    Logger(name='__name__').__getattribute__(severity)(message)


def sls_config(key):
    with open('serverless.yml', 'r') as config:
        file = config.read()
        return yaml.safe_load(file).get(key)


@task
def install_dependencies(c):
    """Install necessary serverless plugins."""
    plugins = sls_config('plugins')

    def install_sls_plugin(plugin):
        log("warning", f">> Install dependencies: {plugin}")
        c.run(f"sls plugin install --name {plugin}")

    list(map(lambda p: install_sls_plugin(p), plugins))


@task(pre=[install_dependencies])
def deploy(c):
    """>> Deploy serverless application."""
    c.run('sls deploy')


@task
def remove(c):
    """>> Remove serverless application."""
    c.run('sls remove')


@task
def info(c):
    """>> Serverless application status info. Including endpoints and api token."""
    c.run(f"sls info")


@task
def offline(c):
    """>> Run serverless application in offline mode."""
    c.run(f"docker-compose -f docker-compose-build.yml exec -T poc pipenv run sls offline --host 0.0.0.0 --printOutput")


@task
def autopep8(c):
    """>> Run autocorrection on python files."""
    log('warning', ">> Autocorrect python files according to styleguide")
    c.run("autopep8 --in-place --max-line-length 200 --aggressive *.py --verbose")

    for wd in lambdas():
        with c.cd(wd):
            log('info', f">> Change working directory to {wd}")
            log('info', ">> Autocorrect python files according to styleguide")
            c.run("autopep8 --in-place --recursive . --max-line-length 200 --aggressive --verbose")


@task
def build_build_docker_compose(c):
    print(">> Build docker-compose")
    c.run('docker-compose -f docker-compose-build.yml build')


@task
def run_build_docker_compose(c):
    print(">> Build docker-compose")
    c.run('docker-compose -f docker-compose-build.yml up -d')


@task
def stop_build_docker_compose(c):
    print(">> Kill docker-compose")
    c.run('docker-compose -f docker-compose-build.yml kill -s SIGKILL')


@task
def rm_build_docker_compose(c):
    print(">> Remove docker-compose")
    c.run('docker-compose -f docker-compose-build.yml rm -f')


@task
def remove_build_container(c):
    stop_build_docker_compose(c)
    rm_build_docker_compose(c)


@task(pre=[build_build_docker_compose, run_build_docker_compose])
def restart_build_container(c):
    """
    >> Build and run build container
    """


ns = Collection()
local = Collection('local')
serverless = Collection('serverless')

local.add_task(autopep8, 'autopep8')
serverless.add_task(deploy, 'deploy')
serverless.add_task(remove, 'remove')
serverless.add_task(info, 'info')
serverless.add_task(offline, 'offline')

serverless.add_task(restart_build_container, 'rebuild_container')
serverless.add_task(remove_build_container, 'stop_container')
ns.add_collection(local)
ns.add_collection(serverless)
