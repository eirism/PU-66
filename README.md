# PU-66

To run locally you need python3, pip, a database (Postgres is preferred) and an account at [Indico](https://indico.io/dashboard/).

## Installation
`pip install -r requirements.txt`

## Running locally
The following environment variables needs to be set.
| Variable       | Value |
| -------------- | ----- |
| SECRET_KEY     | A random value, keep it secret |
| DATABASE_URL   | [A SQLAlchemy database url](http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls) |
| PORT           | The port number the server will run on |
| INDICO_API_KEY | Your [Indico](https://indico.io/) API key |


Run the server with `python run.py`

## Running tests
To run the tests and generate html coverage report: `PYTHONPATH=. py.test --cov-report html:cov_html --cov=iris tests`
