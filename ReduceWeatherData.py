import csv

# Initialize variables
airportIDs=['10140', '10299', '10397', '10423', '10529', '10693', '10721', '10792', '10800', '10821']

# Put header row together
#row = ['Year','Month','Day','Hour','AirportID','Name','PreferredTemperature','ACSetting']
row = ['Month','Day','Hour','AirportID','Temperature','Humidity','Wind']
# Open CSV file
file = open('WeatherData.csv', 'wb')
writer = csv.writer(file, quoting=csv.QUOTE_ALL)

# Write header row
writer.writerow(row)

# Open CSV file
with open('Weather Data.csv') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
    
        if row['AirportID'] not in airportIDs:
            continue
        
        if int(row['AdjustedMonth']) <8 or int(row['AdjustedMonth']) > 10:#not in range(8,10):
            continue
        
        if int(row['AdjustedDay']) <1 or int(row['AdjustedDay']) > 30:#not in range(1,30):
            continue
            
        if int(row['AdjustedHour']) <6 or int(row['AdjustedHour']) > 23:#not in range(6,23):
            continue
            
        # Write CSV file
        writer.writerow([row['AdjustedMonth'],row['AdjustedDay'],row['AdjustedHour'],row['AirportID'],row['DryBulbCelsius'],row['RelativeHumidity'],row['WindSpeed']])

# Close file
file.close()