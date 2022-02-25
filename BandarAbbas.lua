

local function StartGroup( groupName )
    local group = GROUP:FindByName( groupName )
    group:StartUncontrolled()
end

local function ActiveGroup( groupName )
    local group = GROUP:FindByName( groupName )
    group:Activate()
end

local function ActivateRedCap( groupName )
    RedCapGroup = GROUP:FindByName( groupName )
    RedCapGroup:Activate()

    RedZoneGroup = GROUP:FindByName( "Red Zone" )
    RedPatrolZone = ZONE_POLYGON:New( "Red Zone", RedZoneGroup )
    RedAICapZone = AI_CAP_ZONE:New( RedPatrolZone, 2000, 10000, 400, 600 )

    YellowZoneGroup = GROUP:FindByName( "Yellow Zone" )
    YellowZone = ZONE_POLYGON:New( "Yellow Zone", YellowZoneGroup )

    RedAICapZone:SetControllable( RedCapGroup )
    RedAICapZone:SetEngageZone( YellowZone ) -- Set the Engage Zone. The AI will only engage when the bogeys are within the CapEngageZone.
    RedAICapZone:__Start( 1 ) -- They should startup, and start patrolling in the PatrolZone.
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
TexacoStennis=RECOVERYTANKER:New(UNIT:FindByName("STENNIS"), "Texaco")
TexacoStennis:SetTakeoffAir()
TexacoStennis:SetTACAN(12, "TXC")
TexacoStennis:SetRadio(261)
TexacoStennis:SetCallsign(CALLSIGN.Tanker.Texaco)
TexacoStennis:SetRespawnInAir()
TexacoStennis:__Start(3)



UNIT:FindByName("TRUMAN"):PatrolRoute()
UNIT:FindByName("STENNIS"):PatrolRoute()

--
-- Menu
--

_SETTINGS:SetPlayerMenuOff()
local M1 = MENU_COALITION:New( coalition.side.BLUE, "TEST" )
local C1 = MENU_COALITION_COMMAND:New( coalition.side.BLUE, "SPAWN RED CAP", M1, ActivateRedCap, "Mig29*2" )
