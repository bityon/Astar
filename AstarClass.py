import Queue as Q
import math
import random

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __eq__(self, other):
		if other == None or \
			not isinstance(other, Point):
			return False
		return self.x == other.x and self.y == other.y

	def __ne__(self, other):
		return not self.__eq__(other)

class Node():
	def __init__(self, x, y, endx, endy, level=0, priority=0):
		self.x = x
		self.y = y
		self.level = level
		self.endx = endx
		self.endy = endy
		self.dist = self.calc_dist()
		self.priority = priority
		self.parent = 0

	def __str__(self):
		return "Node (x=%d, y=%d, level=%d, dist=%d, priority=%d)" % (self.x, self.y, self.level, self.dist, self.priority)

	def calc_dist(self):
		xd = self.x - self.endx
		yd = self.y - self.endy
		dist = math.fabs(xd) + math.fabs(yd)

		return dist

	def set_parent(self, node_parent):
		self.parent = node_parent

	def update_priority(self):
		self.priority = self.level + self.dist

	def next_level(self, curr_dir):
		self.level += 10 if (curr_dir % 2 == 0) else 14

	def __cmp__(self, other):
		if other == None or \
			not isinstance(other, Node):
			return 1
		return cmp(self.priority, other.priority)

class PathHandler():
	def __init__(self, beginx, beginy, endx, endy, grid, X, Y):
		self.beginx = beginx
		self.beginy = beginy
		self.endx = endx
		self.endy = endy
		self.grid = grid
		self.open_list = Q.PriorityQueue()
		self.close_list = []
		self.X = X
		self.Y = Y

	def contains(self, l, filter):
		for x in l:
			if filter(x):
				return True
		return False

	def contains_node(self, l, x, y):
		return self.contains(l, lambda node: node.x == x and node.y == y)

	def get(self, l, filter):
		for i, x in enumerate(l):
			if filter(x):
				return i, x
		return None, None

	def get_node(self, l, x, y):
		return self.get(l, lambda node: node.x == x and node.y == y)

	def search_around(self):
		for i in range(len(DIR)):
			xd = self.currNode.x + DIR[i].x
			yd = self.currNode.y + DIR[i].y

			if self.is_valid_point(Point(xd, yd)) and \
					is_free(self.grid[xd][yd]) and \
					not self.contains_node(self.close_list, xd, yd):

				newNode = Node(xd, yd, self.endx, self.endy, self.currNode.level,
					self.currNode.priority)
				newNode.next_level(i)
				newNode.update_priority()

				if not self.contains_node(self.open_list.queue, xd, yd):
					self.open_list.put(newNode)
					newNode.parent = self.currNode
				else:
					indexNode, existsNode = self.get_node(self.open_list.queue, xd, yd)
					if existsNode.priority > newNode.priority:
						# Remove existsNode
						del self.open_list.queue[indexNode]

						# Put newNode
						self.open_list.put(newNode)

	def is_close_to_end(self):
		for d in DIR:
			if self.currNode.x + d.x == self.endx and \
				self.currNode.y + d.y == self.endy:
				return True

		return False

	def find_path(self):
		startNode = Node(self.beginx, self.beginy, self.endx, self.endy)
		startNode.update_priority()

		self.open_list.put(startNode)

		while not self.open_list.empty():
			self.currNode = self.open_list.get()

			# Check is current node is one step close to end point
			if self.is_close_to_end():
				endPoint = Node(self.endx, self.endy, self.endx, self.endx)
				endPoint.parent = self.currNode
				self.currNode = endPoint

				return self.return_path()

			self.search_around()

			self.close_list.append(self.currNode)

		return []

	def return_path(self):
		path = []

		while self.currNode.parent != 0:
			path.append(Point(self.currNode.x, self.currNode.y))
			self.currNode = self.currNode.parent

		return path

	def is_valid_point(self, point):
		return point.x >= 0 and \
				point.x < self.X and \
				point.y >= 0 and \
				point.y < self.Y

def is_free(val):
		return val == 0

def random_obstacles(grid, obs_num, X, Y):
	for i in range(obs_num):
		randx, randy = random_free_loc(grid, X, Y)
		grid[randx][randy] = 1

	return grid

def rand_x(X):
	return random.randint(0, X - 1)

def rand_y(Y):
	return random.randint(0, Y - 1)

def random_free_loc(grid, X, Y):
	while True:
		x, y = rand_x(X), rand_y(Y)
		if is_free(grid[x][y]):
			return x, y

def print_grid(grid):
	print '\n'.join([''.join(['{:1}  '.format(item) for item in row])
      for row in grid])

def draw_path(grid, path, end):
	for p in path:
		if p != end:
			grid[p.x][p.y] = "*"

	return grid


DIR = [Point(1, 0), Point(1, 1), Point(0, 1), Point(-1, 1), Point(-1, 0), Point(-1, -1), Point(0, -1), Point(1, -1)]