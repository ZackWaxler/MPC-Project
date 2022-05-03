from mpc import *
from box import *
from car import Car

class Constraints:
	"""
	MPC constraint checkers
	"""

	MAX_ANGLE = 30

	MIN_VELOCITY = 1
	MAX_VELOCITY = 10

	# Minimum distance between (0, 0) and (car.center_x, car.center_y) at the end of phase 1
	MARGIN_CENTER = 2

	# Minimum heading angle that the car can have at the end of phase 2
	HEADING_ANGLE_MINIMUM = 1

	@staticmethod
	def steering_angle(car):
		if car.steering_angle > Constraints.MAX_ANGLE:
			return False
		else:
			return True

	@staticmethod
	def velocity(car):
		if car.velocity > Constraints.MAX_VELOCITY:
			return False
		else: 
			return True

	@staticmethod
	def avoid_box_collision(car, box):
		"""
		The third condition avoids the front of the car going into the box in front of the car.
		"""

		rx, ry = car.get_coordinates('R1')
		lx, ly = car.get_coordinates('L1')

		# print(f'R1({rx},{ry}) L1({lx},{ly}), Box: ({box.x},{box.y}) => ({box.x + Box.WIDTH},{box.y + Box.LENGTH})')

		if rx < box.x + Box.WIDTH or lx < box.x + box.WIDTH:
			return False

		return True

	def avoid_lower_bound(car, phase):
		"""
		Prevent the car from going under the spot (phase 2)
		"""
		if phase != 2:
			return True

		r1x, r1y = car.get_coordinates('R1')
		r2x, r2y = car.get_coordinates('R2')

		if r1y > Box.LENGTH / 2 or r2y > Box.LENGTH / 2:
			return False
		else:
			return True

	@staticmethod
	def phase_1_on_track(car, step, phase, lookahead_step):
		# Only apply the following logic to phase 1
		if phase != 1:
			return True

		# If at step 'N' in the lookahead, is the car within the acceptable location range?
		if step + lookahead_step == MPC.STEPS_PER_PHASE:
			# Compute the distance between (0, 0) and (car.center_x, car.center_y) w/ the distance between points formula
			distance = math.sqrt(
				math.pow( (car.center_x - 0), 2 ) + \
				math.pow( (car.center_y - 0), 2 ) )

			if distance < Constraints.MARGIN_CENTER: 
				return True
			else:
				return False
		else:
			return True

	@staticmethod
	def phase_2_on_track(car, step, phase, lookahead_step):
		# Only apply the following logic to phase 1
		if phase != 2:
			return True

		if step + lookahead_step == MPC.STEPS_PER_PHASE * 2:
			if car.heading_angle > Constraints.HEADING_ANGLE_MINIMUM:
				return False

		return True