function sysCall_init()
    sim.addLog(sim.verbosity_default, "Bajo")
end

function sysCall_beforeSimulation()
    sim.addLog(sim.verbosity_default, "Jajo")
end

function sysCall_afterSave()
    sim.addLog(sim.verbosity_default, "Jajo")
end