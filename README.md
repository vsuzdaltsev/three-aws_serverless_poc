# AWS Serverless POC

## LCM

### Prerequisites

- `python` >= 3.8
- `serverless` framework
- `pipenv`

### Prepare environment

- Prepare python environment

```
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

  local.autopep8       >> Run autocorrection on python files.
  serverless.deploy    >> Deploy serverless application.
  serverless.offline   >> Run serverless application in offline mode.
  serverless.remove    >> Remove serverless application.

```

- Export credentials

```
$ export AWS_REGION="[region here]"
$ export AWS_ACCESS_KEY_ID="[access key id here]"
$ export AWS_SECRET_ACCESS_KEY="[secret access key here]"

```

- Deploy application

```
$ inv serverless.deploy
```

- Remove application along with all related resources

```
$ inv serverless.remove
```
