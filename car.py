import math
import box
import display

def to_radians(degrees):
  return degrees * (math.pi / 180)



# x1 = x0cos(θ) – y0sin(θ)(Equation 1)
# y1 = x0sin(θ) + y0cos(θ)

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
  DISTANCE_CENTER_MASS_R = 4.5 # I_r (cm) (UNUSED)

  MARGIN_BOTTOM = 10           # d_m term

  def __init__(self):
    self.velocity = 2                                  # Placeholder
    self.steering_angle = 10.0                          # Steering angle (deg)
    self.heading_angle = 0.0                           # "Car Heading" Angle - Psi (deg)

    self.x = box.Box.length / 2                        # Rear Left X Position
    self.y = -(box.Box.width / 2) - Car.MARGIN_BOTTOM  # Rear Left Y Position

    self.center_x = self.x + (Car.LENGTH / 2)
    self.center_y = self.y + (Car.WIDTH / 2) 



  def get_coordinates(self, point):
    """
    L1  L2  
    [   ]
    R1  R2
    """

    # TODO: For physical car

    pass

  def get_display_coordinates(self, point):
    """
    L1  L2  
    [   ]
    R1  R2

    x' = x cos(theta) - y sin(theta)
    y' = y cos(theta) + x sin(theta)
    """

    if point == 'L1':
      unrotated_coordinates = [ -(Car.LENGTH / 2), - (Car.WIDTH / 2) ]

      unrotated_coordinates = rotate_point(unrotated_coordinates, -self.heading_angle)

      return (
        display.Display.TRUE_X + ((self.center_x + unrotated_coordinates[0]) * display.Display.SCALE),
        display.Display.TRUE_Y + ((self.center_y + unrotated_coordinates[1]) * display.Display.SCALE) 
        )

    if point == 'L2':
      unrotated_coordinates = [ (Car.LENGTH / 2), -(Car.WIDTH / 2) ]

      unrotated_coordinates = rotate_point(unrotated_coordinates, -self.heading_angle)


      return (
        display.Display.TRUE_X + ((self.center_x + unrotated_coordinates[0]) * display.Display.SCALE),
        display.Display.TRUE_Y + ((self.center_y + unrotated_coordinates[1]) * display.Display.SCALE) 
        )
      
    if point == 'R2':
      unrotated_coordinates = [ (Car.LENGTH / 2), (Car.WIDTH / 2) ]

      unrotated_coordinates = rotate_point(unrotated_coordinates, -self.heading_angle)


      return (
        display.Display.TRUE_X + ((self.center_x + unrotated_coordinates[0]) * display.Display.SCALE),
        display.Display.TRUE_Y + ((self.center_y + unrotated_coordinates[1]) * display.Display.SCALE) 
        )
    if point == 'R1':
      unrotated_coordinates = [ - (Car.LENGTH / 2), (Car.WIDTH / 2) ]

      unrotated_coordinates = rotate_point(unrotated_coordinates, -self.heading_angle)


      return (
        display.Display.TRUE_X + ((self.center_x + unrotated_coordinates[0]) * display.Display.SCALE),
        display.Display.TRUE_Y + ((self.center_y + unrotated_coordinates[1]) * display.Display.SCALE) 
        )
  

  def move(self, delta_time):
    # self.x -= (self.velocity * math.cos(to_radians(self.heading_angle))) * delta_time

    # # += to account for pygame's coordinate system, should be -=
    # self.y += (self.velocity * math.sin(to_radians(self.heading_angle))) * delta_time

    self.center_x -= (self.velocity * math.cos(to_radians(self.heading_angle))) * delta_time

    # += to account for pygame's coordinate system, should be -=
    self.center_y += (self.velocity * math.sin(to_radians(self.heading_angle))) * delta_time

    self.heading_angle += (self.velocity / Car.DISTANCE_CENTER_MASS_F) * self.steering_angle * delta_time

  def print_state(self):
    print(f'True x, y: ({(display.Display.ORIGIN_X - display.Display.TRUE_X) + self.x},{(display.Display.ORIGIN_Y - display.Display.TRUE_Y) + self.y}), v={self.velocity}, steer_ang={self.steering_angle}, head_ang={self.heading_angle}')