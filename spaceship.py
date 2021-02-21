from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.vector import Vector


class Spaceship(Widget):

	lives = NumericProperty(3)
	score = NumericProperty(0)

	x_vel = NumericProperty(0)
	y_vel = NumericProperty(0)
	velocity = ReferenceListProperty(x_vel, y_vel)
	angle = NumericProperty(0)
	turning_vel = NumericProperty(0)

	def move(self):
		"""Handle movement of the spaceship"""
		self.pos = Vector(*self.velocity) + self.pos
		self.angle = self.turning_vel + self.angle

	def respawn(self):
		self.pos = self.parent.center

	def hit_asteroid(self, an_asteroid):
		if self.collide_widget(an_asteroid):
			self.respawn()