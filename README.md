# AWS Serverless POC

## LCM

### Prerequisites

Small demo application which includes AWS Api Gateway and several AWS Lambdas behind it. This has been tested with
macOS, but should work under Linux & Windows as well.

#### Software requirements

The following software is to be installed to start:

- `python` >= 3.8
- `pipenv`
- `docker` & `docker-compose`

### Environment setup

#### Prepare python environment:

```
$ cd [repo root directory]
$ pipenv --python 3.8
$ pipenv shell
$ pipenv sync
$ pipenv sync --dev
```

#### List available tasks:

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

#### Export AWS credentials to authorize serverless

```
$ export AWS_REGION="[region here]"
$ export AWS_ACCESS_KEY_ID="[access key id here]"
$ export AWS_SECRET_ACCESS_KEY="[secret access key here]"

```

#### Start docker

#### Build and run the serverless container:

```
$ inv serverless.rebuild-container
```

### Deployment

```
$ inv serverless.deploy
```

### Launching the application in offline mode

#### Run fake api gateway:

```
$ inv serverless.offline
```

#### Check available routes:

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

#### Run demo script

This will do the following:

* Create s3 bucket
* Generate several random files
* Upload them concurrently to s3
* In order to utilize real API Gateway and Lambdas instead of locally running mocks, set the proper endpoint and token (
  env: TEST_POC_API_KEY, BASE_URI). They can be found in the output of `inv serverless.info` command.

```
$ python demo.py
```

NB: do not forget to remove test s3 bucket!

### Application removal

#### Remove application along with all related resources

```
$ inv serverless.remove
```

### Stopping container

#### Stop and remove serverless container

```
$ inv serverless.stop-container
```
