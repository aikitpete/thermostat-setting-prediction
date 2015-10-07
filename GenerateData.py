import csv
#import gauss
import random

# Open CSV file
file = open('UserData.csv', 'wb')
writer = csv.writer(file, quoting=csv.QUOTE_ALL)

# Put header row together
row = ['Year','Month','Day','Hour','AirportID','Name','PreferredTemperature','ACSetting']

# Write header row
writer.writerow(row)

# Initialize variables
copies=25
year=2015

# Initialize variables
airportIDs=['10140', '10299', '10397', '10423', '10529', '10693', '10721', '10792', '10800', '10821']

# Month cycle
for m in range(8, 11):  
    # Day cycle
    for d in range(1, 31):
        # Hour cycle
        for h in range(0, 24):
            # Airport cycle
            for airportID in airportIDs:
                # Create copies of user
                for x in range(0, copies):
                    
                    # Generate unique name
                    name = 'u'+'M'+str(m)+'D'+str(d)+'H'+str(h)+'A'+airportID+'X'+str(x)
                    
                    # Generate preferred temperature
                    preferredTemperature=random.gauss(20,4)
                    
                    # Generate AC setting
                    ACSetting = 0;
                    
                    # Put everything into one row
                    row = [year,m,d,h,airportID,name,preferredTemperature,ACSetting]
                    
                    # Write CSV file
                    writer.writerow(row)

# Close file
file.close()