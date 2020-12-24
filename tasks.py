from logging import Logger

from invoke import task, Collection
import yaml


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
def autopep8(c):
    """>> Run autocorrection on python files."""
    log('warning', ">> Autocorrect python files according to styleguide")
    c.run("autopep8 --in-place --max-line-length 200 --aggressive *.py --verbose")

    for wd in lambdas():
        with c.cd(wd):
            log('info', f">> Change working directory to {wd}")
            log('info', ">> Autocorrect python files according to styleguide")
            c.run("autopep8 --in-place --recursive . --max-line-length 200 --aggressive --verbose")


ns = Collection()
local = Collection('local')
serverless = Collection('serverless')

local.add_task(autopep8, 'autopep8')
serverless.add_task(deploy, 'deploy')
serverless.add_task(remove, 'remove')

ns.add_collection(local)
ns.add_collection(serverless)
