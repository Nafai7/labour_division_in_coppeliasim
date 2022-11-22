require("LabourDivisionUtilities")

function sysCall_init()
    drone = sim.getObject('.')
    path = sim.getObject("/Path[0]")
    proximitySensor = sim.getObject(":/Proximity_sensor")
    velocity = 0.2
    posAlongPath = 0
    previousPosAlongPath = 0
    previousSimulationTime = 0
end

function sysCall_actuation()
    previousPosAlongPath = posAlongPath
    posAlongPath, previousSimulationTime = follow_path_step(path, drone, velocity, posAlongPath, previousSimulationTime, get_path_data_needed(path))
end

function setPath(newPath)
    path = newPath
end

function didFullPath()
    if posAlongPath < previousPosAlongPath then
        return true
    else
        return false
    end
end