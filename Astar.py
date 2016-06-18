from AstarClass import *

OBSTACLES_NUM = 300
X, Y = 30, 30

if __name__ == '__main__':
	# Create empty grid
	grid = [[0 for x in range(X)] for y in range(Y)]

	# Add obstacles in grid
	grid = random_obstacles(grid, OBSTACLES_NUM, X, Y)
	
	# Random begin point
	beginx, beginy = random_free_loc(grid, X, Y)
	grid[beginx][beginy] = "B"

	# Random end point
	endx, endy = random_free_loc(grid, X, Y)
	grid[endx][endy] = "E"

	p = PathHandler(beginx, beginy, endx, endy, grid, X, Y)

	path = p.find_path()

	grid = draw_path(grid, path, Point(endx, endy))

	print_grid(grid)
