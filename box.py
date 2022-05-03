class Box:
  """
  Boxes representing parking spaces
  """
  LENGTH = 24                  # Box length (cm)
  WIDTH = 50                   # Box width (cm)

  def __init__(self, x, y, color):
    self.x = x
    self.y = y
    self.color = color
