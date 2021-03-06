import Queue as Q
import math
import random
import Image

IMG_OUTPUT = "output.png"

IMG_MAP = {
	"0" : (255, 255, 255), #empty, white
	"*" : (255, 0, 0), #path, red
	"1" : (0, 0, 0), #obstacles, black
	"B" : (0, 255, 0), #begin green
	"E" : (0, 0, 255) #end blue
}

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
	def __init__(self, x, y, endx, endy, move_cost=0):
		self.x = x
		self.y = y
		self.endx = endx
		self.endy = endy

		# Distance from this node to  the target node
		# Also known as h() value
		self.heuristic = self._calc_h()

		# Movement cost from node to another node
		# Also known as g() value
		self.move_cost = move_cost

		# The f() value, combination of heuristic and move values
		# f() = h() + g()
		self.priority = 0

		# The parent node, the node before this node in the path
		self.parent = 0

	def __str__(self):
		return "Node (x=%d, y=%d, heuristic=%d, move_cost=%d, priority=%d)" % \
			   (self.x, self.y, self.move_cost, self.heuristic, self.priority)

	def __cmp__(self, other):
		if other == None or \
			not isinstance(other, Node):
			return 1
		return cmp(self.priority, other.priority)

	def _calc_h(self):
		xd = self.x - self.endx
		yd = self.y - self.endy
		dist = math.fabs(xd) + math.fabs(yd)

		return dist

	def set_parent(self, node_parent):
		self.parent = node_parent

	def update_priority(self):
		self.priority = self.move_cost + self.heuristic

	def update_move_cost(self, curr_dir):
		self.move_cost += 10 if (curr_dir % 2 == 0) else 14

class PathHandler():
	# All directions arround node with points deltas
	DIR = [Point(1, 0), Point(1, 1), Point(0, 1), Point(-1, 1), Point(-1, 0), Point(-1, -1), Point(0, -1), Point(1, -1)]

	def __init__(self, beginx, beginy, endx, endy, grid, X, Y):
		self.beginx = beginx
		self.beginy = beginy
		self.endx = endx
		self.endy = endy
		self.grid = grid
		self.X = X
		self.Y = Y

		# Keep the open nodes in priority queue,
		# the node with the *lowest* priority will be the first one
		self.open_list = Q.PriorityQueue()

		# Keep the already visited nodes in list
		self.close_list = []

	def _contains(self, l, filter):
		"""Check is list contains element with filter"""
		for x in l:
			if filter(x):
				return True
		return False

	def _contains_node(self, l, x, y):
		"""Check is list contains node according to its location"""
		return self._contains(l, lambda node: node.x == x and node.y == y)

	def _get(self, l, filter):
		"""Get first element and index from list if was found"""
		for i, x in enumerate(l):
			if filter(x):
				return i, x
		return None, None

	def _get_node(self, l, x, y):
		"""Get first node and index from list if was found"""
		return self._get(l, lambda node: node.x == x and node.y == y)

	def _search_around(self):
		"""Search arround current node for new nodes in all directions,
		or better nodes (according to priority) than we already found"""
		for i in range(len(self.DIR)):
			xd = self.currNode.x + self.DIR[i].x
			yd = self.currNode.y + self.DIR[i].y

			# If this point is valid (in borders), and not occupied by something
			# and it is not in close list
			if self._is_valid_point(Point(xd, yd)) and \
					is_free(self.grid[xd][yd]) and \
					not self._contains_node(self.close_list, xd, yd):

				# Create new node with current node move cost and priority
				newNode = Node(xd, yd, self.endx, self.endy, self.currNode.move_cost)
				# Update move cost
				newNode.update_move_cost(i)
				# Update priority
				newNode.update_priority()

				# If new node is not in open list, add it to open list
				# and make the current node its parent
				if not self._contains_node(self.open_list.queue, xd, yd):
					self.open_list.put(newNode)
					newNode.parent = self.currNode
				else:
					# If it is already in open list, and the new node's priority is lower
					# than the exists one, replace the nodes
					indexNode, existsNode = self._get_node(self.open_list.queue, xd, yd)
					if existsNode.priority > newNode.priority:
						# I replace the nodes and not changing the exists node, 
						# because the priority queue
						#  will not be updated after this changing

						# Remove existsNode (directly in the queue attribute which is a list object)
						del self.open_list.queue[indexNode]

						# Put newNode
						self.open_list.put(newNode)

	def _is_close_to_end(self):
		"""Chech is current node is close one step to the end"""
		for d in self.DIR:
			if self.currNode.x + d.x == self.endx and \
				self.currNode.y + d.y == self.endy:
				return True

		return False

	def _return_path(self):
		path = []

		while self.currNode.parent != 0:
			path.append(Point(self.currNode.x, self.currNode.y))
			self.currNode = self.currNode.parent

		path.reverse()
		return path

	def _is_valid_point(self, point):
		return point.x >= 0 and \
				point.x < self.X and \
				point.y >= 0 and \
				point.y < self.Y

	def find_path(self):
		"""Find the path from begin point to end point
		:return list of Points from begin to end"""

		# Set the start node
		startNode = Node(self.beginx, self.beginy, self.endx, self.endy)
		startNode.update_priority()

		# Put the start node in open_list queue
		self.open_list.put(startNode)

		# While there is still one node in queue,
		# means we didn't finish to check all points in the grid
		while not self.open_list.empty():
			# Get the lowest priority node from queue
			self.currNode = self.open_list.get()

			# Check is current node is one step close to end point
			if self._is_close_to_end():
				# Add endpoint and make its parent the current node
				endPoint = Node(self.endx, self.endy, self.endx, self.endx)
				endPoint.parent = self.currNode
				self.currNode = endPoint

				# Return the full path from begin to end
				return self._return_path()

			# Search for points arround the current node
			self._search_around()

			# Add current node to close list (done)
			self.close_list.append(self.currNode)

		# We didn't found any path,
		# the path appears to be blocked by obstacles
		# return None
		return None

class Grid:
	def __init__(self, X, Y, obs_num):
		self.X = X
		self.Y = Y
		self.obs_num = obs_num
		self.grid = self._initiaize_grid()

	def _initiaize_grid(self):
		grid = [[0 for y in range(self.Y)] for x in range(self.X)]
		return grid

	def rand_x(self):
		return random.randint(0, self.X - 1)

	def rand_y(self):
		return random.randint(0, self.Y - 1)

	def random_free_loc(self):
		while True:
			x, y = self.rand_x(), self.rand_y()
			if is_free(self.grid[x][y]):
				return x, y

	def print_grid(self):
		print '\n'.join([''.join(['{:1}   '.format(item) for item in row]) \
      		for row in self.grid])
	
	def random_obstacles(self):
		for i in range(self.obs_num):
			randx, randy = self.random_free_loc()
			self.grid[randx][randy] = 1


	def draw_path(self, path, end):
		for p in path:
			if p != end:
				self.grid[p.x][p.y] = "*"

	def save_grid_to_img(self):
		im = Image.new('RGB', (self.Y, self.X) )
		pixels = im.load()

		for y in range(self.Y):
			for x in range(self.X):
				val = str(self.grid[x][y])
				pixels[y, x] = IMG_MAP[val]

		im.save(IMG_OUTPUT)


def is_free(val):
	return val == 0
