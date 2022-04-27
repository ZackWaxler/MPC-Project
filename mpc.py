"""
Model Predictive Controller
- Assume position is always known
- Velocity chosen at each step (but "not instantaneously???")

TODO:
- Get the correct x, y coordinates of the top right by determining what kind of logic is used by the pygame image rotator

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
  N = 200         # N steps per phase
  DELTA_TIME = 0.1 # (seconds)

  def __init__(self):
    self.car = None     # Placeholder
    self.display = None # Placeholder
    self.step = 0

  def attachDisplay(self, display):
    self.display = display

  def next_step(self):
    time.sleep(MPC.DELTA_TIME)

    self.car.move(MPC.DELTA_TIME)

    # Display Boxes and Car
    if self.display is not None:
      self.display.update_boxes(self.boxes)

    self.display.update_car(self.car)
    self.display.update_step(self.step)

    self.step += 1

  def start(self):
    self.car = Car()
    self.boxes = [ Box(-Box.width / 2, 0,       (255, 0, 0)),   # Middle Box
                   Box(-(3 / 2) * Box.width, 0, (0, 255, 0)),  # Left Box
                   Box(Box.width * (1/2), 0,    (0, 0, 255)) ] # Right

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