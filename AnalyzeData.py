import csv

with open('Flight Data.csv') as csvfile:
    reader = csv.DictReader(csvfile)

    airports = []
    for row in reader:
        #print(row['DestAirportID'])
        if row['DestAirportID'] not in airports:
                airports.append(row['DestAirportID'])

airports.sort()          
print airports
print airports[0:10]

with open('Weather Data.csv') as csvfile:
    reader = csv.DictReader(csvfile)

    airports2 = []
    for row in reader:
        #print(row['AirportID'])
        if row['AirportID'] not in airports2:
                airports2.append(row['AirportID'])

airports2.sort()
print airports2
print airports2[0:10]

result = list(set(airports) & set(airports2))

result.sort()
print result
