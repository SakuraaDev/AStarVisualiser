import pygame
from queue import PriorityQueue

def construct(prev_node, current, draw):
	while current in prev_node:
		current = prev_node[current]
		current.set_path()
		draw()

def manhattan(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

def astar_alg(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	prev_node = {}
	gs = {node: float('inf') for row in grid for node in row}
	gs[start] = 0
	fs = {node: float('inf') for row in grid for node in row}
	fs[start] = manhattan(start.position(), end.position())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			construct(prev_node, end, draw)
			end.set_end()
			return True

		for neighbor in current.neighbors:
			temp_gs = gs[current] + 1

			if temp_gs < gs[neighbor]:
				prev_node[neighbor] = current
				gs[neighbor] = temp_gs
				fs[neighbor] = temp_gs + manhattan(neighbor.position(), end.position())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((fs[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.set_open()

		draw()

		if current != start:
			current.set_closed()

	return False