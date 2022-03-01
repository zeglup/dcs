RedZoneGroup = GROUP:FindByName( "Red Zone" )
RedZone = ZONE_POLYGON:New( "Yellow Zone", RedZoneGroup )
YellowZoneGroup = GROUP:FindByName( "Yellow Zone" )
YellowZone = ZONE_POLYGON:New( "Yellow Zone", YellowZoneGroup )
GroundPatrolZoneGroup = GROUP:FindByName( "Bandar Red Zone" )
GroundPatrolZone = ZONE_POLYGON:New( "Bandar Red Zone", GroundPatrolZoneGroup )
GroundSpawnZoneGroup = GROUP:FindByName( "GroundSpawn Zone" )
GroundSpawnZone = ZONE_POLYGON:New( "GroundSpawn Zone", GroundSpawnZoneGroup )
AAAZone1Group = GROUP:FindByName( "SpawnAAA1" )
AAAZone1 = ZONE_POLYGON:New( "SpawnAAA1", AAAZone1Group )
AAAZone2Group = GROUP:FindByName( "SpawnAAA2" )
AAAZone2 = ZONE_POLYGON:New( "SpawnAAA2", AAAZone2Group )
AAAZone3Group = GROUP:FindByName( "SpawnAAA3" )
AAAZone3 = ZONE_POLYGON:New( "SpawnAAA3", AAAZone3Group )
AAAZone4Group = GROUP:FindByName( "SpawnAAA4" )
AAAZone4 = ZONE_POLYGON:New( "SpawnAAA4", AAAZone4Group )
FrontLine1Group = GROUP:FindByName( "SpawnFront1" )
FrontLine1Zone = ZONE_POLYGON:New( "SpawnFront1", FrontLine1Group )
FrontLine2Group = GROUP:FindByName( "SpawnFront2" )
FrontLine2Zone = ZONE_POLYGON:New( "SpawnFront2", FrontLine2Group )

TBOLT_set = SET_CLIENT:New():FilterCoalitions( "blue" ):FilterCategories( "plane" ):FilterPrefixes( "TBOLT" ):FilterActive():FilterStart()

ratioAGPerPlayer = 4


local function StartGroup( groupName )
    local group = GROUP:FindByName( groupName )
    group:StartUncontrolled()
end

local function ActiveGroup( groupName )
    local group = GROUP:FindByName( groupName )
    group:Activate()
end

local function ActivateRedCap( groupName )
    --
    -- Spawn CAP
    --
    local PatrolZones = {}

    RedCapSpawn = SPAWN
            :NewWithAlias( groupName, "REDCAP" )
            :InitRandomizeZones( { RedZone } )
            :OnSpawnGroup( function ( spawnGroup )

        PatrolZones[spawnGroup] = AI_CAP_ZONE:New( RedZone, 2000, 5000, 400, 600 )
        PatrolZones[spawnGroup]:SetControllable( spawnGroup )
        PatrolZones[spawnGroup]:SetDetectionZone( YellowZone )
        PatrolZones[spawnGroup]:SetEngageZone( YellowZone )
        PatrolZones[spawnGroup]:__Start( 5 )
    end
    )
    local num = TBOLT_set:CountAlive() + 1
    for i=1, num, 1 do
        RedCapSpawn:Spawn()
    end
end

local function ActivateCivilians()
    --
    -- Spawn Ground Civilians
    --

    CiviliansBusTemplates = { "Bus1", "Bus2" }
    CiviliansCarTemplates = { "Car" }
    CiviliansTruckTemplates = { "Truck1","Truck2" }

    CiviliansBusSpawn = SPAWN:New("Bus1")
            :InitLimit( 8 , 8 )
            :InitRandomizeTemplate( CiviliansBusTemplates )
            :InitRandomizeZones( { GroundSpawnZone } )
            :InitRandomizeRoute( 1, 1, 500 )
            :SpawnScheduled( 2, 1)
            :OnSpawnGroup(
            function( SpawnGroup )
                SCHEDULER:New( nil,
                        function()
                            SpawnGroup:TaskRouteToZone( GroundPatrolZone, true, 20, "On Road")
                        end, {}, 1, 180
                )

            end
    )

    CiviliansCarSpawn = SPAWN:New("Car")
                          :InitLimit( 20 , 20 )
                          :InitRandomizeTemplate( CiviliansCarTemplates )
                          :InitRandomizeZones( { GroundSpawnZone } )
                          :InitRandomizeRoute( 1, 1, 500 )
                          :SpawnScheduled( 2, 1)
                          :OnSpawnGroup(
            function( SpawnGroup )
                SCHEDULER:New( nil,
                        function()
                            SpawnGroup:TaskRouteToZone( GroundPatrolZone, true, 20, "On Road")
                        end, {}, 1, 180
                )

            end
    )

    CiviliansTruckSpawn = SPAWN:New("Truck1")
                             :InitLimit( 8 , 8 )
                             :InitRandomizeTemplate( CiviliansTruckTemplates )
                             :InitRandomizeZones( { GroundSpawnZone } )
                             :InitRandomizeRoute( 1, 1, 500 )
                             :SpawnScheduled( 2, 1)
                             :OnSpawnGroup(
            function( SpawnGroup )
                SCHEDULER:New( nil,
                        function()
                            SpawnGroup:TaskRouteToZone( GroundPatrolZone, true, 20, "On Road")
                        end, {}, 1, 180
                )

            end
    )



end

local function ActivateAAA()
    maxGroundTargets = TBOLT_set:CountAlive() * ratioAGPerPlayer

    AAATemplates = { "ZU-23", "ZSU-57", "Shilka", "AAA" }

    AAAZones = { AAAZone1, AAAZone2, AAAZone3, AAAZone4 }
    AAASpawn = SPAWN:New("ZU-23")
                          :InitLimit( maxGroundTargets , maxGroundTargets )
                          :InitRandomizeTemplate( AAATemplates )
                          :InitRandomizeZones( AAAZones )
                          :SpawnScheduled( 2, 1)

    ManpadSpawn = SPAWN:New("MANPAD")
                    :InitLimit( maxGroundTargets * 2 , maxGroundTargets * 2 )
                    :InitRandomizeZones( { AAAZones } )
                    :SpawnScheduled( 2, 1)
end


local function ActivateGroundTargets()


    groupsTable = { "C1", "C2", "C3" }
    for i = 1, TBOLT_set:CountAlive() do
        for x = #groupsTable, 2, -1 do
            local y = math.random(x)
            groupsTable[x], groupsTable[y] = groupsTable[y], groupsTable[x]
        end
        BASE:E(groupsTable[i])
        CGroup = GROUP:FindByName(groupsTable[i])
        CGroup:Activate()
        SCHEDULER:New( nil,
                function()
                    CGroup:TaskRouteToZone( GroundPatrolZone, true, 20, "On Road")
                end, {}, 1, 180
        )
    end


    maxGroundTargets = TBOLT_set:CountAlive() * ratioAGPerPlayer
    BASE:E("maxGround" .. tostring(maxGroundTargets))
    FrontLine1Templates = { "BTR", "T-55", "M113", "BMP", "T-72"}

    FrontLine1Spawn = SPAWN:New("BTR")
                               :InitLimit( maxGroundTargets , maxGroundTargets )
                               :InitRandomizeTemplate( FrontLine1Templates )
                               :InitRandomizeZones( { FrontLine1Zone } )
                               :SpawnScheduled( 2, 1)
                               :OnSpawnGroup(
                                function( SpawnGroup )
                                    SpawnGroup:SetCommandImmortal(true)
                                    SpawnUnits = SpawnGroup:GetUnits()
                                    for i = 1, #SpawnUnits do
                                        local unit = SpawnGroup:GetUnit( i )
                                        unit:HandleEvent( EVENTS.Hit )
                                        function unit:OnEventHit( EventData )
                                            BASE:E(EventData.IniUnitName)
                                            if(nil ~= string.find(EventData.IniUnitName, "TBOLT")) then
                                                SpawnGroup:SetCommandImmortal(false)
                                                unit:Explode(500, .1)
                                                BASE:E(EventData.IniUnitName)
                                            end
                                        end
                                    end
                                end
    )

    FrontLine2Spawn = SPAWN:New("MLRS")
                           :InitLimit( 2 , 2 )
                           :InitRandomizeZones( { FrontLine2Zone } )
                           :SpawnScheduled( 2, 1)
                           :OnSpawnGroup(
                                function( SpawnGroup )
                                    SpawnGroup:SetCommandImmortal(true)
                                end
    )

    InfSpawn = SPAWN:New("Inf")
                           :InitLimit( 30 , 50 )
                           :InitRandomizeZones( { FrontLine1Zone } )
                           :SpawnScheduled( 2, 0.5)
                           :OnSpawnGroup(
                                function( SpawnGroup )
                                    SpawnGroup:SetCommandImmortal(true)
                                end
    )


    SA15Group = GROUP:FindByName("SA15")
    SA15Group:SetAIOff()
    SA15Group:Activate()

end


--
-- Rescue Helos
--

local RescueHeloTruman = RESCUEHELO:New("TRUMAN", "Rescue Helo")
RescueHeloTruman:Start()

local RescueHeloStennis = RESCUEHELO:New("STENNIS", "Rescue Helo")
RescueHeloStennis:Start()


-- Texaco Stennis
--
--TexacoStennis=RECOVERYTANKER:New(UNIT:FindByName("STENNIS"), "Texaco")
--TexacoStennis:SetTakeoffAir()
--TexacoStennis:SetTACAN(12, "TXC")
--TexacoStennis:SetRadio(261)
--TexacoStennis:SetCallsign(CALLSIGN.Tanker.Texaco)
--TexacoStennis:SetRespawnInAir()
--TexacoStennis:__Start(3)
--
--
--
--UNIT:FindByName("TRUMAN"):PatrolRoute()
--UNIT:FindByName("STENNIS"):PatrolRoute()

--
-- Menu
--

_SETTINGS:SetPlayerMenuOff()
local M1 = MENU_COALITION:New( coalition.side.BLUE, "TEST" )
MENU_COALITION_COMMAND:New( coalition.side.BLUE, "SPAWN RED CAP", M1, ActivateRedCap, "Mig29" )
MENU_COALITION_COMMAND:New( coalition.side.BLUE, "CIVS", M1, ActivateCivilians )
MENU_COALITION_COMMAND:New( coalition.side.BLUE, "AAA", M1, ActivateAAA )
MENU_COALITION_COMMAND:New( coalition.side.BLUE, "GROUND", M1, ActivateGroundTargets )
