import pygame, time, threading, random

from box import Box
from car import Car

class Display:
  """
   Create a visual representation of the MPC controls
  """

  SCREEN_WIDTH = 500
  SCREEN_HEIGHT = 500

  ORIGIN_X = SCREEN_WIDTH / 2
  ORIGIN_Y = SCREEN_HEIGHT / 2

  TRUE_X = ORIGIN_X
  TRUE_Y = ORIGIN_Y + Box.length / 2

  # Drawing scale factor
  SCALE = 3

  BOX_COLOR = (0, 0, 0)

  def update_car(self, car):
    self.car = car

  # Called by MPC
  def update_boxes(self, boxes):
    self.boxes = boxes

  def update_step(self, step):
    self.step = step

  # Draw each box
  def draw_box(self, box):
    pygame.draw.rect(self.screen, box.color, 
      pygame.Rect(
        Display.ORIGIN_X + box.x * Display.SCALE, 
        Display.ORIGIN_Y + box.y * Display.SCALE,
        box.width * Display.SCALE,
        box.length * Display.SCALE
    ))

  # Draw the car
  def draw_car(self, car):
    if self.car_image is None:
      return

    # scaled_image = pygame.transform.scale(self.car_image, (Car.LENGTH * Display.SCALE, Car.WIDTH * Display.SCALE))

    # rotated_image = pygame.transform.rotate(scaled_image, self.car.heading_angle)
    # self.screen.blit(rotated_image, (Display.TRUE_X + car.x * Display.SCALE, Display.TRUE_Y + car.y * Display.SCALE))


    # Draw car actual pos
    pygame.draw.polygon(self.screen, (0, 0, 0), 
      (
        car.get_display_coordinates('L1'), 
        car.get_display_coordinates('L2'), 
        car.get_display_coordinates('R2'),
        car.get_display_coordinates('R1')
      )
    )

    print(    (
        car.get_display_coordinates('L1'), 
        car.get_display_coordinates('L2'), 
        car.get_display_coordinates('R2'),
        car.get_display_coordinates('R1')
      ))

    # Center Marker
    pygame.draw.rect(self.screen, (255, 0, 255), 
      pygame.Rect(
        Display.TRUE_X + (car.center_x * Display.SCALE) - 3, 
        Display.TRUE_Y + (car.center_y * Display.SCALE) - 3,
        6,
        6
    ))


  # Draw information about the state of the simulation
  def draw_state(self):
    font = pygame.font.Font('freesansbold.ttf', 16)
    text = font.render(f'Step: {self.step} (x: {round(self.car.x, 3)}, y: {round(self.car.y, 3)})', True, (0, 0, 0))
    self.screen.blit(text, (0, 0))

  # Should be adapted to allow for going through the steps 1 by 1
  def start(self):
    pygame.init()
    self.screen = pygame.display.set_mode([Display.SCREEN_WIDTH, Display.SCREEN_HEIGHT])
    self.car_image = pygame.image.load('./car-fullsize.png')

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

      # Origin marker
      pygame.draw.rect(self.screen, (0, 0, 0), 
        pygame.Rect(
          Display.ORIGIN_X, 
          Display.ORIGIN_Y,
          2,
          2
      ))

      # True position marker
      pygame.draw.rect(self.screen, (0, 0, 0), 
        pygame.Rect(
          Display.TRUE_X, 
          Display.TRUE_Y,
          2,
          2
      ))

      pygame.display.flip()

    pygame.quit()

  def __init__(self):
    self.step = 0
    self.car = None
    self.boxes = []

    display_thread = threading.Thread(target=self.start, args=())
    display_thread.start()