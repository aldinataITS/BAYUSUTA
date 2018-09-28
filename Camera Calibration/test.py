from math import radians,asin,sin,cos,tan,pi,degrees, atan2

lat2 = asin( sin(0.0)*cos(1/6371.01) + cos(0.0)*sin(1/6371.01)*cos(1.57))
print"lat2 #: ",lat2
nlat = asin( sin(0) * cos(1/6371.01) + cos(0) * sin(1/6371.01) * cos(1.57) )
print"rlat #: ",nlat

lat = degrees(lat2)
print"lat2: ",lat
lat = degrees(nlat)
print"lat: ",lat
