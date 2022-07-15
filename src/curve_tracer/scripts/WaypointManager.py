#! /usr/bin/env python3

import numpy as np


class WaypointManager:
  def __init__(self,res=1):
    self.index = 0
    self.res = res
    self.way_point()

  def way_point(self):
    #create a numpy array of 'res' points in range 0 to 2*pi
    x = np.linspace(0, 2*np.pi, num = self.res, endpoint=True)[1:]
    #create a numpy array of given path function 
    y = np.sin(x)
    #Returning waypoints in form of (x,y)
    self.list_waypoints  = list(zip(x,y))
    
    return self.list_waypoints
  
  def get_next_waypoint(self):
     
    #Checking if the bot has reached the destination
    if self.index >= len(self.list_waypoints):
      print("Bot has reached its destination")
      return 
    
    self.next_waypoint = self.list_waypoints[self.index]
    self.index = self.index + 1
  
    return self.next_waypoint


if __name__ == "__main__":
  waypoint_manager = WaypointManager(res=10)
  print(waypoint_manager.way_point())
  print(waypoint_manager.get_next_waypoint())
