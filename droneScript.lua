require("LabourDivisionUtilities")

function sysCall_init()
    drone = sim.getObject('.')
    path = sim.getObject("/Path[0]")
    velocity = 0.1
    posAlongPath = 0
    previousSimulationTime = 0
end

function sysCall_actuation()
    posAlongPath, previousSimulationTime = follow_path_step(path, drone, velocity, posAlongPath, previousSimulationTime, get_path_data_needed(path))
end

function setPath(newPath)
    path = newPath
end
