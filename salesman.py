from search import *

import sys
import random

import os.path


class TravellingSalesmanState(object):
	def __init__(self, path, score):
		self.path = path
		self.score = score


	def copy(self):
		path = self.path.copy()
		return TravellingSalesmanState(path, self.score)


class TravellingSalesmanProblem(Problem):
	def __init__(self, points, distance):
		""" points: graph vertexes, distance: function that computes the distance between two functions """
		self.points = points
		self.n = len(points)
		self.distance = distance


	def points_distance(self, i, j):
		""" Computes the distance between points[i] and points[j] """
		return self.distance(self.points[i], self.points[j])

	def make_initial_state(self):
		""" Initial state is always the same: the points in order of appaerance, followed by a copy of the first point (redundant, but much easier implementation) """
		path = [i for i in range(self.n)]
		path.append(0)
		score = sum([self.points_distance(path[i], path[i+1]) for i in range(self.n)])
		return TravellingSalesmanState(path, score)

	
	def random_action(self, state):
		""" Return two distinct points to be swapped places (the cannot be the first of the path) """
		return random.sample(range(1, self.n), 2)

	
	def result(self, state, action):
		a, b = action

		new_state = state.copy()
		new_state.path[a], new_state.path[b] = new_state.path[b], new_state.path[a]

		# This edge cases must be accounted for so that each is considered only one time
		if a - 1 == b:
			new_state.score += self.points_distance(new_state.path[a], new_state.path[a+1]) - self.points_distance(state.path[a], state.path[a+1])
			new_state.score += self.points_distance(new_state.path[b-1], new_state.path[b]) - self.points_distance(state.path[b-1], state.path[b])
		elif a + 1 == b:
			new_state.score += self.points_distance(new_state.path[a-1], new_state.path[a]) - self.points_distance(state.path[a-1], state.path[a])
			new_state.score += self.points_distance(new_state.path[b], new_state.path[b+1]) - self.points_distance(state.path[b], state.path[b+1])
		else:
			new_state.score += self.points_distance(new_state.path[a], new_state.path[a+1]) - self.points_distance(state.path[a], state.path[a+1])
			new_state.score += self.points_distance(new_state.path[b-1], new_state.path[b]) - self.points_distance(state.path[b-1], state.path[b])
			new_state.score += self.points_distance(new_state.path[a-1], new_state.path[a]) - self.points_distance(state.path[a-1], state.path[a])
			new_state.score += self.points_distance(new_state.path[b], new_state.path[b+1]) - self.points_distance(state.path[b], state.path[b+1])

		return new_state


	def score(self, state):
		return state.score
	

def parse_graph_file(filename):
	""" Given the filename of a .graph file, returns the points' coordinates listed in it """
	if not os.path.exists(filename) or not os.path.isfile(filename):
		return None
	points = []
	for line in open(filename, "r"):
		if line == "":
			continue
		tokens = line.split(',')
		if len(tokens) < 2:
			return None
		try:
			x = float(tokens[0])
			y = float(tokens[1])
			points.append((x, y))
		except:
			return None
	return points


def print_solution(path):
	path = [str(it) for it in path]
	print("Solution is: ")
	print(" -> ".join(path))

		
def solve(points, schedule, maxiter):
	euclid_distance = lambda a, b: math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
	problem = TravellingSalesmanProblem(points, euclid_distance)

	solution, stats, halted = simulated_annealing(problem, schedule, maxiter)

	path_length = problem.score(solution)
	print_solution(solution.path)

	print("Path length is {}".format(path_length))
	print_stats(stats)
