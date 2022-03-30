import pygame
import astar

WIDTH = 700
window = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('Pathfinding Visualiser')

RED = (255,0,0)
ORANGE = (255, 165, 0)
DARK_BLUE = (0, 0, 255)
GREEN = (0, 128, 0)
AQUA = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def main(window, width):
	ROWS = 50
	grid = create_grid(ROWS, width)

	start = None
	end = None

	run = True
	while run:

		draw(window, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, column = get_selected_node(pos, ROWS, width)
				node = grid[row][column]
				if not start and node != end:
					start = node
					start.set_start()

				elif not end and node != start:
					end = node
					end.set_end()

				elif node != end and node != start:
					node.set_barrier()

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, column = get_selected_node(pos, ROWS, width)
				node = grid[row][column]
				node.reset()
				if node == start:
					start = None
				elif node == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for node in row:
							node.update_neighbors(grid)

					astar.astar_alg(lambda: draw(window, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = create_grid(ROWS, width)

				if event.key == pygame.K_ESCAPE:
					run = False

	pygame.quit()


class Node:
	def __init__(self, row, column, width, rows):
		self.row = row
		self.column = column
		self.x = row * width
		self.y = column * width
		self.colour = WHITE
		self.neighbors = []
		self.width = width
		self.rows = rows

	def position(self):
		return self.row, self.column

	def is_closed(self):
		return self.colour == RED

	def is_open(self):
		return self.colour == GREEN

	def is_barrier(self):
		return self.colour == BLACK

	def is_start(self):
		return self.colour == ORANGE

	def is_end(self):
		return self.colour == DARK_BLUE


	def reset(self):
		self.colour = WHITE

	def set_start(self):
		self.colour = ORANGE

	def set_closed(self):
		self.colour = RED

	def set_open(self):
		self.colour = GREEN

	def set_barrier(self):
		self.colour = BLACK

	def set_end(self):
		self.colour = DARK_BLUE

	def set_path(self):
		self.colour = AQUA

	def draw(self, window):
		pygame.draw.rect(window, self.colour, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []
        # check if downward move is possible
		if self.row < self.rows - 1 and not grid[self.row + 1][self.column].is_barrier():
			self.neighbors.append(grid[self.row + 1][self.column])
        # check if upward move is possible
		if self.row > 0 and not grid[self.row - 1][self.column].is_barrier():
			self.neighbors.append(grid[self.row - 1][self.column])
        # check if rightward move is possible
		if self.column < self.rows - 1 and not grid[self.row][self.column + 1].is_barrier():
			self.neighbors.append(grid[self.row][self.column + 1])
        # check if leftward move is possible
		if self.column > 0 and not grid[self.row][self.column - 1].is_barrier():
			self.neighbors.append(grid[self.row][self.column - 1])

	def __lt__(self, other):
		return False

def create_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			node = Node(i, j, gap, rows)
			grid[i].append(node)

	return grid

def create_dist_grid(rows, width):
	dist_grid = []
	gap = width // rows
	for i in range(rows):
		dist_grid.append([])
		for j in range(rows):
			node = Node(i, j, gap, rows)
			dist_grid[i].append(node)

	return dist_grid

def create_prev_grid(rows, width):
	prev_grid = []
	gap = width // rows
	for i in range(rows):
		prev_grid.append([])
		for j in range(rows):
			node = Node(i, j, gap, rows)
			prev_grid[i].append(node)

	return prev_grid


def draw_grid(window, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(window, BLACK, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(window, BLACK, (j * gap, 0), (j * gap, width))


def draw(window, grid, rows, width):
	window.fill(WHITE)

	for row in grid:
		for node in row:
			node.draw(window)

	draw_grid(window, rows, width)
	pygame.display.update()


def get_selected_node(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	column = x // gap

	return row, column

main(window, WIDTH)
