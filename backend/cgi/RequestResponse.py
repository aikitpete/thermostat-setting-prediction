import os
import json
import sys

try:
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import Request, urlopen, HTTPError

api_key = os.environ["AZURE_ML_API_KEY"]
url = os.environ.get(
    "AZURE_ML_URL",
    "https://europewest.services.azureml.net/workspaces/8a441e205cc444b9857777ace9d422bb/services/86c9bc5197f646269ded6dce7e95a2c9/execute?api-version=2.0&details=true"
)

if len(sys.argv) != 8:
    print("Usage: script.py <Temperature> <Wind> <Humidity> <Temperature Preference> <Morning> <Noon> <Evening>")
    sys.exit(1)

data = {
    "Inputs": {
        "Input": {
            "ColumnNames": [
                "Temperature", "Wind", "Humidity",
                "Temperature Preference", "Morning", "Noon", "Evening"
            ],
            "Values": [
                [sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7]]
            ]
        }
    },
    "GlobalParameters": {}
}

body = json.dumps(data).encode("utf-8")
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + api_key,
}

req = Request(url, body, headers)

try:
    response = urlopen(req)
    result = response.read()
    print(result.decode("utf-8"))
except HTTPError as error:
    print("The request failed with status code: {}".format(error.code))
    print(error.info())
    print(error.read().decode("utf-8"))
