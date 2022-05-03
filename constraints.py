"""
(Note: these numbers are just guesses; if you need to change them a bit to make things work, that’s fine). 
"""

import mpc
from box import Box
from car import Car

class Constraints:
	"""
	MPC constraint checkers
	"""

	@staticmethod
	def steering_angle(car):
		"""
		(a) Steering servo angle ≤ 𝛿_max = 30°
		(UNCHECKED)
		"""

		MAX_ANGLE = 30

		if car.steering_angle > MAX_ANGLE:
			return False
		else:
			return True

	@staticmethod
	def velocity(car):
		"""
		(b) velocity per step ≤ 𝑣𝑚𝑎𝑥 = 2 𝑐𝑚/𝑠𝑒𝑐,
		(UNCHECKED)
		"""

		MAX_VELOCITY = 2

		if car.velocity > MAX_VELOCITY:
			return False
		else: 
			return True

	@staticmethod
	def avoid_box_collision(car):
		"""
		(c) x-position of the front-right of the car ≥ 𝑊𝑏 + 𝑑𝑚 if its y-position ≥ (𝐿𝑏 / 2)
		(UNCHECKED)
		"""

		x, y = car.get_coordinates('R1')

		if y >= Box.LENGTH / 2:
			if x < Box.WIDTH + Car.MARGIN_BOTTOM:
				return False

		return True

## ALL THE BELOW ONES ARE WRONG

	# @staticmethod
	# def check_constraint_d_1(car):
	# 	"""
	# 	(d_1) x-position of rear right of the car ≥ 𝑑𝑚 = 2 𝑐𝑚
	# 	(UNCHECKED)
	# 	"""
		
	# 	x, y = car.get_display_coordinates('R1')

	# 	if x < Car.MARGIN_BOTTOM:
	# 		return False
	# 	else: 
	# 		return True

	# @staticmethod
	# def check_constraint_d_2(car):
	# 	"""
	# 	(d_2) x-position of front right of the car ≥ 𝑑𝑚 = 2 𝑐𝑚
	# 	(UNCHECKED)
	# 	"""
	# 	x, y = car.get_display_coordinates('R1')

	# 	if x < Car.MARGIN_BOTTOM:
	# 		return False
	# 	else:
	# 		return True

	# # TODO:
	# @staticmethod
	# def check_constraint_e(car):
	# 	"""
	# 	(e) y-distance of rear right of the car ≥ 𝑑𝑚𝑖𝑛 𝑟 = 5𝑐𝑚
	# 	(UNCHECKED)
	# 	"""
	# 	return True

	# @staticmethod
	# def check_constraint_f(car, step):
	# 	"""
	# 	(f) y-distance of the front right of the car in step 2N ≥ 𝑑𝑚𝑖𝑛 𝑓 = 5𝑐𝑚
	# 	(UNCHECKED)
	# 	"""
	# 	x, y = car.get_display_coordinates('R2')

	# 	return True

		# if step > N:
		# 	if y < 
		# else:
		# 	return True


