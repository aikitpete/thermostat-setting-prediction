from pandas import *
from numpy import *
from random import *
from math import *
from locale import *

df = DataFrame({'vals': [4, 2, 3, 1], 'ids': ['a', 'b', 'f', 'n'],'ids2': ['3', '1', '4', '2']})

print df

df2 = DataFrame(df, index=['2', '3'])

print df2

df3 = df.sort(['ids2'])

print df3

df4 = df[(df.vals>2)&(df.ids2>2)]

print df4

forbidden = ['b','f']
df5 = df[df['ids'].isin(forbidden)]

print df5

df6 = DataFrame({'month': [4, 2, 3, 1], 'day': [8, 13, 21, 4],'hour': [3, 1, 4, 2], 'AirportID': [12345, 23456, 34567, 45678], 'foo': [3, 1, 4, 2]})

print df6

df7 = DataFrame({'month': [4, 2, 6, 3, 1], 'day': [8, 13, 56, 21, 4],'hour': [9, 1, 0, 4, 2], 'AirportID': [12345, 23456, 77777, 34567, 45678], 'tss': ['a', 'm', 'u', 'b', 'a']})

print df7

df8 = merge(df6, df7, how='left', on=['month','day','hour','AirportID'])

print df8

df9 = df8
df9['extra'] = df9['month']+df9['hour'] 

print df9

df10 = DataFrame({'vals': [4, 2, 3, 1], 'ids': ['a', 'b', 'f', 'n'],'ids2': ['3', '1', '4', '2']})
df10['extra'] = 'GGG'
df10['extra'] = df10['extra'] + df10['ids'] 

print df10

df11 = DataFrame(np.random.randn(10, 5))

print df11

df12 = DataFrame()
#df12['Timeline'] = range(1,101)
df12['Year'] = np.random.randint(2012,2016,size=100)
df12['Month'] = np.random.randint(1,13,size=100)
df12['Day'] = np.random.randint(1,32,size=100)
df12['Hour'] = np.random.randint(0,24,size=100)
temp = DataFrame({'Value':[3]})
df12['Season'] = np.ceil(df12['Month']/temp['Value'].values) 
df12['Temperature Preference'] = np.round(np.random.normal(22,5,100),decimals=1)
df12['Morning'] = [1 if (x>=4 and x<10) else 0 for x in df12['Hour']] 
df12['Noon'] = [1 if (x>=10 and x<16) else 0 for x in df12['Hour']] 
df12['Evening'] = [1 if (x>=16 and x<22) else 0 for x in df12['Hour']]
df12['Midnight'] = [1 if (x>=22 or x<4) else 0 for x in df12['Hour']]
temp = DataFrame({'Value1':[16],'Value2':[10],'Value3':[6]})
df12['Temperature'] = np.round(np.random.normal(18,5)+temp['Value1'].values*df12['Morning']+temp['Value2'].values*df12['Noon']+temp['Value3'].values*df12['Evening'],decimals=1)
temp = DataFrame({'Value1':[2],'Value2':[0],'Value3':[4]})
df12['Wind'] = np.round(np.random.normal(11,7)+temp['Value1'].values*df12['Morning']+temp['Value2'].values*df12['Noon']+temp['Value3'].values*df12['Evening'],decimals=1)
temp = DataFrame({'Value1':[2],'Value2':[-2],'Value3':[4]})
df12['Humidity'] = np.round(np.random.normal(18,5)+temp['Value1'].values*df12['Morning']+temp['Value2'].values*df12['Noon']+temp['Value3'].values*df12['Evening'],decimals=1)
df12['Flight Number'] = np.random.randint(1,101,size=100)
temp = DataFrame({'Value1':[100],'Value2':[100],'Value3':[4]})
df12['AC Setting'] = np.round(np.random.normal((df12['Temperature']-df12['Temperature Preference'])*((df12['Temperature']/temp['Value1'].values)+(df12['Temperature Preference']/temp['Value2'].values)),temp['Value3'].values),decimals=1)

print df12
