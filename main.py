import time
from zmqRemoteApi import RemoteAPIClient

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

def changePath(droneNumber, pathNumber):
    global addOnScript
    sim.callScriptFunction("changePath", addOnScript, droneNumber, pathNumber)

def checkDetection(detectingDroneNumber):
    global addOnScript
    return sim.callScriptFunction("checkDetection", addOnScript, detectingDroneNumber)

def checkIfDidFullPath(droneNumber):
    global addOnScript
    return sim.callScriptFunction("checkIfDidFullPath", addOnScript, droneNumber)

def getConfig():
    global addOnScript
    return sim.callScriptFunction("getConfig", addOnScript)

def main():
    global client, sim

    connect()
    client.setStepping(True)
    config = getConfig()

    sim.startSimulation()
    client.step()
    changePath(0,0)
    changePath(1,1)
    changePath(3,2)
    changePath(5,3)
    for i in range(0, 100):
        client.step()
    changePath(2,1)
    changePath(4,2)
    changePath(6,3)
    while (t := sim.getSimulationTime()) < 30:
        client.step()
    sim.stopSimulation()

    del client

main()