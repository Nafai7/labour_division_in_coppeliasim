require("LabourDivisionUtilities")

function sysCall_init()
    drone = sim.getObject('.')
    path = nil
    proximitySensor = sim.getObject(":/Proximity_sensor")
    velocity = 0.4
    posAlongPath = 0
    previousPosAlongPath = 0
    previousSimulationTime = 0
end

function sysCall_actuation()
    if path ~= nil then
        previousPosAlongPath = posAlongPath
        posAlongPath = follow_path_step(path, drone, velocity, posAlongPath, previousSimulationTime, get_path_data_needed(path))
    end
    previousSimulationTime = sim.getSimulationTime()
end

function setPath(newPath)
    path = newPath
    posAlongPath = 0
    previousPosAlongPath = 0
end

function didFullPath()
    if posAlongPath < previousPosAlongPath then
        return true
    else
        return false
    end
end