import cell_status as cs

class cell:

	def __init__(self, status, clue: int, num_safe: int, num_mine: int, num_hidden: int, loc: (int, int)):
		self._status = status
		self._clue = clue
		self._num_safe = num_safe
		self._num_mine = num_mine
		self._num_hidden = num_hidden
		self.loc = loc

	def get_status(self):
		return self._status

	def set_status(self, new_status):
		if self._status == cs.Cell_Status.COVERED:
			self._status = new_status
			return True
		else:
			return False

	def get_clue(self):
		return self._clue

	def set_clue(self, new_clue):
		if self._clue == None and new_clue >= 0 and new_clue <= 8:
			self._clue = new_clue
			return True
		else:
			return False

	def get_num_safe(self):
		return self._num_safe

	def set_num_safe(self, new_num_safe):
		if new_num_safe > self._num_safe and new_num_safe >= 0 and new_num_safe <= 8:
			self._num_safe = new_num_safe
			return True
		else:
			return False

	def get_num_mine(self):
		return self._num_mine

	def set_num_mine(self, new_num_mine):
		if new_num_mine > self._num_mine and new_num_mine >= 0 and new_num_mine <= 8:
			self._num_mine = new_num_mine
			return True
		else:
			return False

	def get_num_hidden(self):
		return self._num_hidden

	def set_num_hidden(self, new_num_hidden):
		if new_num_hidden < self._num_hidden and new_num_hidden >= 0 and new_num_hidden <= 8:
			self._num_hidden = new_num_hidden
			return True
		else:
			return False