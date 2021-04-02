f = open('locations.csv', 'r')
LocList = []
for line in f: 
    placename, long, lat, notes = line.strip().split(',')
    if placename == '': 
        placename = None
    if long == '': 
        long = None
    if lat == '':
        lat = None
    if notes == '':
        notes == None
    try:
        coordinates = [float(lat), float(long)]
    except:
        coordinates = [lat, long]
    if coordinates != [None, None]:
        LocList.append(coordinates)
f.close()
print(LocList)
