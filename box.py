class Box:
  """
  Boxes representing parking spaces
  """
  LENGTH = 26                  # Box length (cm)
  WIDTH = 60                   # Box width (cm) (was 50, made it a bit bigger)

  def __init__(self, x, y, color):
    self.x = x
    self.y = y
    self.color = color
