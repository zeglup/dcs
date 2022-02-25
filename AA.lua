_SETTINGS:SetPlayerMenuOff()

--
-- AIB-003 - Two coalitions InitCleanUp test.lua
--

RU_PlanesClientSet = SET_CLIENT:New():FilterCountries( "RUSSIA" ):FilterCategories( "plane" )
RU_PlanesSpawn = SPAWN:New( "AI RU" ):InitCleanUp( 20 )
RU_AI_Balancer = AI_BALANCER:New( RU_PlanesClientSet, RU_PlanesSpawn )

RU_AirbasesSet = SET_AIRBASE:New():FilterCoalitions("red"):FilterStart()
RU_AirbasesSet:Flush()
RU_AI_Balancer:ReturnToNearestAirbases( 10000, RU_AirbasesSet )


US_PlanesClientSet = SET_CLIENT:New():FilterCountries( "USA" ):FilterCategories( "plane" )
US_PlanesSpawn = SPAWN:New( "AI US" ):InitCleanUp( 20 )
US_AI_Balancer = AI_BALANCER:New( US_PlanesClientSet, US_PlanesSpawn )

--RU_AI_Balancer:ReturnToHomeAirbase( 10000 )

--local PatrolZoneGroup = GROUP:FindByName( "Patrol Zone Blue" )
--local PatrolZoneBlue = ZONE_POLYGON:New( "PatrolZone", PatrolZoneGroup )
--local PatrolZoneB = AI_PATROL_ZONE:New( PatrolZoneBlue, 3000, 6000, 900, 1100 ):ManageFuel( 0.2, 180 )
--US_AI_Balancer:SetPatrolZone( PatrolZoneB )
--
--local PatrolZoneGroup = GROUP:FindByName( "Patrol Zone Red" )
--local PatrolZoneRed = ZONE_POLYGON:New( "PatrolZone", PatrolZoneGroup )
--local PatrolZoneR = AI_PATROL_ZONE:New( PatrolZoneRed, 3000, 6000, 900, 1100 ):ManageFuel( 0.2, 180 )
--RU_AI_Balancer:SetPatrolZone( PatrolZoneR )



-- Name: AIB-002 - Patrol AI.lua
-- Author: FlightControl
-- Date Created: 7 December 2016
--
-- # Situation:
--
-- For the red coalition, 2 client slots are foreseen.
-- For those players that have not joined the mission, red AI is spawned.
-- The red AI should start patrolling an area until fuel is empty and return to the home base.
--
-- # Test cases:
--
-- 1. If no player is logging into the red slots, 2 red AI planes should be alive.
-- 2. If a player joins one red slot, one red AI plane should return to the nearest home base.
-- 3. If two players join the red slots, no AI plane should be spawned, and all airborne AI planes should return to the nearest home base.
-- 4. Spawned AI should take-off from the airbase, and start patrolling the area around Anapa.
-- 5. When the AI is out-of-fuel, it should report it is returning to the home base, and land at Anapa.

-- Define the SET of CLIENTs from the red coalition. This SET is filled during startup.
RU_PlanesClientSet = SET_CLIENT:New():FilterCountries( "RUSSIA" ):FilterCategories( "plane" )

-- Define the SPAWN object for the red AI plane template.
-- We use InitCleanUp to check every 20 seconds, if there are no planes blocked at the airbase, waithing for take-off.
-- If a blocked plane exists, this red plane will be ReSpawned.
RU_PlanesSpawn = SPAWN:New( "AI RU" ):InitCleanUp( 20 )

-- Start the AI_BALANCER, using the SET of red CLIENTs, and the SPAWN object as a parameter.
RU_AI_Balancer = AI_BALANCER:New( RU_PlanesClientSet, RU_PlanesSpawn )

local PatrolZones = {}

function RU_AI_Balancer:OnAfterSpawned( SetGroup, From, Event, To, AIGroup )

    local PatrolZoneGroup = GROUP:FindByName( "PatrolZone" )
    local PatrolZone = ZONE_POLYGON:New( "PatrolZone", PatrolZoneGroup )


    PatrolZones[AIGroup] = AI_PATROL_ZONE:New( PatrolZone, 3000, 6000, 400, 600 )
    PatrolZones[AIGroup]:ManageFuel( 0.2, 60 )
    PatrolZones[AIGroup]:SetControllable( AIGroup )
    PatrolZones[AIGroup]:__Start( 5 )

end


---
-- Name: CAP-011 - CAP and Engage within Zone
-- Author: FlightControl
-- Date Created: 16 January 2017
--
-- # Situation:
--
-- The Su-27 airplane will patrol in PatrolZone.
-- It will engage when it detects the airplane and when the A-10C is within the CapEngageZone.
--
-- # Test cases:
--
-- 1. Observe the Su-27 patrolling.
-- 2. Observe that, when the A-10C is within the engage zone, it will engage.
-- 3. After engage, observe that the Su-27 returns to the PatrolZone.
-- 4. If you want, you can wait until the Su-27 is out of fuel and will land.


CapPlane = GROUP:FindByName( "Plane" )

PatrolZone = ZONE:New( "Patrol Zone" )

AICapZone = AI_CAP_ZONE:New( PatrolZone, 500, 1000, 500, 600 )

EngageZoneGroup = GROUP:FindByName( "Engage Zone" )

CapEngageZone = ZONE_POLYGON:New( "Engage Zone", EngageZoneGroup )

AICapZone:SetControllable( CapPlane )
AICapZone:SetEngageZone( CapEngageZone ) -- Set the Engage Zone. The AI will only engage when the bogeys are within the CapEngageZone.

AICapZone:__Start( 1 ) -- They should statup, and start patrolling in the PatrolZone.




---
-- Name: CAP-010 - CAP and Engage within Range
-- Author: FlightControl
-- Date Created: 16 January 2017
--
-- # Situation:
--
-- The Su-27 airplane will patrol in PatrolZone.
-- It will engage when it detects the airplane and when the A-10C is within the engage range.
--
-- # Test cases:
--
-- 1. Observe the Su-27 patrolling.
-- 2. Observe that, when the A-10C is within the engage range, it will engage.
-- 3. After engage, observe that the Su-27 returns to the PatrolZone.
-- 4. If you want, you can wait until the Su-27 is out of fuel and will land.

CapPlane = GROUP:FindByName( "Plane" )

PatrolZone = ZONE:New( "Patrol Zone" )

AICapZone = AI_CAP_ZONE:New( PatrolZone, 500, 1000, 500, 600 )

AICapZone:SetControllable( CapPlane )
AICapZone:SetEngageRange( 20000 ) -- Set the Engage Range to 20.000 meters. The AI won't engage when the enemy is beyond 20.000 meters.

AICapZone:__Start( 1 ) -- They should statup, and start patrolling in the PatrolZone.

---
-- Name: ZON-510 - ZONE_POLYGON declared in ME
-- Author: FlightControl
-- Date Created: 21 May 2018
--
-- # Situation:
--
-- A ZONE_POLYGON has been defined, within the mission editor using ~ZONE_POLYGON in the group name.
-- Its boundaries are smoking.
-- A vehicle is driving through the zone perimeters.
-- When the vehicle is driving in the zone, a red smoke is fired from the vehicle location.
--
-- # Test cases:
--
-- 1. Observe the polygon perimeter smoke.
-- 2. Observe the vehicle smoking a red smoke when driving through the zone.

GroupInside = GROUP:FindByName( "Test Inside Polygon" )
GroupOutside = GROUP:FindByName( "Test Outside Polygon" )

PolygonZone = ZONE_POLYGON:FindByName( "Polygon A" )
PolygonZone:SmokeZone( SMOKECOLOR.White, 10 )

Messager = SCHEDULER:New( nil,
        function()
            GroupInside:MessageToAll( ( GroupInside:IsCompletelyInZone( PolygonZone ) ) and "Inside Polygon A" or "Outside Polygon A", 1 )
            if GroupInside:IsCompletelyInZone( PolygonZone ) then
                GroupInside:GetUnit(1):SmokeRed()
            end
        end,
        {}, 0, 1 )

---
-- Name: SCO-101 - Scoring Client to Client
-- Author: FlightControl
-- Date Created: 24 Feb 2017
--
-- # Situation:
--
-- A shooting range has been setup to test client to client scoring.
--
-- # Test cases:
--
-- 1. Observe the scoring granted to your flight when you hit and kill other clients.


HQ = GROUP:FindByName( "HQ", "Bravo HQ" )

CommandCenter = COMMANDCENTER:New( HQ, "Lima" )

Scoring = SCORING:New( "Detect Demo" )



--BASE:TraceClass("SET_CLIENT")
--BASE:TraceClass("AIBALANCER")
--BASE:TraceClass("SET_AIRBASE")
--BASE:TraceClass("PATROLZONE")
--BASE:TraceAll(true)
BASE:TraceLevel( 3 )
BASE:TraceClass( "SPAWN" )