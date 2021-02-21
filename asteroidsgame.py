from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.vector import Vector
from math import sin, cos, radians, degrees, pi
from laser import Laser
from asteroid import Asteroid
from random import randint


class AsteroidsGame(Widget):
        spaceship = ObjectProperty(None)
        laser = Laser()
        laser2 = Laser()
        laser3 = Laser()
        asteroid = Asteroid()
        asteroid2 = Asteroid()
        count = 0
        im_too_lazy_to_think_this_through = True

        def __init__(self, **kwargs):
                super(AsteroidsGame, self).__init__(**kwargs)
                self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
                self._keyboard.bind(on_key_down=self._on_keyboard_down)

        def _keyboard_closed(self):
                self._keyboard.unbind(on_key_down=self._on_keyboard_down)
                self._keyboard = None

        def _on_keyboard_down(self, keyboard, keycode, text, modifiers):

                # MOVEMENT

                # Angle, in radians, of the spaceship
                spaceship_angle = radians(self.spaceship.angle)

                # Reversed cosine and sine to make 0 radians point/move up and to make
                # movement feel more natural
                if keycode[1] == 'up':
                        self.spaceship.x_vel -= sin(spaceship_angle)
                        self.spaceship.y_vel += cos(spaceship_angle)

                if keycode[1] == 'down':
                        self.spaceship.x_vel += sin(spaceship_angle)
                        self.spaceship.y_vel -= cos(spaceship_angle)

                # Rotation
                if keycode[1] == 'right':
                        self.spaceship.turning_vel -= 1.5

                if keycode[1] == 'left':
                        self.spaceship.turning_vel += 1.5

                # Shooting
                if keycode[1] == 'spacebar':
                        if self.laser.pos == [1600, 1200]:
                                self.laser.center = self.spaceship.center
                                self.laser.x_vel = -(sin(radians(self.spaceship.angle))) * 25
                                self.laser.y_vel = cos(radians(self.spaceship.angle)) * 25

                # PAUSING AND RESUMING

                if keycode[1] == 'p':
                        self.pause_toggle = not self.pause_toggle

                return True

        def spawn_asteroid(self):

                random_coordinates = [
                        randint(0, self.width),
                        randint(0, self.height)
                ]
                self.asteroid.velocity = Vector(4, 0).rotate(randint(0, 360))
                self.asteroid.pos = random_coordinates
                self.asteroid2.velocity = Vector(4, 0).rotate(randint(0, 360))
                self.asteroid2.pos = random_coordinates

        def check_player_lives(self):

                if self.spaceship.lives <= 0:
                        #Stop game
                        #'GAME OVER'
                        #play again?
                        pass

        def update(self, dt):

                # Romove laser after 60/100ths of a second
                if self.laser.x_vel != 0 or self.laser.y_vel != 0:
                        self.count += 1
                        if self.count > (60 * 0.6):
                                self.count = 0
                                self.laser.pos = -100, -100
                                self.laser.x_vel = 0
                                self.laser.y_vel = 0

                # Allow movement
                self.asteroid.move()
                self.asteroid2.move()
                self.laser.move()
                self.laser2.move()
                self.laser3.move()
                self.spaceship.move()


                # Spawn asteroid
                if self.im_too_lazy_to_think_this_through:
                        self.spawn_asteroid()
                        self.im_too_lazy_to_think_this_through = False

                # Handle laser-asteroid collision
                self.laser.hit_asteroid(self.asteroid, self.spaceship)
                self.laser.hit_asteroid(self.asteroid2, self.spaceship)

                # Handle player-asteroid collision
                self.asteroid.hit_player(self.spaceship)
                self.spaceship.hit_asteroid(self.asteroid)
                self.asteroid2.hit_player(self.spaceship)
                self.spaceship.hit_asteroid(self.asteroid2)

                # FRICTION LOGIC
                # Slow down the spaceship movement over time
                # Divide by 60 to compensate for x60 update rate

                # UPWARD VELOCITY // POSITIVE y_vel
                if self.spaceship.y_vel > 0:
                        self.spaceship.y_vel -= (self.spaceship.y_vel / 2) / 60

                # RIGHT VELOCITY // POSITIVE x_vel
                if self.spaceship.x_vel > 0:
                        self.spaceship.x_vel -= (self.spaceship.x_vel / 2) / 60
                # Rotation
                if self.spaceship.turning_vel < 0:
                        self.spaceship.turning_vel -= (self.spaceship.turning_vel * 2) / 60

                # DOWNWARD VELOCITY // NEGATIVE y_vel
                if self.spaceship.y_vel < 0:
                        self.spaceship.y_vel += -(self.spaceship.y_vel / 2) / 60

                # LEFT VELOCITY // NEGATIVE x_vel
                if self.spaceship.x_vel < 0:
                        self.spaceship.x_vel += -(
                                self.spaceship.x_vel / 2) / 60
                # Rotation
                if self.spaceship.turning_vel > 0:
                        self.spaceship.turning_vel -= (
                                self.spaceship.turning_vel * 2) / 60

                # SCREEN COLLISION
                # Warp objects on screen collision
                transition_offset = -10

                # BOTTOM
                if self.spaceship.top < 0:
                        self.spaceship.y = self.height

                if self.laser.top < 0:
                        self.laser.y = self.height

                if self.asteroid.top < 0:
                        self.asteroid.y = self.height
                if self.asteroid2.top < 0:
                        self.asteroid2.y = self.height

                # TOP
                if self.spaceship.y > self.height:
                        self.spaceship.top = 0

                if self.laser.y > self.height:
                        self.laser.top = 0

                if self.asteroid.y > self.height:
                        self.asteroid.top = 0
                if self.asteroid2.y > self.height:
                        self.asteroid2.top = 0

                # LEFT
                if self.spaceship.right < transition_offset:
                        self.spaceship.x = self.width

                if self.laser.right < transition_offset:
                        self.laser.x = self.width

                if self.asteroid.right < transition_offset:
                        self.asteroid.x = self.width
                if self.asteroid2.right < transition_offset:
                        self.asteroid2.x = self.width

                # RIGHT
                if self.spaceship.x > self.width:
                        self.spaceship.right = 0

                if self.laser.x > self.width:
                        self.laser.right = 0

                if self.asteroid.x > self.width:
                        self.asteroid.right = 0
                if self.asteroid2.x > self.width:
                        self.asteroid2.right = 0
