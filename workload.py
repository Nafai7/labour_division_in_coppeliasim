class Workload:
    def __init__(self, numberOfTasks, workloadLevels, levelSize, workloadIncrementArray):
        if len(workloadIncrementArray) != numberOfTasks:
            raise RuntimeError("Workload incrementation array has to be have length equal to number of tasks")
        self.numberOfTasks = numberOfTasks
        self.workloadLevels = workloadLevels
        self.levelSize = levelSize
        self.workloadIncrementArray = workloadIncrementArray

        self.tasksWorkloads = [0 for _ in range(numberOfTasks)]

    def increaseWorkload(self):
        self.tasksWorkloads += self.workloadIncrementArray
    
    def checkTaskEvaluation(self, taskNumber):
        taskWorkload = self.tasksWorkloads[taskNumber]
        if taskWorkload < self.levelSize:
            return 1
        for level in range(2, self.workloadLevels - 1):
            if (taskWorkload >= ((level - 1) * self.levelSize)) and (taskWorkload < (level * self.levelSize)):
                return level
        
        return self.workloadLevels