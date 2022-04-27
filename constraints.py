"""
Steering servo angle ≤ 𝛿max = 30°
(b) velocity per step ≤ 𝑣𝑚𝑎𝑥 = 2 𝑐𝑚/𝑠𝑒𝑐,
(c) x-position of the front-right of the car ≥ 𝑊𝑏 + 𝑑𝑚 if its y-position ≥ (𝐿𝑏 / 2)
(d_1) x-position of rear right of the car ≥ 𝑑𝑚 = 2 𝑐𝑚, 
(d_2) x-position of front right of the car ≥ 𝑑𝑚 = 2 𝑐𝑚, 
(e) y-distance of rear right of the car ≥ 𝑑𝑚𝑖𝑛 𝑟 = 5𝑐𝑚,
(f) y-distance of the front right of the car in step 2N ≥ 𝑑𝑚𝑖𝑛 𝑓 = 5𝑐𝑚, . 
(Note: these numbers are just guesses; if you need to change them a bit to make things work, that’s fine). 
"""

import mpc

class Constraints:
	@staticmethod
	def check_constraint_c(car):
		pass

	@staticmethod
	def check_constraint_d_1(car):
		pass

	@staticmethod
	def check_constraint_d_2(car):
		pass

	@staticmethod
	def check_constraint_e(car):
		pass

	@staticmethod
	def check_constraint_f(car):
		pass

	@staticmethod
	def check_constraint_a(car):
		MAX_ANGLE = 30

		if car.heading_angle > MAX_ANGLE:
			return False
		else:
			return True

		return true

	@staticmethod
	def check_constraint_b(car):
		MAX_VELOCITY = 2

		if car.velocity > MAX_VELOCITY:
			return False
		else: 
			return True