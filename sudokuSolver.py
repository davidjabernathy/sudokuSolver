from random import randint, uniform
from copy import deepcopy
from scipy import sqrt, mean

'''
cross isn't working correctly
given values shouldn't change during cross 
make array of changable numbers
'''
			  #0 1 2 3  4 5 6 7  
START_BOARD = [1,0,0,3, 0,0,1,0, 0,2,0,0, 4,0,0,2]
SOLUTION_BOARD = [1,4,2,3, 2,3,1,4, 3,2,4,1, 4,1,3,2]
reference4 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
reference9 = [0 for i in range(9*9)]

START_BOARD9 = [
1,0,5,7,0,6,0,4,0,
9,0,7,0,0,2,0,6,0,
6,0,8,9,0,0,0,3,0,
7,0,0,1,0,4,0,2,8,
0,0,6,5,0,3,4,0,0,
4,8,0,2,0,7,0,0,3,
0,6,0,0,0,8,5,0,7,
0,1,0,6,0,0,3,0,4,
0,7,0,3,0,9,2,0,6
]

# board size (e.g. 4x4)
n = 9
squareWidth = int(sqrt(n))

maxFitness = n * (n - 1) * 2 * 2

# prints the board in a sudoku like format
def printBoard(board):	
	for i in range(n*n):
		print(board[i], end = ' ')
		if (i + 1) % n == 0 and i != 0:
			print()

# makes the initial random population of specified size
def initialPopulation(board, size):
	population = []
	for i in range(size):
		individual = []
		for num in board:
			# 0 indicates an unknown space, so use random number
			if num == 0:
				individual.append(randint(1,n))
			# otherwise use the number given
			else:
				individual.append(num)
		population.append(individual)
	return population

# number of row conflicts
# works for 4 and 9
def rowConflicts(board):
	# printBoard(board)
	conflicts = 0
	# index of each row
	for row in range(0, n*n, n):
		# check if the current number equals any of the remaining numbers
		for i in range(row, row + n):

			for j in range(i + 1, row + n):
				#print('Row', row, 'index:', i, j)
				# print(i, j)
				if board[i] == board[j]:
					conflicts += 1

	return conflicts

# number of column conflicts
def columnConflicts(board):
	conflicts = 0
	for column in range(0, n):
		for i in range(column, n * (n-1) + column + 1, n):
			for j in range(i + n, n * (n-1) + column + 1, n):
				#print(i, j)
				if board[i] == board[j]:
					#print('conflict')
					conflicts += 1

	return conflicts

# returns fitness, where 0 <= fitness <= maxFitness
def fitness(board):
	conflicts = 0

	conflicts += rowConflicts(board)

	conflicts += columnConflicts(board)
		
	return maxFitness - conflicts

# returns true if the individual is chosen to reproduce, false otherwise
def shouldReproduce(individual, fitness, meanFitness):
	if fitness >= meanFitness - meanFitness * 0.005:
		return True
	return False
	# if uniform(0, maxFitness) <= fitness:
	# 	return True 
	# else:
	# 	return False

def changableIndex(START_BOARD):
	changable = []
	for i in range(n*n):
		if START_BOARD[i] == 0:
			changable.append(i)

	return changable

# returns new population after random crossing occurs
def cross(population, changable):
	newPopulation = []
	while len(population) > 1:
		# get random index of two individuals to reproduce
		firstIndex = randint(0,len(population) - 1)
		individualOne = population[firstIndex]
		population.pop(firstIndex)

		secondIndex = randint(0,len(population) - 1)
		individualTwo = population[secondIndex]
		population.pop(secondIndex)

		# replace with changable index from the other child
		individual1Change = []
		individual2Change = []
		for index in changable:
			individual1Change.append(individualOne[index])
			individual2Change.append(individualTwo[index])

		crossIndex = randint(1, len(changable))

		child1Change = individual1Change[0:crossIndex] + individual2Change[crossIndex:]
		child2Change = individual2Change[0:crossIndex] + individual1Change[crossIndex:]

		i = 0
		for index in changable:
			individualOne[index] = child1Change[i]
			individualTwo[index] = child2Change[i]
			i += 1

		newPopulation.append(individualOne)
		newPopulation.append(individualTwo)

	return newPopulation

# returns the solved board, if any
def solve(board, populationSize, numGenerations):
	#print(randint(1,n))

	# get initial population
	population = initialPopulation(board, populationSize)

	# repeat the following until solution found or number of times met
	bestEver = 0
	GensWithoutImprovement = 0
	for generations in range(numGenerations):
		# run fitness on the population.
		individualFitness = [fitness(individual) for individual in population]
		meanFitness = mean(individualFitness)
		individualFitnessReproducing = []
		#print(individualFitness)

		# check to see if any of the individuals have a fitness of 0
		bestFitness = 0
		# keep best individual in the population every time
		bestIndividual = []

		i = 0
		while i < len(individualFitness):
			if individualFitness[i] > bestFitness:
				bestFitness = individualFitness[i]
				# best individual keeps going in every population
				bestIndividual = deepcopy(population[i])
			if individualFitness[i] == maxFitness:
				print('Max found:', fitness(population[i]))
				return population[i]
			else:
				# select individuals to reproduce, empty individual board and fitness if shouldn't reproduce
				if shouldReproduce(population[i], individualFitness[i], meanFitness) == False:
					population.pop(i)
					individualFitness.pop(i)
				else:
					i += 1
		numberReproduce = len(population)
		#print('Number reproduce:', numberReproduce)
		#print(individualFitness)

		# get changable spots
		changable = changableIndex(START_BOARD9)
		#print(changable)

		# randomly pick two to cross until all used or only one remains
		# if uneven number, last one gets left out?
				#print('Population size:', len(population))
		population = cross(population, changable)
		population.append(bestIndividual)
		# mutation
		for individual in population:
			for i in range(n*n):
				# mustation rate 
				if randint(1, 100) == 10 and i in changable:
					currentValue = individual[i]
					mutationValue = randint(1,n)
					while currentValue == mutationValue:
						mutationValue = randint(1,n)
					individual[i] = mutationValue

		population.append(bestIndividual) # should this be done before or after mutation??
		bestInThisPop = 0
		# check for the best individual
		for i in range(len(population)):
			if fitness(population[i]) > bestInThisPop:
				bestInThisPop = fitness(population[i])
		if bestInThisPop > bestEver:
			bestEver = bestInThisPop
			print(bestEver)
			GensWithoutImprovement -= 100
			if GensWithoutImprovement <= 0:
				GensWithoutImprovement = 1
		else:
			GensWithoutImprovement += 1
		
		# get new population if improvement isn't being seen
		# if GensWithoutImprovement % 1000 == 0:
		# 	population = initialPopulation(board, populationSize)
		# 	population.append(bestIndividual)
	print('end', fitness(bestIndividual))
	return bestIndividual
	
	# repeat





	

#print('Fitness:', fitness(SOLUTION_BOARD))
# print(columnConflicts([1,2,4,3,4,2,1,3,4,2,1,3,4,3,1,2]))
# print(fitness([1,2,4,3,4,2,1,3,4,2,1,3,4,3,1,2]))
# popSize = 100000
# numGenerations = 10000
popSize = 1000
numGenerations = 1000
# r = rowConflicts(reference9)
# c = columnConflicts(reference9)
# print(r, '+', c, '=', r+c)

solution = solve(START_BOARD9, popSize, numGenerations)
if solution != None:
		printBoard(solution)





