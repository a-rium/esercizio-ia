from search import *

import sys
import math
import random


class MagicSquareState(object):
	""" The state must store the square configuration, the rows' sums, the columns' sums and the diagonal sums """
	def __init__(self, square, rows, cols, leftdiag, rightdiag, score):
		self.square = square
		self.rows = rows
		self.cols = cols
		self.leftdiag = leftdiag
		self.rightdiag = rightdiag
		self.score = score


	def copy(self):
		square = self.square[:]
		rows = self.rows[:]
		cols = self.cols[:]
		return MagicSquareState(square, rows, cols, self.leftdiag, self.rightdiag, self.score)
		


class MagicSquareProblem(Problem):
	def __init__(self, n):
		self.n = n
		self.magic = n * (n**2 + 1) // 2


	def make_initial_state(self):
		""" 
		The initial square configuration is the following:
		
		1	2	...	n
		n+1	n+2	...	2n
		.
		.
		.
		n^2-n+1	n^2-n+2	...	n^2
		
		"""
		square = [i for i in range(1, self.n**2 + 1)]	
		# Sums are set accordingly
		rows = [sum(square[i*self.n:i*self.n+self.n]) for i in range(self.n)]
		cols = [0 for i in range(self.n)]
		for i in range(self.n):
			cols[i] += sum([square[(j*self.n + i)] for j in range(self.n)])
		leftdiag = sum([square[(i * self.n + i)] for i in range(self.n)])
		rightdiag = sum([square[(i * self.n + (self.n - 1 - i))] for i in range(self.n)])
		score = sum([abs(self.magic - rows[i]) for i in range(self.n)])
		score += sum([abs(self.magic - cols[i]) for i in range(self.n)])
		score += abs(self.magic - leftdiag)
		score += abs(self.magic - rightdiag)
		return MagicSquareState(square, rows, cols, leftdiag, rightdiag, score)

	
	def random_action(self, state):
		""" Action is a couple of distinct indexes corresponding to the two cells to be swapped """ 
		return random.sample(range(0, self.n**2), 2)


	def inverse_action(self, action):
		return [action[1], action[0]]


	def result(self, state, action):
		a, b = action
		ar, ac = a // self.n, a % self.n
		br, bc = b // self.n, b % self.n

		an = state.square[a]
		bn = state.square[b]
		diff = an - bn

		new_state = state
		new_state.square[a], new_state.square[b] = state.square[b], state.square[a]

		new_state.score -= abs(self.magic - new_state.rows[ar])
		new_state.rows[ar] -= diff
		new_state.score += abs(self.magic - new_state.rows[ar])
		new_state.score -= abs(self.magic - new_state.cols[ac])
		new_state.cols[ac] -= diff
		new_state.score += abs(self.magic - new_state.cols[ac])
		new_state.score -= abs(self.magic - new_state.rows[br])
		new_state.rows[br] += diff
		new_state.score += abs(self.magic - new_state.rows[br])
		new_state.score -= abs(self.magic - new_state.cols[bc])
		new_state.cols[bc] += diff
		new_state.score += abs(self.magic - new_state.cols[bc])

		new_state.score -= abs(self.magic - new_state.leftdiag)
		if ar == ac:
			new_state.leftdiag -= diff
		if br == bc:
			new_state.leftdiag += diff
		new_state.score += abs(self.magic - new_state.leftdiag)

		new_state.score -= abs(self.magic - new_state.rightdiag)
		if ar == self.n - 1 - ac:
			new_state.rightdiag -= diff
		if br == self.n - 1 - bc:
			new_state.rightdiag += diff
		new_state.score += abs(self.magic - new_state.rightdiag)

		return new_state

	
	def score(self, state):
		return state.score


	def goal(self, state):
		return self.score(state) == 0


def print_solution(solution):
	def print_row_separator(write, ncols, colswidth):
		write("+")
		for i in range(ncols):
			write("-" * colswidth + "+")
		write("\n")
		

	print("Proposed solution's board representation will be saved into magic.out")

	nsquared = len(solution.square)
	n = round(math.sqrt(nsquared))
	digits = math.floor(math.log(max(solution.cols), 10)) + 1
	entry_fmt = "{:>" + str(digits) + "}"
	with open("magic.out", 'w') as f:
		f.write(" ")
		for i in range(n):
			f.write(" " * (digits + 1))
		f.write(" {}\n".format(solution.rightdiag))
		print_row_separator(f.write, n, digits)
		for row in range(n):
			f.write("|")
			for col in range(n):
				idx = row*n + col
				f.write(entry_fmt.format(solution.square[idx]) + "|")
			f.write(" {}\n".format(solution.rows[row]))
			print_row_separator(f.write, n, digits)
		f.write("\n")
		f.write(" ")
		for s in solution.cols:
			f.write(entry_fmt.format(str(s) + " "))
		f.write(" {}".format(solution.leftdiag))


def solve(n, schedule, maxiter):
	problem = MagicSquareProblem(n)

	solution, stats, halted = simulated_annealing(problem, schedule, maxiter)
	score = problem.score(solution)
	if n < 15:
		print_solution(solution)
	print("Score (sum of the absolute difference between the sums and the magic number, 0 meaning solution): {}".format(score))
	print_stats(stats)
