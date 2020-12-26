# AWS Serverless POC

## LCM

### Requirements

The following software is to be installed to start:

- `python` >= 3.8
- `pipenv`
- `docker` & `docker-compose`

### Environment setup

- Prepare python environment

```
$ cd [repo root directory]
$ pipenv --python 3.8
$ pipenv shell
$ pipenv sync
$ pipenv sync --dev
```

- List available tasks

```
$ inv -l
>>
Available tasks:

  local.autopep8                 >> Run autocorrection on python files.
  serverless.deploy              >> Deploy serverless application.
  serverless.info                >> Serverless application status info. Including endpoints and api token.
  serverless.offline             >> Run serverless application in offline mode.
  serverless.rebuild-container   >> Build and run build container.
  serverless.remove              >> Remove serverless application.
  serverless.stop-container      >> Stop and remove sls container.

```

- Export credentials

```
$ export AWS_REGION="[region here]"
$ export AWS_ACCESS_KEY_ID="[access key id here]"
$ export AWS_SECRET_ACCESS_KEY="[secret access key here]"

```

- Start docker
- Build and run serverless container:

```
$ inv serverless.rebuild-container
```

### Deploy application

```
$ inv serverless.deploy
```

### Run application in offline mode

- Run fake api gateway

```
$ inv serverless.offline
```

- Check available routes:

```
$ curl localhost:3000
>>
{
  "currentRoute": "get - /",
  "error": "Serverless-offline: route not found.",
  "existingRoutes": [
    "post - /prod/poc/create_s3_bucket",
    "get - /prod/poc/list_s3_bucket/{bucket_name}",
    "post - /prod/poc/upload_to_s3_bucket"
  ],
  "statusCode": 404
}
```

### Remove application along with all related resources

```
$ inv serverless.remove
```

### Stop and remove serverless container

```
$ inv serverless.stop-container
```
