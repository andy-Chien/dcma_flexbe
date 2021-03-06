#!/usr/bin/env python

from flexbe_core import EventState, Logger
from math import radians
import random
import ikfast_ur5
import time

class Ur5IkState(EventState):
	"""
	Calculate IK of UR5.

	># tar_trans               float[]
	># tar_rot                 float[]

	#> joint_values            float[]		   Target joint values of robot

	<= done										Pose has been published.
	<= fail                 

	"""
	
	def __init__(self):
		"""Constructor"""
		super(Ur5IkState, self).__init__(outcomes=['done', 'fail'], input_keys=['tar_trans', 'tar_rot'], output_keys=['joint_values'])
		self.success = False
		self.ur5_sols = None

	def execute(self, userdata):
		if self.success:
			indx = 5 if len(self.ur5_sols) >= 6 else 2 if len(self.ur5_sols) >= 3 else 0
			userdata.joint_values = self.ur5_sols[indx]
			return 'done'
		else:
			return 'fail'

	def on_enter(self, userdata):
		self.success = False
		self.ur5_sols = None
		if userdata.tar_trans is not None and userdata.tar_rot is not None:
			if len(userdata.tar_trans) == 3 and len(userdata.tar_rot) == 3 and len(userdata.tar_rot) == 3:
				self.ur5_sols = ikfast_ur5.get_ik(userdata.tar_trans, userdata.tar_rot)
				print('-------')
				for sol in self.ur5_sols:
					print sol
				print('++++++++')
				self.success = True
