# Cookbook API

Cookbook API is a simple REST application for creating recipes with ingredients.

## Create an environment

In the project folder, create a `venv` folder:

```bash
cd /path/to/project
python3 -m venv venv
```

## Activate the environment

Before starting the application, activate the corresponding environment:

```bash
. venv/bin/activate
```

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install cookbook-api requirements.

```bash
pip install -r requirements.txt
```

## Start the application

After setup is completed, start the application:

```bash
python app.py
```

## Usage

User will have to sign up for an account, and login in order to call the endpoints:

```python
POST /recipe
{
  "name": "cake",
  "ingredients": [
    {
      "name": "flour",
      "quantity": 1
    },
    {
      "name": "egg",
      "quantity": 4
    }
  ]
}
```
