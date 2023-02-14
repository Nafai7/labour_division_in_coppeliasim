class Workload:
    def __init__(self, numberOfTasks, workloadLevels, levelSize):
        self.numberOfTasks = numberOfTasks
        self.workloadLevels = workloadLevels
        self.levelSize = levelSize

        self.tasksWorkloads = [0 for _ in range(numberOfTasks)]

    def increaseWorkload(self):
        for i in range(len(self.tasksWorkloads)):
            self.tasksWorkloads[i] += 1
    
    def decreaseWorkload(self, taskNumber):
        self.tasksWorkloads[taskNumber] -= 5
    
    def checkTaskEvaluation(self, taskNumber):
        taskWorkload = self.tasksWorkloads[taskNumber]
        if taskWorkload < self.levelSize:
            return 1
        for level in range(2, self.workloadLevels - 1):
            if (taskWorkload >= ((level - 1) * self.levelSize)) and (taskWorkload < (level * self.levelSize)):
                return level
        
        return self.workloadLevels