# wuzzel-ranking
This repository contains a simple ranking-system for wuzzeln.

**NOTE: This project is still in development!**

## Setting everything up
All the software is ready to be hosted on [pythonanywhere](https://www.pythonanywhere.com/).
The only thing to be done after cloning this repository is the configuration.
Create a virtualenv: `mkvirtualenv wuzzel-ranking --python=python3.6`.
Install tools in virtualenv with `pip install flask flask-login flask-sqlalchemy mysql-connector-python`.
Install Flask-Migrate using `pip install Flask-Migrate`.


## Configuration
Create a `config.py`-file in this repository.
This file should hold the following configuration:
**Note: You have to change the strings below!**
```python
secret_key = "<random string for encrypting the sessions>"
db_hostname = "<hostname of your database>"
db_name = "<name of your database>"
db_user = "<user for your database>"
db_password = "<password for the database>"

```
