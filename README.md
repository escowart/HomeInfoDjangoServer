# Home Info Django Server

Get information about homes!

# Setup

1. Install [Python3](https://www.python.org/downloads/)
2. Install [Pycharm](https://www.jetbrains.com/pycharm/download)
3. Install dependencies: `pip3 install -r requirements.txt`
4. Black
   1. Install BlackConnect Plugin: PyCharm > Preferences > Plugins > MarketPlace > BlackConnect
   2. Enable black format on save: PyCharm > Preferences > Tools > BlackConnect > Trigger when saving changed files
   3. Create blackd PyCharm startup script: PyCharm > Preferences > Tools > Startup Tasks > + (Add New Configuration) > Shell Script
      - Name: blackd
      - Execute: Script text
      - Script text: blackd
      - Execute in terminal: uncheck
      - Activate tool window: uncheck
5. Setup File Header: PyCharm > Preferences > Editor > File and Code Templates > Python Script

```
  """
  Author: ${USER}
  Created: ${DATE}
  """
```
6. Install Requirements Plugin: PyCharm > Preferences > Plugins > MarketPlace > Requirements

## Run Development Server

`python3 manage.py runserver 0.0.0.0:8000`

The development server can then be accessed at `http://0.0.0.0:8000`

## Run Tests

`python3 manage.py test homeinfo/tests`


## Available APIs

Summary: Does the given address have a septic tank for sewage?

Method: `GET`

Path: `home/septic`

Content Type: `application/json`

Authorization: `None`

Query Params

   - `address`
     - Type: string
     - Required: True
     - Example: "123+Main+St"
   
   - `zipcode`
     - Type: string
     - Required: True
     - Example: "20500"

Responses

   - `200`
     - Scenario: Call to House Canary succeeded
     - Body
       - Type: boolean
       - Example: True
   - `400`
     - Scenario: Missing Required Query Parameter
     - Body:
       - Type: string
       - Example: "Missing require query params: address and zipcode"
   - `500`
     - Scenario: Internal Server Error
     - Body:
       - Type: string
       - Example: "Oops! something went wrong. Please contact us for assistance at 1-800-123-5678!"
   - `503`
     - Scenario: Call to House Canary Failed
     - Body:
       - Type: string
       - Example: "Oops! something went wrong with our home info service. Please contact us for assistance at 1-800-123-5678!"


# Next Steps

- [Dockerize the Project](https://docs.docker.com/samples/django/). Note that the Docket-Django QuickStart guide isn't working out of the gate. `docker-compose up` fails with the exception: "ModuleNotFoundError: No module named 'homeinfo'".
- [Checklist for Django Deployment to Production](https://docs.djangoproject.com/en/4.0/howto/deployment/)
- Research & Integrate an off-premise logging and error monitoring service
- [Remove development dependencies from requirements.txt](https://stackoverflow.com/questions/63836220/creating-a-requirements-txt-without-development-dependencies) during the production/QA build process
- [Hookup separate environment files for: dev, qa, prod (maybe demo as well)](https://medium.com/@mateo.cobanov/using-multiple-env-files-in-django-1a4390b4762c). Production environment keys will never be committed to version control.
- Turn off DEBUG in settings.py for production.
- [Generate a new Django Secret for production](https://humberto.io/blog/tldr-generate-django-secret-key/). DO NOT add to version control.
- [Hookup a Gunicorn, Nginx, & HTTPS](https://realpython.com/django-nginx-gunicorn/) for load balancing & additional security
- [Hookup a Database](https://docs.djangoproject.com/en/4.0/ref/settings/#databases)
- [Hookup a Cache to reduce the number of requests to the Home Canary API](https://docs.djangoproject.com/en/4.0/topics/cache/)
- [Create separate Django apps if we intend to have multiple services in the app](https://docs.djangoproject.com/en/4.0/intro/tutorial01/#creating-the-polls-app)
- [Add Access Policy if we want different levels of permissions for different users](https://github.com/rsinger86/drf-access-policy)
- [Setup CORS for more security](https://github.com/adamchainz/django-cors-headers)
- [Investigate Admin URLs](https://docs.djangoproject.com/en/4.0/ref/contrib/admin/)
- Investigate parameterizing tests & disabling logging if the test passes (Both features are supported by pytest)
- Validate inbound data, so we don't waste resources or $$$ with a call to an external service
