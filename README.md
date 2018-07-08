# ArtsLink

Web application can be found at www.ArtsLinkPHL.org

## Team Members

* Steven Bursztyn (Project Manager)
* Rani Iyer (Technical Lead)
* Abhinav Suri
* Nishita Jain
* Brandon Obas

## Setting up

##### Clone the repo

```bash
$ git clone https://github.com/hack4impact/oacce.git
$ cd oacce
```

##### Initialize a virtualenv

```bash
$ pip install virtualenv
$ virtualenv -p python3 venv
$ source venv/bin/activate
```

##### (If you're on a mac) Make sure xcode tools are installed

```bash
$ xcode-select --install
```

#### Install the dependencies

```bash
$ pip install -r requirements.txt
```

##### Add Environment Variables

Create a file called `config.env` that contains environment variables in the following syntax: `ENVIRONMENT_VARIABLE=value`.
You may also wrap values in double quotes like `ENVIRONMENT_VARIABLE="value with spaces"`.
For example, the mailing environment variables can be set as the following.
We recommend using Sendgrid for a mailing SMTP server, but anything else will work as well.

```
MAIL_USERNAME=SendgridUsername
MAIL_PASSWORD=SendgridPassword
SECRET_KEY=SuperRandomStringToBeUsedForEncryption
```

Other Key value pairs:

* `ADMIN_EMAIL`: set to the default email for your first admin account (default is `flask-base-admin@example.com`)
* `ADMIN_PASSWORD`: set to the default password for your first admin account (default is `password`)
* `DATABASE_URL`: set to a postgresql database url (default is `data-dev.sqlite`)
* `REDISTOGO_URL`: set to Redis To Go URL or any redis server url (default is `http://localhost:6379`)
* `RAYGUN_APIKEY`: api key for raygun (default is `None`)
* `FLASK_CONFIG`: can be `development`, `production`, `default`, `heroku`, `unix`, or `testing`. Most of the time you will use `development` or `production`.

**Note: do not include the `config.env` file in any commits. This should remain private.**

##### Install the dependencies

```
$ pip install -r requirements.txt
```

##### Other dependencies for running locally

You need [Redis](http://redis.io/), and [Sass](http://sass-lang.com/). Chances are, these commands will work:


**Sass:**

```
$ gem install sass
```

**Redis:**

_Mac (using [homebrew](http://brew.sh/)):_

```
$ brew install redis
```

_Linux:_

```
$ sudo apt-get install redis-server
```

You will also need to install **PostgresQL**

_Mac (using homebrew):_

```
brew install postgresql
```

_Linux (based on this [issue](https://github.com/hack4impact/flask-base/issues/96)):_

```
sudo apt-get install libpq-dev
```


##### Create the database

```
$ python manage.py recreate_db
```

##### Other setup (e.g. creating roles in database)

```
$ python manage.py setup_dev
```

Note that this will create an admin user with email and password specified by the `ADMIN_EMAIL` and `ADMIN_PASSWORD` config variables. If not specified, they are both `flask-base-admin@example.com` and `password` respectively.

##### [Optional] Add fake data to the database

```
$ python manage.py add_fake_data
```

## Running the app

```
$ source venv/bin/activate
$ honcho start -f Local
```

Then navigate to http://localhost:5000 on your preferred browser to open the web app.

## Formatting code

Before you submit changes, you may want to auto-format your code with `python manage.py format`.

## Updating live site

The site can be found at ArtsLinkPhl.org -- any change made on this repo will be automatically deployed. Therefore, **make sure that the changes made build and work before pushing to master!**

## Documentation

Documentation available at [http://hack4impact.github.io/flask-base](http://hack4impact.github.io/flask-base).

## License
[MIT License](LICENSE.md)
