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

## Run Server

`python3 manage.py runserver 0.0.0.0:8000`

The server can be accessed by making requests to `http://0.0.0.0:8000`

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
   - `401`
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


## Run Tests

`python3 manage.py test homeinfo/tests`

# Next Steps

- [Dockerize the Project](https://docs.docker.com/samples/django/). Note that the Docket-Django QuickStart guide isn't working out of the gate. `docker-compose up` fails with the exception: "ModuleNotFoundError: No module named 'homeinfo'".
- [Generate a Secret for Production](https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/)
- [Hookup a Database](https://docs.djangoproject.com/en/3.2/ref/settings/#databases)
- [Create separate Django apps if we intend to have multiple services in the app](https://docs.djangoproject.com/en/4.0/intro/tutorial01/#creating-the-polls-app)
- [Add Access Policy if we want different levels of permissions for different users](https://github.com/rsinger86/drf-access-policy)
- [Setup CORS for more security](https://github.com/adamchainz/django-cors-headers)
- [Investigate Admin URLs](https://docs.djangoproject.com/en/4.0/ref/contrib/admin/)
- Integrate error monitoring service
- Investigate parameterizing tests & disabling logging if the test passes (Both features supported by pytest)
- Validate inbound data, so we don't waste resources or $$$ with a call to an external service
- Capturing contract violations at the service level rather than allowing the exception to propagate down the call stack
