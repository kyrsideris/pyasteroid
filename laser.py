from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.vector import Vector


class Laser(Widget):

	x_vel = NumericProperty(0)
	y_vel = NumericProperty(0)
	velocity = ReferenceListProperty(x_vel, y_vel)

	def move(self):
		"""Handle movement of the 'laser'"""
		self.pos = Vector(*self.velocity) + self.pos

	def hit_asteroid(self, asteroid, player):

		if self.collide_widget(asteroid):
			
			# Reset laser
			self.pos = [1600, 1200]
			self.velocity = [0, 0]

			# Decrease asteroid size
			asteroid.size[0] /= 2
			asteroid.size[1] /= 2

			# Slightly speedup and change the direction of the asteroid
			speedup = 1.1
			offset = 0.01 * Vector(0, asteroid.center_y - self.center_y)
			asteroid.velocity = speedup * (offset - asteroid.velocity)

			player.score += 100