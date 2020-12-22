from invoke import task, Collection


@task
def deploy(c):
    """>> Deploy serverless application"""
    c.run('sls info')


ns = Collection()
serverless = Collection('serverless')

serverless.add_task(deploy, 'deploy')

ns.add_collection(serverless)
