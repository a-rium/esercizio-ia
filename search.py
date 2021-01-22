import random
import math
import signal


class Problem(object):
	def make_initial_state(self):
		pass

	def random_action(self, state):
		pass

	def inverse_action(self, action):
		pass

	def result(self, state, action):
		pass
	
	def score(self, score):
		pass
		

Halted = False
	
def stop(signum, frame):
	global Halted
	Halted = True


def print_stats(stats):
	print("Simulated annealing execution's statistics: ")
	for (key, value) in stats.items():
		print("{}: {}".format(key, value))

	
def simulated_annealing(problem, schedule, maxiter=0):
	# Installing a CTRL-C handler so that when the user press it the annealing process will stop
	old_sigint_handler = signal.signal(signal.SIGINT, stop)
	
	state = problem.make_initial_state()
	score = problem.score(state)
	# Statistics about the method execution
	stats = {"Good swaps": 0, "Random swaps": 0, "Local optimum reached since": 0}

	t = 0
	while not Halted:
		t += 1
		temperature = schedule(t)
		if temperature <= 0:
			break
		action = problem.random_action(state)
		new_state = problem.result(state, action)
		new_score = problem.score(new_state)
		gain = new_score - score
		if gain < 0:
			state = new_state
			score = new_score
			stats["Good swaps"] += 1
			stats["Local optimum reached since"] = t
		else:
			p = math.exp(-gain / temperature)
			if random.random() < p:
				state = new_state
				score = new_score
				stats["Random swaps"] += 1
				if gain > 0:
					stats["Local optimum reached since"] = t
			else:
				action = problem.inverse_action(action)
				state = problem.result(new_state, action)
		if t == maxiter:
			break


	stats["Iterations"] = t
	stats["Final temperature"] = temperature

	signal.signal(signal.SIGINT, old_sigint_handler)

	return state, stats, Halted


# Schedules

class LogSchedule(object):
	def __init__(self, initial_temperature, sigma):
		self.initial_temperature = initial_temperature
		self.sigma = sigma

	
	def __call__(self, t):
		return self.initial_temperature / math.log2(t + self.sigma)


class LinearSchedule(object):
	def __init__(self, initial_temperature, c):
		self.initial_temperature = initial_temperature
		self.c = c

	
	def __call__(self, t):
		return self.initial_temperature - t * self.c


class GeometricSchedule(object):
	def __init__(self, initial_temperature, alpha):
		self.temperature = initial_temperature
		self.alpha = alpha


	def __call__(self, t):
		current = self.temperature
		self.temperature *= self.alpha
		return current
