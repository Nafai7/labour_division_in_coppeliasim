import numpy as np
import random
import math

class LabourDivisionAlgorithmEnviroment:
    def __init__(self, numberOfLaborers, numberOfTasks, workloadLevels, evaporationFactor, taskChangeFunction, initializeWithDelay = False, stepFunction = (), delayInSteps = 1):
        self.numberOfLaborers = numberOfLaborers
        self.numberOfTasks = numberOfTasks
        self.workloadLevels = workloadLevels
        self.evaporationFactor = evaporationFactor
        self.taskChangeFunction = taskChangeFunction
        
        self.laborers = []
        for i in range(numberOfLaborers):
            self.laborers.append(Laborer(i, numberOfTasks))

        # distribute laborers equally among tasks
        dronesPerTask = math.floor(numberOfLaborers / numberOfTasks)
        index = 0
        for i in range(numberOfTasks):
            for j in range(dronesPerTask):
                self.laborers[index].assignTask(i, taskChangeFunction)
                index += 1
                if initializeWithDelay:
                    for i in range(delayInSteps):
                        stepFunction()

        # laborers left with no task get random tasks assigned
        for i in range(index, numberOfLaborers):
            self.laborers[i].assignTask(random.randint(0, numberOfTasks - 1), taskChangeFunction)
            if initializeWithDelay:
                    for i in range(delayInSteps):
                        stepFunction()


    def iterate(self, checkDetectionFunction, checkTaskCompletionFunction, taskEvaluationFunction):
        for laborer in self.laborers:
            detectedLaborers = checkDetectionFunction(laborer.id)
            listOfPheromones = []
            for i in detectedLaborers:
                listOfPheromones.append(self.laborers[i].pheromones)
            laborer.iterate(checkTaskCompletionFunction(laborer.id), self.workloadLevels, taskEvaluationFunction, self.taskChangeFunction, listOfPheromones, self.evaporationFactor)

class Laborer:
    def __init__(self, id, numberOfTasks):
        self.id = id
        self.pheromones = [0 for _ in range(numberOfTasks)]
        self.taskAssigned = None

    def assignTask(self, taskNumber, taskChangeFunction):
        taskChangeFunction(self.id, taskNumber)
        self.taskAssigned = taskNumber
        self.pheromones[taskNumber] += 0.5

    def didTask(self, workloadLevels, taskEvaluationFunction):
        evaluation = taskEvaluationFunction(self.taskAssigned)

        if 0 <= evaluation <= workloadLevels:
            self.pheromones[self.taskAssigned] += (1.0 / workloadLevels) * evaluation
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
        
    def checkIfToChangeTask(self, taskChangeFunction):
        maxValue = 0
        maxIndexes = []
        for i in range(len(self.pheromones)):
            if self.pheromones[i] > maxValue:
                maxValue = self.pheromones[i]
                maxIndexes.clear()
                maxIndexes.append(i)
            elif self.pheromones[i] == maxValue:
                maxIndexes.append(i)
        randomTask = random.choice(maxIndexes)
        if randomTask != self.taskAssigned:
            taskChangeFunction(self.id, randomTask)
            self.taskAssigned = randomTask

    def iterate(self, taskDone, workloadLevels, taskEvaluationFunction, taskChangeFunction, listOfReceivedPheromones, evaporationFactor):
        if taskDone:
            self.didTask(workloadLevels, taskEvaluationFunction)
        if len(listOfReceivedPheromones) > 0:
            for receivedPheromones in listOfReceivedPheromones:
                self.receivePheromones(receivedPheromones)
            self.checkIfToChangeTask(taskChangeFunction)
        self.evaporatePheromones(evaporationFactor)
