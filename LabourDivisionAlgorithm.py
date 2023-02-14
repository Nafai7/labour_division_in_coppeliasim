import numpy as np
import random
import math
import logging

class LabourDivisionAlgorithmEnviroment:
    def __init__(self, numberOfLaborers, numberOfTasks, workloadLevels, evaporationFactor, taskChangeFunction, initializeWithDelay = False, stepFunction = (), delayInSteps = 1, debugTime = ()):
        self.numberOfLaborers = numberOfLaborers
        self.numberOfTasks = numberOfTasks
        self.workloadLevels = workloadLevels
        self.evaporationFactor = evaporationFactor
        self.taskChangeFunction = taskChangeFunction
        
        self.laborers = []
        for i in range(numberOfLaborers):
            self.laborers.append(Laborer(i, numberOfTasks, debugTime))

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
                listOfPheromones.append({ "taskNumber": self.laborers[i].taskAssigned, "pheromones": self.laborers[i].pheromones})
            laborer.iterate(checkTaskCompletionFunction(laborer.id, laborer.taskAssigned), self.workloadLevels, taskEvaluationFunction, self.taskChangeFunction, listOfPheromones, self.evaporationFactor)

class Laborer:
    def __init__(self, id, numberOfTasks, debugTime):
        self.id = id
        self.pheromones = [0 for _ in range(numberOfTasks)]
        self.newPheromones = [0 for _ in range(numberOfTasks)]
        self.taskAssigned = None
        self.debugTime = debugTime

    def assignTask(self, taskNumber, taskChangeFunction):
        taskChangeFunction(self.id, taskNumber)
        self.taskAssigned = taskNumber
        self.pheromones[taskNumber] += 0.5

    def didTask(self, workloadLevels, taskEvaluationFunction):
        logging.info(self.debugTime() + ": Drone " + str(self.id) + " did task")
        logging.info(self.pheromones)
        evaluation = taskEvaluationFunction(self.taskAssigned)

        if 0 <= evaluation <= workloadLevels:
            self.pheromones[self.taskAssigned] += (1.0 / workloadLevels) * evaluation
            if self.pheromones[self.taskAssigned] > 1:
                self.pheromones[self.taskAssigned] = 1
        else:
            raise RuntimeError("Task evaluation function returns number not in bounds of levels of task imporance")
        logging.info(self.pheromones)

    def evaporatePheromones(self, evaporationFactor):
        self.pheromones = [round(x - (x * evaporationFactor), 6) for x in self.pheromones]
    
    def receivePheromones(self, receivedPheromones):
        if self.taskAssigned != receivedPheromones["taskNumber"]:
            logging.info(self.pheromones)
            logging.info(receivedPheromones)
            for i in range(len(self.pheromones)):
                self.newPheromones[i] = self.pheromones[i] + receivedPheromones["pheromones"][i]
                if self.newPheromones[i] > 1:
                    self.newPheromones[i] = 1
            logging.info(self.newPheromones)
        
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
        for i in maxIndexes:
            self.pheromones[i] -= 0.1
            if self.pheromones[i] < 0:
                self.pheromones[i] = 0
        self.pheromones[randomTask] += 0.1

    def changeToNewPheromones(self):
        if len(self.newPheromones) > 0:
            for i in range(len(self.pheromones)):
                self.pheromones[i] = self.newPheromones[i]
            self.newPheromones = [0 for _ in range(len(self.pheromones))]

    def iterate(self, taskDone, workloadLevels, taskEvaluationFunction, taskChangeFunction, listOfReceivedPheromones, evaporationFactor):
        self.changeToNewPheromones()
        self.evaporatePheromones(evaporationFactor)
        if taskDone:
            self.didTask(workloadLevels, taskEvaluationFunction)
            self.checkIfToChangeTask(taskChangeFunction)
        if len(listOfReceivedPheromones) > 0:
            for receivedPheromones in listOfReceivedPheromones:
                self.receivePheromones(receivedPheromones)
