# TrueLayer Pokedex

## Tech Stack
Built on top of the following tech: Serverless(sls), python, Flask, Flask-RESTful, AWS Lambda, API-Gateway


## Prerequisites
1. Clone this repo.
2. [Install](https://serverless.com/framework/docs/providers/aws/guide/installation/) serverless. Then [read a quick example.](https://serverless.com/blog/flask-python-rest-api-serverless-lambda-dynamodb)
3. Make sure you've installed:
	- brew
	- python 3.7
	- node.js, npm


## Project Structure
Though the problem is simple. OOP patters are fallowed, specifically, the Strategy, Factory and Singleton patterns. The project has the following main folders:

* **`/src`**
  * `/config`: the basic config of the application.
  * `/core`: like `base_resource`: the base class for any flask RESTful resource.
  * `/domain`: the actual logic where we handle strategies and factories. Mainly singletons.
  * `/resources`: the presentation layer of the API.
  * `/services`: contains clients to 3rd party API like PokeAPI and translation APIs. Mainly singletons.
  * `/exceptions`: for custom exceptions. 
  * `/tests`: contains `/unit`: For unit tests and `/integration`: for end-to-end testing.


## Setup Local Development
- Create a virtual environment and install your dependencies (once):
```shell script
cd path/to/project
rm -rf venv
python3.7 -m venv venv
source venv/bin/activate
pip install -r requirements/development.txt
```

#### Note for MacOS
- According to this [bug](https://github.com/dherault/serverless-offline/issues/1150), and your version of linux/Mac, you may need to enforce another version of node for the POST request to work. Tested with v14.17.0 and it works.

## Running Local Development
- Run the flask app:
```shell script
cd path/to/project
source venv/bin/activate
sls offline start --stage local-api --region local
```
   
- The output should be similar to this:
```shell script
 * Running on http://localhost:5010/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
```

- A list of the supported API endpoints will showup:
```
ANY | http://localhost:5010/local-api                               ???
???   POST | http://localhost:5010/2015-03-31/functions/app/invocations   ???
???   ANY | http://localhost:5010/local-api/{proxy*}                      ???
???   POST | http://localhost:5010/2015-03-31/functions/app/invocations   ???
???   GET | http://localhost:5010/local-api/v1/mobile-app/init            ???
???   POST | http://localhost:5010/2015-03-31/functions/app/invocations   ???
```

- Now you can make API calls like:
```
http://localhost:3000/local-api/v1/pokemon/mewtwo
```
They need `client_id` and `client_secret` with `Basic` auth. For local setup, simply use:
```
client_id = 123
client_secret = 123
```

This can be easily exchanged with X-API keys if we want.

## Running Tests Locally
- Run the tests:
```shell script
cd path/to/project
source venv/bin/activate
stage=test-api stage_rcs=test pytest src/tests  --hypothesis-show-statistics --cov=src --cov-report html
```

## CI/CD Pipeline
- In the future we can simply integrate this with CircleCI/Jenkins.
