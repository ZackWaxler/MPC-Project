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

import constraints

class MPC:
  """
   MPC Controller
  """

  # Static

  # N steps per phase
  N = 20 * 100         

  # Delay between steps (seconds)
  DELTA_TIME = 0.01

  def __init__(self):
    self.car = None     # Placeholder
    self.display = None # Placeholder
    self.step = 0

  def attachDisplay(self, display):
    self.display = display

  def next_step(self):
    self.car.move(MPC.DELTA_TIME)

    # Display Boxes and Car
    if self.display is not None:
      self.display.update_boxes(self.boxes)

    self.display.update_car(self.car)
    self.display.update_step(self.step)

    time.sleep(MPC.DELTA_TIME)

    self.step += 1

  # TODO:
  def look_ahead(steps):
    plan = [] # 2d array of [[steering_angle, velocity]]

    car = self.car

    # for i in range(steps):
    #   while not Constraints.satisfies_constraints(car):
    #     car = self.car

    #     planned_step = [] # [steering_angle, velocity]

    #     car.steering_angle = planned_step[0]
    #     car.velocity = planned_step[1]
    #     car.move(MPC.DELTA_TIME)

    #   plan.push(planned_step)

  def start(self):
    self.car = Car()
    self.boxes = [ Box(-Box.WIDTH / 2, 0,       (255, 0, 0)),  # Middle Box
                   Box(-(3 / 2) * Box.WIDTH, 0, (0, 255, 0)),  # Left Box
                   Box(Box.WIDTH * (1/2), 0,    (0, 0, 255)) ] # Right

    while self.step < self.N * 2 + 1:
      self.next_step()

  def print_state(self):
    print(self.step)
    self.car.print_state()

def main():
  mpc = MPC()
  display = Display()

  mpc.attachDisplay(display)
  mpc.start()

if __name__ == '__main__':
  main()