from AstarClass import *

OBSTACLES_NUM = 100
X = 50 # Rows
Y = 100 # Cols

if __name__ == '__main__':
	# Create empty grid, empty grid is '0'
	g = Grid(X, Y, OBSTACLES_NUM)

	# Add obstacles to the grid, represent it in grid with '1'
	g.random_obstacles()
	
	# Random begin point, represent it in grid with 'B'
	beginx, beginy = g.random_free_loc()
	g.grid[beginx][beginy] = "B"

	# Random end point, represent it in grid with 'E'
	endx, endy = g.random_free_loc()
	g.grid[endx][endy] = "E"

	# Find the path from begin point to end point
	p = PathHandler(beginx, beginy, endx, endy, g.grid, X, Y)
	path = p.find_path()

	if path == None:
		print "Didn't find the path. Sorry"
	else:
		# Draw all the points on the grid
		grid = g.draw_path(path, Point(endx, endy))

	# Print the grid
	g.print_grid()

	# Save grid to image
	g.save_grid_to_img()


