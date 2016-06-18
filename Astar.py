from AstarClass import *

OBSTACLES_NUM = 300
X, Y = 30, 30

if __name__ == '__main__':
	# Create empty grid, empty grid is '0'
	grid = [[0 for x in range(X)] for y in range(Y)]

	# Add obstacles to the grid, represent it in grid with '1'
	grid = random_obstacles(grid, OBSTACLES_NUM, X, Y)
	
	# Random begin point, represent it in grid with 'B'
	beginx, beginy = random_free_loc(grid, X, Y)
	grid[beginx][beginy] = "B"

	# Random end point, represent it in grid with 'E'
	endx, endy = random_free_loc(grid, X, Y)
	grid[endx][endy] = "E"

	# Find the path from begin point to end point
	p = PathHandler(beginx, beginy, endx, endy, grid, X, Y)
	path = p.find_path()

	if path == None:
		print "Didn't find the path. Sorry"
	else:
		# Draw all the points on the grid
		grid = draw_path(grid, path, Point(endx, endy))

	# Print the grid
	print_grid(grid)


