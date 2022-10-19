import time
from zmqRemoteApi import RemoteAPIClient
client = RemoteAPIClient()

sim = client.getObject('sim')
client.setStepping(True)
drone = sim.getObject('/Quadcopter')
droneInitMass = sim.getShapeMass(drone)
sensor = sim.getObject('/Proximity_sensor')

sim.startSimulation()
messageToDisplay = 1
while (sim.getSimulationTime() < 8):
    sim.setShapeMass(drone, sim.getShapeMass(drone) + 0.001)
    if (sim.getSimulationTime().is_integer()):
        print("[DRON]: Bzzzz")
        result = sim.checkProximitySensor(sensor, drone)
        if (result != 0):
            if (messageToDisplay == 1):
                print("[SENSOR]: O jakiś dron")
            if (messageToDisplay == 2):
                print("[SENSOR]: O NIE O SPADA")
            if (messageToDisplay == 3):
                print("[SENSOR]: O BOŻE O KURWA!")
            if (messageToDisplay == 4):
                print("[SENSOR]: CO SIĘ DZIĘJE SŁODKI JEZU NIE WIEM CO MAM ROBIĆ POMOCY! KURWA POMOCY LUDZIE DRON SIĘ ROZJEBIE AAAA!")
            messageToDisplay += 1
        else:
            print("[SENSOR]: Wszystko w porządku")
    client.step()

sim.setShapeMass(drone, droneInitMass)
sim.stopSimulation()
del client