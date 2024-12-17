import sys
import os
import datetime

from math import *
import numpy as np
import numpy.ma as ma

#debug: import netCDF4
#debug: from netCDF4 import Dataset
#debug: import networkx as netx

#--------------------------------------------------------
def find(lons, lats, lonin, latin):
  #debug print("lon, lat in:",lonin, latin, flush=True)
  tmpx = lons - lonin
  tmpy = lats - latin
  #debug print("x ",tmpx.max(), tmpx.min(), lons.max(), lons.min(), flush=True )

  xmask = ma.masked_outside(tmpx, -0.5, 0.5)
  xin = xmask.nonzero() 
  wmask = ma.logical_and(xmask, ma.masked_outside(tmpy, +0.5, -0.5) )
  win = wmask.nonzero()

  imin = -1 
  jmin = -1
  dxmin = 999.
  dymin = 999.
  dmin  = 999.
  for k in range(0, len(win[0]) ):
    i = win[1][k]
    j = win[0][k] 
    #debug print(k,i,j,abs(tmpx[j,i]), abs(tmpy[j,i]), dxmin, dymin, dmin, flush=True)
    #if (abs(tmpx[j,i]) < dxmin and abs(tmpy[j,i]) < dymin):
    if (sqrt(tmpx[j,i]**2 + tmpy[j,i]**2) < dmin):
      imin = i
      jmin = j
      dxmin = abs(tmpx[j,i])
      dymin = abs(tmpy[j,i])
      dmin  = sqrt(tmpx[j,i]**2 + tmpy[j,i]**2)
  #print("dmin:",imin, jmin, dmin, dxmin, dymin)
  return (imin,jmin)
#--------------------------------------------------------
# Polar ship class
#debug: PC = int(input("What is the polar class of the ship vessel? (1-7)\n"))
PC = 1
PossAnswers = [1, 2, 3, 4, 5, 6, 7]
if(PC not in PossAnswers):
  raise Exception("Please select an answer between 1 and 7.")

def calculateCost(PolarClass, iceCon, iceThick):
    #RIO = (aice*10)RV
    #If aice <= .1, return 0
    #If RIO < 0, return 99999
    cost = 1
    return 1.

    #Considered Ice-Free
    if(iceCon <= .1):
        return 0

    if(PolarClass == 1 or PolarClass == 2 or PolarClass == 3 or PolarClass == 4):
        if(iceThick <= 70):
            cost = 3*(iceCon * 10)
        elif(iceThick <= 120):
            cost = 2*(iceCon * 10)
        else:
            cost = (iceCon * 10)
    elif(PolarClass == 5 or PolarClass == 6):
        if(iceThick <= 70):
            cost = 3*(iceCon * 10)
        elif(iceThick <= 95):
            cost = 2*(iceCon * 10)
        elif(iceThick <= 120):
            cost = iceCon*10
        else:
            return 999
    else:
        if(iceThick <= 30):
            cost = 3*(iceCon * 10)
        elif(iceThick <= 50):
            cost = 2*(iceCon * 10)
        elif(iceThick <= 70):
            cost = iceCon*10
        else:
            return 999
    return cost

#Calculates the distance of two points based on the longitude and latitude points of each point
def calculate_distance(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    earth_radius = 6371

    # Convert latitude and longitude from degrees to radians
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Calculate the distance
    distance = earth_radius * c

    return distance

def cost(case, lat1 = 0, lon1 = 0, lat2 = 0, lon2 = 0, i1 = 0, j1 = 0, i2 = 0, j2 = 0, aice = 0, hi = 0):
  if (case == 1):
    return 1.
  elif (case == 2):
    if (lon1 == 0 and lat1 == 0 and lon2 == 0 and lat2 == 0):
      print("Must give lat,lon of points to compute distance weighting")
      return 1
    else:
      return calculate_distance(lat1, lon1, lat2, lon2)
  elif (case == 3):
    if (i1 == 0 and i2 == 0 and j1 == 0 and j2 == 0):
      print("Must give i,j of points when weighting by polar class")
      return 1
    else:
      return 1 #RG: temporary
  elif (case == 4):
    if (lon1 == 0 and lat1 == 0 and lon2 == 0 and lat2 == 0):
      print("Must give lat,lon of points to compute area-distance weighting")
      return 1.
    else:
      return 1.1*calculate_distance(lat1, lon1, lat2, lon2) / (1.1 - aice)

  else:
    print("unknown case, =",case)
    return 1

#--------------------------------------------------------
