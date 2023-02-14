import logging
import datetime
import pathlib

from zmqRemoteApi import RemoteAPIClient

import LabourDivisionAlgorithm as LDA
import workload

# GLOBAL VARIABLES:
# client, sim, addOnScript - client handle, simulation handle, add on script handle

def connect():
    global client, sim, addOnScript

    client = RemoteAPIClient()
    sim = client.getObject('sim')
    print("Connected to remote client")

    addOnScript = sim.getScript(sim.scripttype_addonscript, -1, "LabourDivisionAlgorithm")
    if sim.callScriptFunction("checkToScriptConnection", addOnScript):
        print("Connected to add on script")
    else:
        print("Failed to connect to add on script")

def getSimTimeToLog():
    return "[" + str(datetime.timedelta(seconds=round(sim.getSimulationTime(),2))) + "]:"

def changePath(droneNumber, pathNumber):
    global addOnScript
    sim.callScriptFunction("changePath", addOnScript, droneNumber, pathNumber)
    logging.info(getSimTimeToLog() + "Drone " + str(droneNumber) + " changed path to " + str(pathNumber))

def checkDetection(detectingDroneNumber):
    global addOnScript
    result = sim.callScriptFunction("checkDetection", addOnScript, detectingDroneNumber)
    if len(result) > 0:
        logging.info(getSimTimeToLog() + "Drone " + str(detectingDroneNumber) + " was detected by drones: " + str(result))
    return result

def checkIfDidFullPath(droneNumber, taskNumber):
    global addOnScript
    result = sim.callScriptFunction("checkIfDidFullPath", addOnScript, droneNumber)
    if result:
        workloadManager.decreaseWorkload(taskNumber)
    return result

def getConfig():
    global addOnScript
    return sim.callScriptFunction("getConfig", addOnScript)

def setUP():
    global client, config
    p = pathlib.Path("Logs/")
    p.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(filename=p.absolute().as_posix() + "\Simulation_logs_" + str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) + ".txt", filemode='a',format='%(message)s', level=logging.DEBUG)
    
    connect()
    client.setStepping(True)

    config = getConfig()

def main(timeLength, workload: workload.Workload, evaporationFactor):
    global client, sim, config
    
    sim.startSimulation()
    logging.info(getSimTimeToLog() + "############################Simulation started############################")
    
    client.step()
    lda = LDA.LabourDivisionAlgorithmEnviroment(config["numberOfDrones"], config["numberOfPaths"], workload.workloadLevels, evaporationFactor, changePath, True, client.step, 20, getSimTimeToLog)
    while (t := sim.getSimulationTime()) < timeLength:
        client.step()
        workload.increaseWorkload()
        lda.iterate(checkDetection, checkIfDidFullPath, workload.checkTaskEvaluation)
        logging.info(getSimTimeToLog() + "Workloads - " + str(workload.tasksWorkloads))

    logging.info(getSimTimeToLog() + "############################Simulation ended############################")
    sim.stopSimulation()

    del client

setUP()
workloadManager = workload.Workload(config["numberOfPaths"], 10, 100)
main(60, workloadManager, 0.01)