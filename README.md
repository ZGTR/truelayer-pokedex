# TrueLayer Pokedex

## Tech Stack
Built on top of the following tech: Serverless(sls), python (Flask), AWS: lambda, api-gateway


## Prerequisites
1. Clone this repo.
2. [Install](https://serverless.com/framework/docs/providers/aws/guide/installation/) serverless. Then [read a quick example.](https://serverless.com/blog/flask-python-rest-api-serverless-lambda-dynamodb)
3. Make sure you've installed:
	- brew
	- python 3.7
	- node.js, npm


## Setup Local Development
- Install Pipenv (system wide)
```shell script
pip install pipenv
```

- Create a virtual environment and install your dependencies (once):
```shell script
cd path/to/project
pipenv --rm
pipenv install --python 3.7 --dev
npm install
```

#### Note for MacOS
- According to this [bug](https://github.com/dherault/serverless-offline/issues/1150), and your version of linux/Mac, you may need to enforce another version of node for the POST request to work. Tested with v14.17.0 and it works.

## Running Local Development
- Run the flask app:
```shell script
cd path/to/project
pipenv shell
sls offline --stage local-api --region local --httpPort 5010
```
   
- The output should be similar to this:
```shell script
 * Running on http://localhost:5010/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
```

## Running Tests Locally
- Run the tests:
```shell script
cd path/to/project
pipenv shell
stage=test-api stage_rcs=test pytest src/tests  --hypothesis-show-statistics --cov=src --cov-report html
```

## CI/CD Pipeline
- In the future we can simply integrate this with CircleCI/Jenkins.
