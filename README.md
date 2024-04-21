# Football Mixer

A project made at InHolland University of Applied Sciences for the Big Data & AI minor.

The 'app' folder contains a Python project that uses the Flask framework to create a REST API, which interacts with a ML model that analyses microphone data input to determine the sounds of a football match.

The 'client' folder contains a Quasar project that uses Vue.js to interact with the REST API.

## Requirements for Client

- Node.js
- Yarn

## Requirements for App

- Python 3.9

## Getting Client to work

Go to the 'client' folder and run the following commands:

```bash
yarn install
```

### Start the app in development mode (hot-code reloading, error reporting, etc.)

```bash
yarn run dev
```

### Build the app for production

```bash
yarn run build
```

## Getting App to work

### Initial setup

For the initial setup, you need a virtual environment. To create one, run the following commands:

```bash
python3 -m venv .venv
```

I **HIGHLY** recommend modifying the `.venv/bin/activate` file to include the following line at the end:

```bash
export FLASK_APP=manage.py
```

This will automatically set the `FLASK_APP` environment variable every time you activate the virtual environment, so you don't have to do it manually every time.

To activate the virtual environment, run the following command:

```bash
source .venv/bin/activate
```

### Install dependencies

To install the dependencies, run the following command:

```bash
python3.9 -m pip install -r requirements.txt
```

### Start the app

To start the app, run the following command:

```bash
python3.9 -m flask run
```

For hot-reloading, you can use the following command:

```bash
python3.9 -m flask --debug run
```

## Usage with Postman

To use the API with Postman, you can import the following collection:

[![Run in Postman](https://run.pstmn.io/button.svg)](https://lively-desert-374565.postman.co/collection/30102792-2bff9db9-3da0-446d-8322-e4330bbe6983?source=rip_html)

You can also simply connect to http://localhost:5000/ and use the Swagger UI.

## Authors

- [Konrad Figura](mailto:mail@kfigura.nl)
- [Rareş Simion](mailto:683655@student.inholland.nl)
- [Rodrigo Bange](mailto:rodrigo99@live.nl)
- [Philip Tsagli](mailto:682624@student.inholland.nl)
- [Mirko Cuccurullo](mailto:691362@student.inholland.nl>)
