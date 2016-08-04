#!/usr/bin/python
import math
from math import tan, sin, cos

def getDistance_v2(lat_a, lng_a, lat_b, lng_b):
   pk = 180 / 3.14169  
   a1 = lat_a / pk
   a2 = lng_a / pk  
   b1 = lat_b / pk  
   b2 = lng_b / pk  
   t1 = math.cos(a1) * math.cos(a2) * math.cos(b1) * math.cos(b2)  
   t2 = math.cos(a1) * math.sin(a2) * math.cos(b1) * math.sin(b2)  
   t3 = math.sin(a1) * math.sin(b1)  
   tt = math.acos(t1 + t2 + t3)  
   return 6366000 * tt  

def getDistance(Lat_A, Lng_A, Lat_B, Lng_B):
   if (Lat_A - Lat_B) < 10e-4 and (Lng_A - Lng_B) < 10e-4:
      return 0
   ra = 6378.140  
   rb = 6356.755 
   flatten = (ra - rb) / ra
   rad_lat_A = math.radians(Lat_A)
   rad_lng_A = math.radians(Lng_A)
   rad_lat_B = math.radians(Lat_B)
   rad_lng_B = math.radians(Lng_B)
   pA = math.atan(rb / ra * tan(rad_lat_A))
   pB = math.atan(rb / ra * tan(rad_lat_B))
   xx = math.acos(math.sin(pA) * sin(pB) + cos(pA) * cos(pB) * cos(rad_lng_A - rad_lng_B))
   c1 = (sin(xx) - xx) * (sin(pA) + sin(pB)) ** 2 / cos(xx / 2) ** 2
   c2 = (sin(xx) + xx) * (sin(pA) - sin(pB)) ** 2 / sin(xx / 2) ** 2
   dr = flatten / 8 * (c1 - c2)
   distance = ra * (xx + dr)
   return distance

#  print getDistance(32.060255, 118.796877, 39.904211, 116.407395)


def getCloudlet(latitude, longitude, cloudletPositions):
   cloudlet = 1
   i  = 0
   min_c = 100000
   for position in cloudletPositions:
      i += 1
      position_t = position.split(' ')
      dis = getDistance((float)(latitude), (float)(longitude), (float)(position_t[1]), (float)(position_t[2]))
      if dis < min_c:
         min_c = dis
         cloudlet = i
   return cloudlet
