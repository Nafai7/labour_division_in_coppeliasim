require("LabourDivisionUtilities")
local config = require("config")
local firstStep = true
local drones = {}
local droneScripts = {}
local paths = {}

function loadObjects()
    for i = 0, (config.numberOfDrones - 1) do
        drones[i] = sim.getObject("/Quadcopter["..tostring(i).."]")
    end

    for i = 0,(config.numberOfDrones - 1) do
        local target = sim.getObject("/Quadcopter["..tostring(i).."]/target")
        local currentScript = sim.getScript(sim.scripttype_childscript, target)
        if currentScript ~= -1 then
            sim.removeScript(currentScript)
        end
        droneScripts[i] = sim.addScript(sim.scripttype_childscript)
        sim.setScriptText(droneScripts[i], droneScript)
        sim.associateScriptWithObject(droneScripts[i], target)
    end

    for i = 0,(config.numberOfPaths - 1) do
        paths[i] = sim.getObject("/Path["..tostring(i).."]")
    end
end

function sysCall_init()
    local allGood = true

    loadObjects()

    sim.addLog(sim.verbosity_default, "LDA script loaded")
end

-- function sysCall_actuation()
--     if firstStep then
--         sim.callScriptFunction("setPath", droneScripts[0], paths[0])
--         sim.callScriptFunction("setPath", droneScripts[1], paths[1])
--         firstStep = false
--     end

--     sim.addLog(sim.verbosity_default, tostring(sim.callScriptFunction("didFullPath", droneScripts[0])))

--     local detected = checkDetection(0)

--     sim.addLog(sim.verbosity_default, tostring(table.concat(detected,", ")))
-- end

-- function sysCall_afterSimulation()
--     firstStep = true
-- end

function changePath(droneNumber, pathNumber)
    sim.callScriptFunction("setPath", droneScripts[droneNumber], paths[pathNumber])
end

function checkDetection(detectingDroneNumber)
    local detected = {}
    for i = 0,(config.numberOfDrones - 1) do
        if i ~= detectingDroneNumber then
            if sim.checkProximitySensor(sim.getObject("/Quadcopter["..tostring(detectingDroneNumber).."]/Proximity_sensor"), drones[i]) == 1 then
                detected[i] = i
            end
        end
    end
    return detected
end

function checkIfDidFullPath(droneNumber)
    return sim.callScriptFunction("didFullPath", droneScripts[droneNumber])
end

function checkToScriptConnection()
    return true
end

function getConfig()
    return config
end