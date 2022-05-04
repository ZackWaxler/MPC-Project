"""
Model Predictive Controller

TODO:
- Fix inverted y-axis positivity
"""

import math, time, copy
import random

from box import *
from display import *
from car import *
from constraints import *

class MPC:
  """
   MPC Controller
  """

  # Number steps per phase
  STEPS_PER_PHASE = 20

  # Number of steps to look ahead
  NUM_LOOKAHEAD_STEPS = 20

  # Delay between steps (seconds)
  DELTA_TIME = 0.5

  # Should arbitrary errors be added to the simulation?
  # This will occasionally cause the simulation to fail.
  # With this option enabled, try running the simulation multiple times. 
  ADD_ERRORS = False

  # Percent chance that a small actuation error will occur
  ERROR_RATE = 0.2

  def __init__(self):
    self.car = None     # Placeholder
    self.display = None # Placeholder

    self.step = 0

    # Current phase the car is in:
    # - 1: navigating to (0,0)
    # - 2: straightening
    # - 3: setting the angle to 0
    self.phase = 1

  def attachDisplay(self, display):
    self.display = display

  def check_constraints(self, car, lookahead_step):    
    if Constraints.velocity(car) and \
       Constraints.steering_angle(car) and \
       Constraints.avoid_lower_bound(car, self.phase) and \
       Constraints.avoid_box_collision(car, self.boxes[1]) and \
       Constraints.phase_1_on_track(car, self.step, self.phase, lookahead_step) and \
       Constraints.phase_2_on_track(car, self.step, self.phase, lookahead_step):

      return True
    else:
      return False
  
  # Run the simulation for the next num_steps steps and return the next steering angle and velocity pair that satisfies all constraints
  def look_ahead(self, num_steps):
    current_velocity = Constraints.MIN_VELOCITY

    # For each possible velocity value:
    while current_velocity < Constraints.MAX_VELOCITY:
      current_angle = 0

      # Positive steering angle in phase 1, negative steering angle in phase 2
      if self.phase == 1:
        angle_direction = 1      
      else:
        angle_direction = -1

      # For the given velocity value:
      # - Check if there is an angle that satisfies all constraints
      # - If not, increment the velocity
      while current_angle < Constraints.MAX_ANGLE:
        iteration_car = copy.deepcopy(self.car)

        working_angle = True

        for i in range(num_steps):
          iteration_car.move(MPC.DELTA_TIME, angle_direction * current_angle, current_velocity)

          # Ensure that each constraint is satisfied for each lookahead step
          if not self.check_constraints(iteration_car, i):
            working_angle = False
        
        if working_angle == True:
          print(f'[Phase {self.phase}, Step {self.step}] Satisfactory steering angle, velocity found: ({angle_direction * current_angle}deg, {current_velocity}cm/step)')
          return (angle_direction * current_angle, current_velocity)
        else:
          current_angle += 1

      current_velocity += 1

    print('[FATAL] NO COMBINATION OF POSSIBLE ANGLES + VELOCITIES WILL SATISFY THE CONSTRAINTS FROM THIS POSITION. QUITTING.')

  def generate_actuation_error(self, rate):
    if random.random() < rate: 
      print(f'[!] Artificially adding error to step {self.step}')
      if random.choice([True, False]):
        self.car.center_x += (random.random() / 2) * random.choice([1, -1])
      else:
        self.car.center_y += (random.random() / 2) * random.choice([1, -1])

  def next_step(self):
    # Perform the lookahead to find a satisfactory steering angle and velocity for the next step
    next_angle, next_velocity = self.look_ahead(MPC.NUM_LOOKAHEAD_STEPS)

    # Update the values for the display
    self.car.steering_angle = next_angle
    self.car.velocity = next_velocity

    # Apply the movement to the real car
    self.car.move(MPC.DELTA_TIME, next_angle, next_velocity)

    # Generate artificial actuation error
    if MPC.ADD_ERRORS:
      self.generate_actuation_error(MPC.ERROR_RATE)

    # Snap the car to a straight angle at the end of both phases
    if self.phase == 3:
      self.car.heading_angle = 0

    # Send information about the state of the simulation to the display thread
    if self.display is not None:
      self.display.update_boxes(self.boxes)
      self.display.update_car(self.car)
      self.display.update_step(self.step)

    # Sleep for DELTA_TIME, then continue to the next step
    time.sleep(MPC.DELTA_TIME)
    self.step += 1

  # Start the simulation
  def start(self):
    self.car = Car()
    self.boxes = [ Box(-Box.WIDTH / 2, -Box.LENGTH / 2,       (0, 255, 0)),  # Middle Box
                   Box(-(3 / 2) * Box.WIDTH, -Box.LENGTH / 2, (255, 0, 0)),  # Left Box
                   Box(Box.WIDTH * (1/2), -Box.LENGTH / 2,    (255, 0, 0)) ] # Right

    # Iterate through all 2N + 1 steps, updating the phase accordingly
    while self.step < MPC.STEPS_PER_PHASE * 2 + 1:
      if self.step == MPC.STEPS_PER_PHASE:
        self.phase = 2

      elif self.step == MPC.STEPS_PER_PHASE * 2:
        self.phase = 3

      self.next_step()

def main():
  mpc = MPC()
  display = Display()

  mpc.attachDisplay(display)
  mpc.start()

if __name__ == '__main__':
  main()