import math
# import box
from box import *
import display

def to_radians(degrees):
  return degrees * (math.pi / 180)

def rotate_point(point, degrees):
  x = point[0]
  y = point[1]

  theta = to_radians(degrees)

  x_prime = x * math.cos(theta) - y * math.sin(theta)
  y_prime = x * math.sin(theta) + y * math.cos(theta)

  return [ x_prime, y_prime ]

class Car:
  """
   MPC-Controlled Car
  """

  # Static
  LENGTH = 22                  # Car length (cm)
  WIDTH = 16                   # Car width (cm)

  DISTANCE_CENTER_MASS_F = 5   # I_f (cm)
  MARGIN_BOTTOM = 7            # Margin for the starting y position of the car (d_m term)

  def __init__(self):
    self.velocity = 2                                  # Placeholder
    self.steering_angle = 0.0                          # Steering angle (deg)
    self.heading_angle = 0.0                           # "Car Heading" Angle - Psi (deg)

    self.x = Box.WIDTH / 2                             # Rear left starting x position                          
    self.y = -Box.LENGTH - Car.MARGIN_BOTTOM           # Rear left starting y position

    self.center_x = self.x + (Car.LENGTH / 2)
    self.center_y = self.y + (Car.WIDTH / 2) 

  def get_coordinates(self, point):
    """
            L1  L2  
    (Back)  [   ]  (Front)
            R1  R2
    """

    x, y = self.get_display_coordinates(point)

    return (
      (x - display.Display.TRUE_X) / display.Display.SCALE,
      (y - display.Display.TRUE_Y) / display.Display.SCALE,
    )

  def get_display_coordinates(self, point):
    """
            L1  L2  
    (Back)  [   ]  (Front)
            R1  R2

    Get the display-relative coordinates of a given point on the car. 

    TODO: Refactor
    """

    if point == 'L1':
      unrotated_coordinates = [ -(Car.LENGTH / 2), - (Car.WIDTH / 2) ]

      rotated_coordinates = rotate_point(unrotated_coordinates, -self.heading_angle)

      return (
        display.Display.TRUE_X + ((self.center_x + rotated_coordinates[0]) * display.Display.SCALE),
        display.Display.TRUE_Y + ((self.center_y + rotated_coordinates[1]) * display.Display.SCALE) 
        )

    if point == 'L2':
      unrotated_coordinates = [ -(Car.LENGTH / 2), (Car.WIDTH / 2) ]

      rotated_coordinates = rotate_point(unrotated_coordinates, -self.heading_angle)

      return (
        display.Display.TRUE_X + ((self.center_x + rotated_coordinates[0]) * display.Display.SCALE),
        display.Display.TRUE_Y + ((self.center_y + rotated_coordinates[1]) * display.Display.SCALE) 
        )
      
    if point == 'R2':
      unrotated_coordinates = [ (Car.LENGTH / 2), (Car.WIDTH / 2) ]
      rotated_coordinates = rotate_point(unrotated_coordinates, -self.heading_angle)

      return (
        display.Display.TRUE_X + ((self.center_x + rotated_coordinates[0]) * display.Display.SCALE),
        display.Display.TRUE_Y + ((self.center_y + rotated_coordinates[1]) * display.Display.SCALE) 
        )
    if point == 'R1':
      unrotated_coordinates = [ (Car.LENGTH / 2), - (Car.WIDTH / 2) ]
      # unrotated_coordinates = [ - (Car.LENGTH / 2), (Car.WIDTH / 2) ]
      rotated_coordinates = rotate_point(unrotated_coordinates, -self.heading_angle)

      return (
        display.Display.TRUE_X + ((self.center_x + rotated_coordinates[0]) * display.Display.SCALE),
        display.Display.TRUE_Y + ((self.center_y + rotated_coordinates[1]) * display.Display.SCALE) 
        )

  def move(self, delta_time, steering_angle, velocity):
    self.center_x -= (velocity * math.cos(to_radians(self.heading_angle))) * delta_time
    self.center_y += (velocity * math.sin(to_radians(self.heading_angle))) * delta_time

    self.heading_angle += (velocity / Car.DISTANCE_CENTER_MASS_F) * steering_angle * delta_time    
