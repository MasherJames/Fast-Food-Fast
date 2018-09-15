![license](https://img.shields.io/github/license/mashape/apistatus.svg)
[![Build Status](https://travis-ci.org/MasherJames/Food-delivery.svg?branch=develop)](https://travis-ci.org/MasherJames/Food-delivery)
[![Coverage Status](https://coveralls.io/repos/github/MasherJames/Food-delivery/badge.svg?branch=develop)](https://coveralls.io/github/MasherJames/Food-delivery?branch=develop)
[![GitHub issues](https://img.shields.io/github/issues/MasherJames/Food-delivery.svg)](https://github.com/MasherJames/Food-delivery/issues)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/2f0335eec7df4311bd9c7d7d177b6a6a)](https://www.codacy.com/app/MasherJames/Food-delivery?utm_source=github.com&utm_medium=referral&utm_content=MasherJames/Food-delivery&utm_campaign=Badge_Grade)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)

# Fast Food Fast

Fast food fast is a food delivery application.

## How it Works

- An admin creates food items
- A normal user creates an account and can login
- A logged in user can view available food items created by the admin
- A user chooses on a food item and makes an order
- An Admin can accept or reject the order request from a user
- A user gets notified on his/her order status
- Accepted orders are delivered

## Prerequisite

- [Python3.6](https://www.python.org/downloads/release/python-365/)
- [Virtua Environment](https://virtualenv.pypa.io/en/stable/installation/)

# Installation and Setup

Clone the repository below

```
git clone git@github.com:MasherJames/Fast-Food-Fast.git
```

### Create and activate a virtual environment

    virtualenv env --python=python3.6

    source env/bin/activate

### Install required Dependencies

    pip install -r requirements.txt

## Running the application

```bash
$ export FLASK_APP = run.py

$ export MODE = development

$ flask run
```

## Endpoints Available

| Method | Endpoint                                 | Description                                   |
| ------ | ---------------------------------------- | --------------------------------------------- |
| POST   | /api/v1/auth/signup                      | sign up a user                                |
| POST   | /api/v1/auth/login                       | login a user                                  |
| POST   | /api/v1/fooditems                        | post a fooditem                               |
| GET    | /api/v1/fooditems                        | get all available fooditems                   |
| POST   | /api/v1/fooditems/<{id}>/orders          | post an order on a specific food item         |
| GET    | /api/v1/fooditems/orders                 | get the all food orders                       |
| GET    | /api/v1/fooditems/orders/<{id}>          | get a specific food order                     |
| GET    | /api/v1/fooditems/<{id}>                 | get a specific fooditem                       |
| GET    | /api/v1/fooditems/orders/customer_name   | get all orders for a specific customer        |
| DELETE | /api/v1/fooditems/<{id}>                 | delete a specific fooditem                    |
| PUT    | /api/v1/fooditems/<{id}>                 | update an existing fooditem                   |
| PUT    | /api/v1/fooditems/orders/<{id}>/accept   | update on the status of an order to accepted  |
| PUT    | /api/v1/fooditems/orders/<{id}>/decline  | update on the status of an order to declined  |
| PUT    | /api/v1/fooditems/orders/<{id}>/complete | update on the status of an order to completed |
| GET    | /api/v1/fooditems/orders/accepted        | get the all accepted food orders              |
| GET    | /api/v1/fooditems/orders/declined        | get the all declined food orders              |
| GET    | /api/v1/fooditems/orders/completed       | get the all completed food orders             |

### Testing

    nosetests

    - Testing with coverage

    nosetests --with-coverage --cover-package=app

### Author

James Macharia
