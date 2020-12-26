from logging import Logger

from invoke import task, Collection

FAKE_API_KEY = 'd41d8cd98f00b204e9800998ecf8427e'
IN_DOCKER = 'docker-compose -f docker-compose.yml exec -T poc pipenv run'


def lambdas():
    return 'create_s3_bucket', 'upload_to_s3_bucket', 'list_s3_bucket'


def log(severity, message):
    Logger(name='__name__').__getattribute__(severity)(message)


@task
def deploy(c):
    """>> Deploy serverless application."""
    c.run(f"{IN_DOCKER} sls deploy")


@task
def remove(c):
    """>> Remove serverless application."""
    c.run(f"{IN_DOCKER} sls remove")


@task
def info(c):
    """>> Serverless application status info. Including endpoints and api token."""
    c.run(f"{IN_DOCKER} sls info")


@task
def offline(c):
    """>> Run serverless application in offline mode."""
    try:
        c.run(f"{IN_DOCKER} sls offline --apiKey {FAKE_API_KEY} --host 0.0.0.0 --printOutput")
    finally:
        remove_build_container(c)


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
    c.run('docker-compose -f docker-compose.yml build')


@task
def run_build_docker_compose(c):
    print(">> Build docker-compose")
    c.run('docker-compose -f docker-compose.yml up -d')


@task
def stop_build_docker_compose(c):
    print(">> Kill docker-compose")
    c.run('docker-compose -f docker-compose.yml kill -s SIGKILL')


@task
def rm_build_docker_compose(c):
    print(">> Remove docker-compose")
    c.run('docker-compose -f docker-compose.yml rm -f')


@task
def remove_build_container(c):
    """>> Build and run sls container."""
    stop_build_docker_compose(c)
    rm_build_docker_compose(c)


@task(pre=[build_build_docker_compose, run_build_docker_compose])
def restart_build_container(c):
    """>> Stop and remove sls container."""


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
