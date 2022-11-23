class LabourDivisionAlgorithm:
    def __init__(self, numberOfLaborers, numberOfTasks, levelsOfTaskImportance, evaporationFactor, taskEvaluationFunction):
        self.numberOfLaborers = numberOfLaborers
        self.numberOfTasks = numberOfTasks
        self.levelsOfTaskImportance = levelsOfTaskImportance
        self.evaporationFactor = evaporationFactor
        self.taskEvaluationFunction = taskEvaluationFunction

class Laborer:
    def __init__(self, numberOfTasks):
        self.pheromones = [0 for _ in range(numberOfTasks)]
        self.taskAssigned = None

    def assignTask(self, taskNumber):
        self.taskAssigned = taskNumber

    def didTask(self, levelsOfTaskImportance, taskEvaluationFunction):
        evaluation = taskEvaluationFunction(self.taskAssigned)

        if 0 <= evaluation <= levelsOfTaskImportance:
            self.pheromones[self.taskAssigned] += (1.0 / levelsOfTaskImportance) * evaluation
            if self.pheromones[self.taskAssigned] > 1:
                self.pheromones[self.taskAssigned] = 1
        else:
            raise RuntimeError("Task evaluation function returns number not in bounds of levels of task imporance")

    def evaporatePheromones(self, evaporationFactor):
        self.pheromones = [x * evaporationFactor for x in self.pheromones]
    
    def receivePheromones(self, receivedPheromones):
        for i in range(len(self.pheromones)):
            self.pheromones[i] += receivedPheromones[i]
            if self.pheromones[i] > 1:
                self.pheromones[i] = 1
