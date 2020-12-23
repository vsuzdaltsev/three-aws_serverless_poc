from logging import Logger

from invoke import task, Collection


def lambdas():
    return ['create_s3_bucket']


@task
def deploy(c):
    """>> Deploy serverless application."""
    c.run('sls deploy')


@task
def remove(c):
    """>> Remove serverless application."""
    c.run('sls remove')


def log(severity, message):
    Logger(name='__name__').__getattribute__(severity)(message)


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
