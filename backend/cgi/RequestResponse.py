import urllib2
# If you are using Python 3+, import urllib instead of urllib2

import json 
import sys

data =  {

        "Inputs": {

                "Input":
                {
                    "ColumnNames": 
                    [
                        "Temperature", "Wind", "Humidity", "Temperature Preference", "Morning", "Noon", "Evening"
                    ],
                    "Values": 
                    [ 
                        [ 
                            sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7]
                        ], 
                        [ 
                            sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7]
                        ] 
                    ]
                },        
        },
        "GlobalParameters": {
        }
}

body = str.encode(json.dumps(data))

url = 'https://europewest.services.azureml.net/workspaces/8a441e205cc444b9857777ace9d422bb/services/86c9bc5197f646269ded6dce7e95a2c9/execute?api-version=2.0&details=true'
api_key = 'y02I/HrFvr/Spfuz5LI5VKcdLfEslc+m6HPvLYNrz5s9nAyNkE8DKEnPCmDvuISOXsHHtls2rPTTP94IrtYNvQ==' # Replace this with the API key for the web service
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

req = urllib2.Request(url, body, headers) 

try:
    response = urllib2.urlopen(req)

    # If you are using Python 3+, replace urllib2 with urllib.request in the above code:
    # req = urllib.request.Request(url, body, headers) 
    # response = urllib.request.urlopen(req)

    result = response.read()
    print(result) 
except urllib2.HTTPError, error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())

    print(json.loads(error.read()))       
