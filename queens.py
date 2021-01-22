from search import *

import sys
import math


class QueensState(object):
	""" 
	The board configuration is composed of:
	queens: list of rows where queen pieces are positioned
	leftdiag: list containing the number of queens in each of the 2n - 1 upleft-to-downright diagonal 
	rightdiag: list containing the number of queens in each of the 2n - 1 upright-to-downleft diagonal 
	The score/energy is one half for each queen under attack
	"""
	def __init__(self, queens, leftdiag, rightdiag, score):
		self.queens = queens
		self.leftdiag = leftdiag
		self.rightdiag = rightdiag
		self.score = score

	def copy(self):
		queens = self.queens[:]
		leftdiag = self.leftdiag[:]
		rightdiag = self.rightdiag[:]
		return QueensState(queens, leftdiag, rightdiag, self.score)
		


class QueensProblem(Problem):
	def __init__(self, n):
		self.n = n


	def make_initial_state(self):
		""" 
		The initial board configuration is always the same: the queens are positioned on the board's main diagonal 
		leftdiag and rightdiag are initialized accordingly
		"""
		queens = [i for i in range(self.n)]
		leftdiag = [0 for i in range(2*self.n - 1)]
		rightdiag = [0 for i in range(2*self.n - 1)]
		for i in range(self.n):
			leftdiag[self.n - 1 - i + queens[i]] += 1
			rightdiag[i + queens[i]] += 1
		# On the main diagonal there are n-1 more queens than the maximum allowed (1)
		score = self.n - 1
		return QueensState(queens, leftdiag, rightdiag, score)

	
	def random_action(self, state):
		""" Return the indexes of the queens to be swapped """
		return random.sample(range(self.n), 2)


	def inverse_action(self, action):
		return [action[1], action[0]]


	def queens_enter_the_diag(self, diag, i):
		""" 
		Given the fact that a queen has entered the i-th diagonal (the diagonals are specified by diag), 
		return 1 if this move increases the number of queens that can be attacked by 2, 0 otherwise
		"""
		diag[i] += 1
		if diag[i] > 1:
			return 1
		else:
			return 0


	def queens_exit_the_diag(self, diag, i):
		""" 
		Given the fact that a queen has exited the i-th diagonal (the diagonals are specified by diag), 
		return 0 if this diagonal was not containing any attacked queens (i.e. there was just one queen), -1 otherwise 
		(by removing the queen, the number of remaining queens that can attacked inevitably drops by two)
		"""
		diag[i] -= 1
		return -1 if diag[i] > 0 else 0
	

	def result(self, state, action):
		i, j = action
		new_state = state
		new_state.queens[i], new_state.queens[j] = new_state.queens[j], new_state.queens[i]
		new_state.score += self.queens_exit_the_diag(new_state.leftdiag, self.n - 1 - i + new_state.queens[j])
		new_state.score += self.queens_enter_the_diag(new_state.leftdiag, self.n - 1 - i + new_state.queens[i])
		new_state.score += self.queens_exit_the_diag(new_state.leftdiag, self.n - 1 - j + new_state.queens[i])
		new_state.score += self.queens_enter_the_diag(new_state.leftdiag, self.n - 1 - j + new_state.queens[j])
		new_state.score += self.queens_exit_the_diag(new_state.rightdiag, i + new_state.queens[j])
		new_state.score += self.queens_enter_the_diag(new_state.rightdiag, i + new_state.queens[i])
		new_state.score += self.queens_exit_the_diag(new_state.rightdiag, j + new_state.queens[i])
		new_state.score += self.queens_enter_the_diag(new_state.rightdiag, j + new_state.queens[j])
		return new_state


	def score(self, state):
		return state.score


	def goal(self, state):
		return self.score(state) == 0



def print_solution(solution):
	if len(solution.queens) <= 10:	
		print("Solution is: ")
		print(", ".join([str(queen+1) for queen in solution.queens]))
	print("The position in the sequence corresponds to the queen's column, the value to the row")
	print("Full board representation will be saved into queens.out")
	n = len(solution.queens)
	with open("queens.out", 'w') as f:
		f.write("+")
		f.write("-+" * n + '\n')
		for queen in solution.queens:
			f.write("|")
			f.write(" |" * queen)
			f.write("Q|")
			f.write(" |" * (n - queen - 1) + '\n')
			f.write("+")
			f.write("-+" * n + '\n')
			
	

def solve(n, schedule, maxiter):
	problem = QueensProblem(n)
	solution, stats, halted = simulated_annealing(problem, schedule, maxiter)
	score = problem.score(solution)
	if len(solution.queens) < 100:
		print_solution(solution)
	print("Score (number of attacked queens in each diagonal, 0 meaning solution): {}".format(score))
	print_stats(stats)
