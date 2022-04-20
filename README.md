# HomeInfoDjangoServer

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

## Run Tests

`python3 manage.py test homeinfo/tests`

# Next Steps

- [Dockerize the Project](https://docs.docker.com/samples/django/). Note that the Docket-Django QuickStart guide isn't working out of the gate. `bento-compose up` fails with the exception: `ModuleNotFoundError: No module named 'homeinfo'`.
- [Generate a Secret for Production](https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/)
- [Hookup a Database](https://docs.djangoproject.com/en/3.2/ref/settings/#databases)
- [Create separate Django apps if we intend to have multiple services in the app](https://docs.djangoproject.com/en/4.0/intro/tutorial01/#creating-the-polls-app)
- [Add Access Policy if we want different levels of permissions for different users](https://github.com/rsinger86/drf-access-policy)
- [Setup CORS for more security](https://github.com/adamchainz/django-cors-headers)
- [Investigate Admin URLs](https://docs.djangoproject.com/en/4.0/ref/contrib/admin/)
- Integrate error monitoring service
- Investigate parameterizing tests & disabling logging if the test passes (Both features supported by pytest)
