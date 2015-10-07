import csv

# Initialize variables
airportIDs=['10140', '10299', '10397', '10423', '10529', '10693', '10721', '10792', '10800', '10821']

# Put header row together
#row = ['Year','Month','Day','Hour','AirportID','Name','PreferredTemperature','ACSetting']
row = ['Month','Day','Hour','Carrier','OriginAirportID','DestAirportID']
# Open CSV file
file = open('FlightData2.csv', 'wb')
writer = csv.writer(file, quoting=csv.QUOTE_ALL)

# Write header row
writer.writerow(row)

# Open CSV file
with open('Flight Data.csv') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
    
        if row['DestAirportID'] not in airportIDs:
            continue
        
        if int(row['Month']) <8 or int(row['Month']) > 10:#not in range(8,10):
            continue
        
        if int(row['DayofMonth']) <1 or int(row['DayofMonth']) > 30:#not in range(1,30):
            continue
            
        if int(row['CRSArrTime']) <6 or int(row['CRSArrTime']) > 23:#not in range(6,23):
            continue
            
        # Write CSV file
        writer.writerow([row['Month'],row['DayofMonth'],row['CRSArrTime'],row['Carrier'],row['OriginAirportID'],row['DestAirportID']])

# Close file
file.close()