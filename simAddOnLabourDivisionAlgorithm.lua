require("LabourDivisionUtilities")

function sysCall_init()
    local message = "LDA script loaded"
    local allGood = true

    drone = sim.getObject("/Quadcopter")

    paths = {}
    for i = 0,2 do
        paths[i] = sim.getObject("/Path["..tostring(i).."]")
    end

    sim.addLog(sim.verbosity_default, message)
end

function sysCall_actuation()
    droneScript = sim.getScript(sim.scripttype_childscript, sim.getObject("/target"))

    sim.callScriptFunction("setPath", droneScript, paths[1])
end