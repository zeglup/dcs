--
-- A/A Training
--

local function StartGroup( groupName )
    MESSAGE:New( groupName .. " a démarré", 5 ):ToAll()
    local group = GROUP:FindByName( groupName )
    group:StartUncontrolled()
end

local function ActivateGroup( groupName )
    MESSAGE:New( groupName .. " est actif", 5 ):ToAll()
    local group = GROUP:FindByName( groupName )
    group:Activate()
end

local function ActivateMagic()
    MESSAGE:New( "MAGIC est actif sur 125.000Mhz", 5 ):ToAll()
    local group = GROUP:FindByName( "Magic" )
    group:Activate()
end

local function ActivateOverlord()
    MESSAGE:New( "OVERLORD est actif sur 126.000Mhz", 5 ):ToAll()
    local group = GROUP:FindByName( "Overlord" )
    group:Activate()
end

local function ActivateTexaco()
    MESSAGE:New( "TEXACO est actif : 125.000Mhz / TCN 1X A22 300kts", 10 ):ToAll()
    local group = GROUP:FindByName( "Texaco" )
    group:Activate()
end

local function ActivateArco()
    MESSAGE:New( "ARCO est actif : 126.000Mhz / TCN 2X A22 300kts", 10 ):ToAll()
    local group = GROUP:FindByName( "Arco" )
    group:Activate()
end

local function ActivateRedCap( groupName )
    US_PlanesClientSet = SET_CLIENT:New():FilterCoalitions( "blue" ):FilterCategories( "plane" ):FilterPrefixes( "TBOLT" ):FilterActive():FilterStart()

    RU_PlanesSpawn = SPAWN
            :NewWithAlias( groupName, "REDAI" )
            :InitRandomizeZones( { RedZone } )
            :OnSpawnGroup( function ( spawnGroup )

        PatrolZones[spawnGroup] = AI_CAP_ZONE:New( RedZone , 2000, 5000, 400, 600 )
        PatrolZones[spawnGroup]:SetControllable( spawnGroup )
        PatrolZones[spawnGroup]:SetDetectionZone( YellowZone )
        PatrolZones[spawnGroup]:SetEngageZone( YellowZone )
        PatrolZones[spawnGroup]:__Start( 5 )
    end
    )
    local num = 1
    for i=1, US_PlanesClientSet:CountAlive(), 1 do
        RU_PlanesSpawn:Spawn()
        num = i
    end
    MESSAGE:New( tostring(num) .. " x " .. groupName .. " en Zone Rouge", 10 ):ToAll()
end


local function ActivateBlueAI( mode )
    US_PlanesSpawn = SPAWN
            :NewWithAlias( "TBOLT BLUE AI " .. mode, "BLUEAI" )
            :InitCleanUp( 20 )
    local FilterName = "TBOLT"
    if (mode == "HOT") then
        FilterName = "TBOLT HOT"
    end
    US_PlanesClientSet = SET_CLIENT:New():FilterCoalitions( "blue" ):FilterCategories( "plane" ):FilterPrefixes( "TBOLT HOT" ):FilterStart()
    US_AI_Balancer = AI_BALANCER:New( US_PlanesClientSet, US_PlanesSpawn )
    US_AI_Balancer:InitSpawnInterval(2)
    US_AI_Balancer:ReturnToHomeAirbase( 10000 )

    function US_AI_Balancer:OnAfterSpawned( SetGroup, From, Event, To, AIGroup )

                PatrolZones[AIGroup] = AI_CAP_ZONE:New( BlueZone , 5000, 10000, 400, 500 )
                PatrolZones[AIGroup]:SetControllable( AIGroup )
                PatrolZones[AIGroup]:SetDetectionZone( YellowZone )
                PatrolZones[AIGroup]:SetEngageZone( YellowZone )
                PatrolZones[AIGroup]:__Start( 1 )

    end
    MESSAGE:New( "TBOLT BLUE AI " .. mode .. " est actif", 10 ):ToAll()

end

local function ActivateRedAI()


end

local function KillAllRed()
    RU_PlanesUnitSet = SET_UNIT:New():FilterCoalitions( "red" ):FilterCategories( "plane" ):FilterPrefixes("REDAI"):FilterActive():FilterOnce()
    RU_PlanesUnitSet:ForEachUnit(function( unitObject )
        unitObject:Destroy()
    end
    )
    MESSAGE:New( "Tous les rouges sont morts !", 10 ):ToAll()
end


local function ImmortalMode( switch )


    local tagName = ""
    local TBOLTGroupsB = {
        GROUP:FindByName( "TBOLT" .. tagName .. " 1-1"),
        GROUP:FindByName( "TBOLT" .. tagName .. " 1-2"),
        GROUP:FindByName( "TBOLT" .. tagName .. " 1-3"),
        GROUP:FindByName( "TBOLT" .. tagName .. " 1-4"),
        GROUP:FindByName( "TBOLT" .. tagName .. " HOT 1-1"),
        GROUP:FindByName( "TBOLT" .. tagName .. " HOT 1-2"),
        GROUP:FindByName( "TBOLT" .. tagName .. " HOT 1-3"),
        GROUP:FindByName( "TBOLT" .. tagName .. " HOT 1-4"),
        GROUP:FindByName( "TBOLT" .. tagName .. " M2000 1-1"),
        GROUP:FindByName( "TBOLT" .. tagName .. " M2000 1-2"),
        GROUP:FindByName( "TBOLT" .. tagName .. " M2000 1-3"),
        GROUP:FindByName( "TBOLT" .. tagName .. " M2000 1-4"),
        GROUP:FindByName( "TBOLT" .. tagName .. " HOT M2000 1-1"),
        GROUP:FindByName( "TBOLT" .. tagName .. " HOT M2000 1-2"),
        GROUP:FindByName( "TBOLT" .. tagName .. " HOT M2000 1-3"),
        GROUP:FindByName( "TBOLT" .. tagName .. " HOT M2000 1-4")
    }
    tagName = " RED"
    local TBOLTGroupsR = {
        GROUP:FindByName( "TBOLT" .. tagName .. " 1-1"),
        GROUP:FindByName( "TBOLT" .. tagName .. " 1-2"),
        GROUP:FindByName( "TBOLT" .. tagName .. " 1-3"),
        GROUP:FindByName( "TBOLT" .. tagName .. " 1-4"),
        GROUP:FindByName( "TBOLT" .. tagName .. " HOT 1-1"),
        GROUP:FindByName( "TBOLT" .. tagName .. " HOT 1-2"),
        GROUP:FindByName( "TBOLT" .. tagName .. " HOT 1-3"),
        GROUP:FindByName( "TBOLT" .. tagName .. " HOT 1-4"),
        GROUP:FindByName( "TBOLT" .. tagName .. " M2000 1-1"),
        GROUP:FindByName( "TBOLT" .. tagName .. " M2000 1-2"),
        GROUP:FindByName( "TBOLT" .. tagName .. " M2000 1-3"),
        GROUP:FindByName( "TBOLT" .. tagName .. " M2000 1-4"),
        GROUP:FindByName( "TBOLT" .. tagName .. " HOT M2000 1-1"),
        GROUP:FindByName( "TBOLT" .. tagName .. " HOT M2000 1-2"),
        GROUP:FindByName( "TBOLT" .. tagName .. " HOT M2000 1-3"),
        GROUP:FindByName( "TBOLT" .. tagName .. " HOT M2000 1-4")
    }


    if(switch) then
        MESSAGE:New( "Mode Immortel activé !", 10 ):ToAll()
        Trainer = MISSILETRAINER
                :New( 200 )
                :InitMessagesOnOff(true)
                :InitAlertsToAll(false)
                :InitAlertsHitsOnOff(true)
                :InitAlertsLaunchesOnOff(false)
                :InitBearingOnOff(false)
                :InitRangeOnOff(false)
                :InitTrackingOnOff(false)
                :InitTrackingToAll(false)
                :InitMenusOnOff(false)

    else
        Trainer.TrackingScheduler:Stop()
        MESSAGE:New( "Mode Immortel désactivé !", 10 ):ToAll()
    end



end

local function TrackingMode( switch )
    Trainer.DetailsRangeOnOff = switch
    Trainer.DetailsBearingOnOff = switch
    Trainer.TrackingOnOff = switch
    if( switch ) then
        MESSAGE:New( "Tracking des missiles activé !", 10 ):ToAll()
    else
        MESSAGE:New( "Tracking des missiles désactivé !", 10 ):ToAll()
    end
end

local function AIFormation( team )
    local tagName = ""
    local teamName = "blue"
    local prefix = "BLUEAI"
    if (team == "R") then
        tagName = " RED"
        teamName = "red"
        prefix = "REDAI"
    end
    local AISet = SET_GROUP:New():FilterCoalitions( teamName ):FilterCategories("plane"):FilterPrefixes( prefix ):FilterStart()
    AISet:Flush()
    local LeaderUnit = UNIT:FindByName( "TBOLT" .. tagName .. " 1-1" )
    if(nil == LeaderUnit) then
        LeaderUnit = UNIT:FindByName( "TBOLT" .. tagName .. " HOT 1-1" )
    end
    local LargeFormation = AI_FORMATION:New( LeaderUnit, AISet, "Center Wing Formation", "Briefing" )
    LargeFormation:FormationCenterWing( 500, 50, 0, 0, 250, 250 )
    LargeFormation:__Start( 1 )
end

local function MissileTrainer()


end
--
-- FOX
--

--fox=FOX:New()
--
--RedZoneGroup = GROUP:FindByName( "Red Zone" )
--RedZone = ZONE_POLYGON:New( "Red Zone", RedZoneGroup )
--
--BlueZoneGroup = GROUP:FindByName( "Blue Zone" )
--BlueZone = ZONE_POLYGON:New( "Blue Zone", BlueZoneGroup )
--
--YellowZoneGroup = GROUP:FindByName( "Yellow Zone" )
--YellowZone = ZONE_POLYGON:New( "Yellow Zone", BlueZoneGroup )
--
--fox:AddSafeZone(RedZone)
--fox:AddSafeZone(BlueZone)
--fox:AddLaunchZone(YellowZone)
--fox:SetDefaultLaunchAlerts(false)
--fox:SetDefaultLaunchMarks(false)
--fox:SetDisableF10Menu(true)
--fox:Start()

--
-- Menu
--

_SETTINGS:SetPlayerMenuOff()
local MenuRed = MENU_MISSION:New( "ROUGE" )
local MenuBlue = MENU_MISSION:New( "BLEU" )
local MenuImmortal = MENU_MISSION:New( "MODE IMMORTEL" )
local MenuSupport = MENU_MISSION:New( "SUPPORT" )
--local MenuTest = MENU_MISSION:New( "TESTS" )
--local MenuScoring = MENU_MISSION:New( "SCORING" )

MENU_MISSION_COMMAND:New( "MODE IMMORTEL ON", MenuImmortal, ImmortalMode, true )
MENU_MISSION_COMMAND:New( "MODE IMMORTEL OFF", MenuImmortal, ImmortalMode, false )
MENU_MISSION_COMMAND:New( "TRACKING ON", MenuImmortal, TrackingMode, true )
MENU_MISSION_COMMAND:New( "TRACKING OFF", MenuImmortal, TrackingMode, false )

MENU_MISSION_COMMAND:New( "Mig-21", MenuRed, ActivateRedCap, "Mig-21" )
MENU_MISSION_COMMAND:New( "Su-27", MenuRed, ActivateRedCap, "Su-27" )
MENU_MISSION_COMMAND:New( "Mig-29", MenuRed, ActivateRedCap, "Mig-29" )
MENU_MISSION_COMMAND:New( "F-16", MenuRed, ActivateRedCap, "F-16" )
MENU_MISSION_COMMAND:New( "M-2000C", MenuRed, ActivateRedCap, "M-2000C" )
MENU_MISSION_COMMAND:New( "F-16 DOGFIGHT", MenuRed, ActivateRedCap, "F-16 DF" )
MENU_MISSION_COMMAND:New( "F/A-18C DOGFIGHT", MenuRed, ActivateRedCap, "F-18 DF" )
MENU_MISSION_COMMAND:New( "RESET TOUS LES ROUGES", MenuRed, KillAllRed )


MENU_MISSION_COMMAND:New( "TBOLT AI : DEPART HOT", MenuBlue, ActivateBlueAI, "HOT" )
MENU_MISSION_COMMAND:New( "TBOLT AI : DEPART COLD", MenuBlue, ActivateBlueAI, "COLD" )
MENU_MISSION_COMMAND:New( "TBOLT AI : SUIVRE TBOLT 1-1", MenuBlue, AIFormation )

MENU_MISSION_COMMAND:New( "AWACS BLEU", MenuSupport, ActivateMagic )
MENU_MISSION_COMMAND:New( "AWACS ROUGE", MenuSupport, ActivateOverlord )
MENU_MISSION_COMMAND:New( "TANKER BLEU", MenuSupport, ActivateTexaco )
MENU_MISSION_COMMAND:New( "TANKER ROUGE", MenuSupport, ActivateArco )

MENU_MISSION_COMMAND:New( "POULET BLEU", MenuTest, ActivateGroup, "poulet1" )
MENU_MISSION_COMMAND:New( "POULET ROUGE", MenuTest, ActivateGroup, "poulet2" )
MENU_MISSION_COMMAND:New( "PORC ROUGE", MenuTest, ActivateGroup, "porc1" )


PatrolZones = {}
BlueZoneGroup = GROUP:FindByName( "Blue Zone" )
BlueZone = ZONE_POLYGON:New( "Blue Zone", BlueZoneGroup )
RedZoneGroup = GROUP:FindByName( "Red Zone" )
RedZone = ZONE_POLYGON:New( "Red Zone", RedZoneGroup )
YellowZoneGroup = GROUP:FindByName( "Yellow Zone" )
YellowZone = ZONE_POLYGON:New( "Yellow Zone", YellowZoneGroup )


