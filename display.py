import pygame, time, threading

from box import *
from car import *

class Display:
  """
   Create a visual representation of the MPC controls
  """

  TITLE = 'Parallel Parking MPC Simulation'

  SCREEN_WIDTH = 900
  SCREEN_HEIGHT = 900

  # Center of the screen
  ORIGIN_X = SCREEN_WIDTH / 2
  ORIGIN_Y = SCREEN_HEIGHT / 2

  # Drawing scale factor
  SCALE = 4

  # Offset for the coordinate system used where (0, 0) is in the center of the middle box
  TRUE_X = ORIGIN_X
  TRUE_Y = ORIGIN_Y + (Box.LENGTH / 2) * SCALE 

  # Update functions are called by the MPC to transmit information about the simulation to the display thread
  def update_car(self, car):
    self.car = car

  def update_boxes(self, boxes):
    self.boxes = boxes

  def update_step(self, step):
    self.step = step

  # Draw each box
  def draw_box(self, box):
    pygame.draw.rect(self.screen, box.color, 
      pygame.Rect(
        Display.TRUE_X + box.x * Display.SCALE, 
        Display.TRUE_Y + box.y * Display.SCALE,
        Box.WIDTH * Display.SCALE,
        Box.LENGTH * Display.SCALE
    ))

  def draw_car(self, car):
    # Draw the car
    pygame.draw.polygon(self.screen, (0, 0, 0), 
      (
        car.get_display_coordinates('L1'), 
        car.get_display_coordinates('L2'), 
        car.get_display_coordinates('R2'),
        car.get_display_coordinates('R1')
      )
    )

    # Marker for the center of the car
    pygame.draw.rect(self.screen, (255, 0, 255), 
      pygame.Rect(
        Display.TRUE_X + (car.center_x * Display.SCALE) - 5, 
        Display.TRUE_Y + (car.center_y * Display.SCALE) - 5,
        10,
        10
    ))


  # Draw information about the state of the simulation
  def draw_state(self):
    font = pygame.font.Font('freesansbold.ttf', 16)
    text = font.render(
      f'[Step: {self.step}] Car Center: ({round(self.car.center_x, 3)},{round(self.car.center_y, 3)}), heading_angle: {round(self.car.heading_angle, 3)}, steering_ang: {round(self.car.steering_angle, 3)}, velocity: {round(self.car.velocity, 3)}',
      True, (0, 0, 0))
    self.screen.blit(text, (0, 0))

  # Draw axis
  def draw_grid(self):
    pygame.draw.line(self.screen, (0, 0, 0), ((Display.SCREEN_WIDTH / 2), 0), ((Display.SCREEN_WIDTH / 2), Display.SCREEN_HEIGHT), width=1)
    pygame.draw.line(self.screen, (0, 0, 0), (0, Display.TRUE_Y), (Display.SCREEN_WIDTH, Display.TRUE_Y), width=1)

  def start(self):
    pygame.init()
    pygame.display.set_caption(Display.TITLE)

    self.screen = pygame.display.set_mode([Display.SCREEN_WIDTH, Display.SCREEN_HEIGHT])

    self.running = True
    while self.running:
      time.sleep(0.01)

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.running = False

      self.screen.fill((255, 255, 255))

      # Draw each box
      for i, box in enumerate(self.boxes):
        self.draw_box(box)

      # Draw the car
      if self.car is not None:
        self.draw_car(self.car)
        self.draw_state()

      self.draw_grid()

      # (0,0) marker
      pygame.draw.rect(self.screen, (255, 255, 255), 
        pygame.Rect(
          Display.TRUE_X - 2, 
          Display.TRUE_Y - 2,
          4,
          4
      ))

      pygame.display.flip()

    pygame.quit()

  def __init__(self):
    self.step = 0
    self.car = None
    self.boxes = []

    display_thread = threading.Thread(target=self.start, args=())
    display_thread.start()