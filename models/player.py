class Player:
  def __init__(self,name, age, overall):
    self.name = name
    self.age = age
    self.overall = overall
    
  def __str__(self):
    return f"Player: {self.name} | Age: {self.age} | Overall {self.overall}"
    
  def increase_overall(self, num):
    self.overall += num