"""
Model Predictive Controller
- Assume position is always known
- Velocity chosen at each step (but "not instantaneously???")

TODO:
- y-coordinate positivity is inverted
"""

import math, time

from box import Box
from display import Display
from car import Car

from constraints import *

class MPC:
  """
   MPC Controller
  """

  # Number steps per phase
  STEPS_PER_PHASE = 50

  # Delay between steps (seconds)
  DELTA_TIME = 0.5

  def __init__(self):
    self.car = None     # Placeholder
    self.display = None # Placeholder
    self.step = 0

    # Current phase the car is in
    # 0 => navigating to (0,0)
    # 1 => straightening
    # 2 => setting the angle to 0
    self.phase = 0 

  def attachDisplay(self, display):
    self.display = display

  def check_constraints(self):
    print(f'p:{self.phase},s:{self.step} --- velocity : {Constraints.velocity(self.car)}')
    print(f'p:{self.phase},s:{self.step} --- steering_angle: {Constraints.steering_angle(self.car)}')
    print(f'p:{self.phase},s:{self.step} --- avoid_box_collision: {Constraints.avoid_box_collision(self.car)}')

    print(self.car.get_coordinates('L1'))
  
  # # Look ahead i steps and return the next steering angle that satisfies all constraints
  # def look_ahead(self, num_steps):
  #   working_angle = None
  #   current_angle = 0

  #   while working_angle == None:
  #     iteration_car = copy.deep_copy(self.car)

  #     iteration_car.steering_angle = testing_angle

  #     # Move num_steps times with the specified steering angle
  #     for i in range(num_steps):
  #       iteration_car.move()

  #     # Probably going to need to change this
  #     if self.check_constraints(iteration_car):
  #       return testing_angle
  #     else:
  #       current_angle += 3


  def next_step(self):
    self.check_constraints()

    self.car.move(MPC.DELTA_TIME)

    # Send information to the display thread
    if self.display is not None:
      self.display.update_boxes(self.boxes)

    self.display.update_car(self.car)
    self.display.update_step(self.step)

    time.sleep(MPC.DELTA_TIME)

    self.step += 1

  def start(self):
    self.car = Car()
    self.boxes = [ Box(-Box.WIDTH / 2, 0,       (255, 0, 0)),  # Middle Box
                   Box(-(3 / 2) * Box.WIDTH, 0, (0, 255, 0)),  # Left Box
                   Box(Box.WIDTH * (1/2), 0,    (0, 0, 255)) ] # Right

    while self.step < MPC.STEPS_PER_PHASE * 2 + 1:
      if self.step == MPC.STEPS_PER_PHASE:
        self.phase = 1

      elif self.step == MPC.STEPS_PER_PHASE * 2:
        self.phase = 2 

      self.next_step()

def main():
  mpc = MPC()
  display = Display()

  mpc.attachDisplay(display)
  mpc.start()

if __name__ == '__main__':
  main()