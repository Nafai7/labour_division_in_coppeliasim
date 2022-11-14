function get_path_data_needed(path)
    local pathData=sim.unpackDoubleTable(sim.readCustomDataBlock(path,'PATH'))
    local m=Matrix(#pathData//7,7,pathData)
    local pathPositions=m:slice(1,1,m:rows(),3):data()
    local pathQuaternions=m:slice(1,4,m:rows(),7):data()
    local pathLengths,totalLength=sim.getPathLengths(pathPositions,3)
    return pathPositions, pathQuaternions, pathLengths, totalLength
end

function follow_path_step(path, drone, velocity, posAlongPath, previousSimulationTime, pathPositions, pathQuaternions, pathLengths, totalLength)
    local t=sim.getSimulationTime()
    posAlongPath=posAlongPath+velocity*(t-previousSimulationTime)
    posAlongPath=posAlongPath % totalLength
    local pos=sim.getPathInterpolatedConfig(pathPositions,pathLengths,posAlongPath)
    local quat=sim.getPathInterpolatedConfig(pathQuaternions,pathLengths,posAlongPath,nil,{2,2,2,2})
    sim.setObjectPosition(drone,path,pos)
    sim.setObjectQuaternion(drone,path,quat)
    return posAlongPath, t
end

local f = assert(io.open("droneScript.lua", "rb"))
droneScript = f:read("*all")
f:close()