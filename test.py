import time
from zmqRemoteApi import RemoteAPIClient
client = RemoteAPIClient()

sim = client.getObject('sim')
client.setStepping(True)
drone = sim.getObject('/Quadcopter')
droneInitMass = sim.getShapeMass(drone)
sensor = sim.getObject('/Proximity_sensor')

sim.startSimulation()

sim.stopSimulation()
del client