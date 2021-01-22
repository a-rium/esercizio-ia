from search import *
import queens
import magic
import salesman

import os.path

from timeit import default_timer as timer


def input_cast(cast, prompt, default=None):
	while True:
		result = input(prompt)
		if result == "" and default is not None:
			result = default
			break
		else:
			try:
				result = cast(result)
				break
			except:
				pass
	print()
	return result


def nqueens_dialog():
	print("You selected the n-Queens problem")
	print("This problem admit solutions for integer n greater or equal to 4")
	print()
	while True:
		n = input_cast(int, "Please insert your pick for n: ")
		if n > 3:
			return {"n": n}


def magic_square_dialog():
	print("You selected the Magic Square problem")
	print("Let n be the side of the magic square to search for")
	print("This problem admit solutions for integer n greater or equal to 3")
	print()
	while True:
		n = input_cast(int, "Please insert your pick for n: ")
		if n > 2:
			return {"n": n}


def travelling_salesman_dialog():
	print("You selected the Travelling Salesman problem")
	print("Please insert the *.graph filename contained into the data subfolder")
	print()
	while True:
		filename = input("Filename: ")
		points = salesman.parse_graph_file(os.path.join("data", filename))
		if points is not None:
			return {"points": points}


def log_schedule_dialog():
	print("You selected the Log schedule")
	print("This schedule controls the temperature as given by the following rule:")
	print("T(t) = t0 / log2(t + alpha)")
	default_t0 = 1
	print("Initial temperature t0 must be greater than 0 (default is {})".format(default_t0))
	print()
	while True:
		t0 = input_cast(float, "Please insert your pick for t0: ", default_t0)
		if t0 > 0:
			break

	default_sigma = 1
	print("Speedup factor sigma must be greater than 0 (default is {})".format(default_sigma))
	print()
	while True:
		sigma = input_cast(float, "Please insert your pick for sigma: ", default_sigma)
		if sigma > 0:
			break
	
	return LogSchedule(t0, sigma)


def geometric_schedule_dialog():
	print("You selected the Geometric schedule")
	print("This schedule controls the temperature as given by the following rule:")
	print("T(t) = alpha^t t0")
	default_t0 = 10
	print("Initial temperature t0 must be greater than 0 (default is {})".format(default_t0))
	print()
	while True:
		t0 = input_cast(float, "Please insert your pick for t0: ", default_t0)
		if t0 > 0:
			break

	default_alpha = 0.99
	print("Geometric factor alpha must be in between 0 and 1 (default is {})".format(default_alpha))
	print()
	while True:
		alpha = input_cast(float, "Please insert your pick for alpha: ", default_alpha)
		if alpha > 0 and alpha < 1:
			break
	
	return GeometricSchedule(t0, alpha)


def linear_schedule_dialog():
	print("You selected the Linear schedule")
	print("This schedule controls the temperature as given by the following rule:")
	print("T(t) = t0 - ct")
	default_t0 = 5
	print("Initial temperature t0 must be greater than 0 (default is {})".format(default_t0))
	print()
	while True:
		t0 = input_cast(float, "Please insert your pick for t0: ", default_t0)
		if t0 > 0:
			break

	default_c = 10e-6
	print("Linear factor c must be greater than 0 (default is {})".format(default_c))
	print()
	while True:
		c = input_cast(float, "Please insert your pick for c: ", default_c)
		if c > 0:
			break
	
	return LinearSchedule(t0, c)


def schedule_dialog():
	print("Type the number next to the desired schedule and press <Enter> to use it")
	print("(1) Log schedule (slowest, finds the best solution)")
	print("(2) Geometric schedule (fastest, solution may be far from optimal)")
	print("(3) Linear schedule (faster than log, slower than the geometric)")
	dialog = [log_schedule_dialog, geometric_schedule_dialog, linear_schedule_dialog]
	print()
	while True:
		pick = input_cast(int, "Your pick: ")
		if pick > 0 and pick < 4:
			return dialog[pick-1]()	


def main():
	print()
	print("Type the number next to the problem name and press <Enter> to solve it with the simulated annealing technique")
	print("(1) n-Queens")
	print("(2) Magic Square")
	print("(3) Travelling Salesman")

	dialog = [nqueens_dialog, magic_square_dialog, travelling_salesman_dialog]
	solve_problem = [queens.solve, magic.solve, salesman.solve]
	print()
	while True:
		pick = input_cast(int, "Your pick: ")
		if pick > 0 and pick < 4:
			break

	problem_args = dialog[pick-1]()	
	problem_args["schedule"] = schedule_dialog()
	print("Please insert the maximum amount of iterations allowed (0 means no cap)")
	print()
	while True:
		maxiter = input_cast(int, "Your pick: ")
		if maxiter >= 0:
			break
	problem_args["maxiter"] = maxiter

	print("Solving.... Press CTRL-C anytime to stop the execution")
	start = timer()
	solve_problem[pick-1](**problem_args)
	end = timer()
	print()
	print("Search took {:.6} seconds".format(end-start))


if __name__ == "__main__":
	main()
