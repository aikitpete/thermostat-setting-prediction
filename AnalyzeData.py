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