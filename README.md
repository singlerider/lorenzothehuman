# lorenzothehuman
An extension of lorenzotherobot, an IRC chatbot companion for Twitch.tv.

The purpose of this repository is to provide the chatbot everything it needs
to be able to extend rudimentary bi-directional communications based on
existing chat logs.

## Installation

Setting up a virtual environment (ideally), installing dependencies, and gaining
credentials.

### Virtual Environment

I would recommend running this in a virtual environment to keep your
dependencies in check. If you'd like to do that, run:

`sudo pip install virtualenv`

Followed by:

`virtualenv venv`

This will create an empty virtualenv in your project directory in a folder
called "venv." To enable it, run:

`source venv/bin/activate`

and your console window will be in that virtualenv state. To deactivate, run:

`deactivate`

### Dependencies

To install all dependencies locally (preferably inside your activated
virtualenv), run:

`pip install -r requirements.txt`

### Further Steps

Make a copy of the example config file:

`cp config_example.py config.py`

Go in the config.py file and modify the existing information to reflect your
current credentials setup for your database.

Depending on how you set this thing up, you can have it gather data directly
from your database or from a series of API endpoints.

#### MySQL Installation

Depending on your distribution, starting the server will be different, on a mac, this is accomplished by doing

`brew install mysql`

`mysql.server start`

### Dependencies

To install all dependencies locally (preferably inside your activated
virtualenv), run:

`pip install -r requirements.txt`

## To Run
(TODO)
