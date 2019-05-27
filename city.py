class City:
	def __init__(self, Id, Name, Long, Lat):
		self.Id = Id
		self.Name = Name
		self.Long = Long
		self.Lat = Lat

	def stringify(self):
		return "{} {} {} {}".format(self.Id, self.Name, self.Long, self.Lat)
