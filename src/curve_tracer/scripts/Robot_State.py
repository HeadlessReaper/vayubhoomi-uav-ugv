from enum import Enum

class Bot_State(Enum):


  IdleState = 0
  Fixing_Yaw = 1
  Moving_Straight = 2
  Goal_Reached = 3
