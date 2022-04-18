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


## Run the Server

`python3 manage.py runserver 0.0.0.0:8000`
