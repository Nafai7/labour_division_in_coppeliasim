import logging
import datetime
import pathlib

from zmqRemoteApi import RemoteAPIClient

import LabourDivisionAlgorithm as LDA

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
    return "[" + str(datetime.timedelta(seconds=round(sim.getSimulationTime(),2))) + "["

def changePath(droneNumber, pathNumber):
    global addOnScript
    sim.callScriptFunction("changePath", addOnScript, droneNumber, pathNumber)
    logging.info(getSimTimeToLog() + "Drone " + str(droneNumber) + " changed path to " + str(pathNumber))

def checkDetection(detectingDroneNumber):
    global addOnScript
    result = sim.callScriptFunction("checkDetection", addOnScript, detectingDroneNumber)
    logging.info(getSimTimeToLog() + "Drone " + str(detectingDroneNumber) + " was detected by drones: " + str(result))
    return result

def checkIfDidFullPath(droneNumber):
    global addOnScript
    return sim.callScriptFunction("checkIfDidFullPath", addOnScript, droneNumber)

def getConfig():
    global addOnScript
    return sim.callScriptFunction("getConfig", addOnScript)

def main(timeLength):
    global client, sim

    p = pathlib.Path("Logs/")
    p.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(filename=p.absolute().as_posix() + "\Simulation_logs_" + str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) + ".txt", filemode='a',format='%(message)s', level=logging.DEBUG)

    connect()
    client.setStepping(True)
    config = getConfig()

    sim.startSimulation()
    client.step()
    changePath(0,0)
    while (t := sim.getSimulationTime()) < timeLength:
        client.step()
        for i in range(0, config["numberOfDrones"]):
            checkDetection(i)
        if (t == 1.0):
            changePath(1,1)
        if (t == 2.0):
            changePath(3,2)
        if (t == 3.0):
            changePath(5,3)
        if (t == 4.0):
            changePath(2,1)
        if (t == 5.0):
            changePath(4,2)
        if (t == 6.0):
            changePath(6,3)
        if (t == 30.0):
            changePath(2,2)
            changePath(1,3)

    sim.stopSimulation()

    del client

main(60)