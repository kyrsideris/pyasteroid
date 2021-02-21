from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.vector import Vector


class Asteroid(Widget):

	x_vel = NumericProperty(0)
	y_vel = NumericProperty(0)
	velocity = ReferenceListProperty(x_vel, y_vel)

	def move(self):
		"""Handle movement of the asteroids"""
		self.pos = Vector(*self.velocity) + self.pos

	def hit_player(self, player):
		if self.collide_widget(player):
			# Decrement player lives
			player.lives -= 1