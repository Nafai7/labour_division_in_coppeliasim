require("LabourDivisionUtilities")
local config = require("config")
local firstStep = true

function loadObjects()
    drones = {}
    for i = 0, (config.numberOfDrones - 1) do
        drones[i] = sim.getObject("/Quadcopter["..tostring(i).."]")
    end

    droneScripts = {}
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

    paths = {}
    for i = 0,(config.numberOfPaths - 1) do
        paths[i] = sim.getObject("/Path["..tostring(i).."]")
    end
end

function sysCall_init()
    local allGood = true

    loadObjects()

    sim.addLog(sim.verbosity_default, "LDA script loaded")
end

function sysCall_actuation()
    if firstStep then
        sim.callScriptFunction("setPath", droneScripts[0], paths[1])
        firstStep = false
    end
end

function sysCall_afterSimulation()
    firstStep = false
end