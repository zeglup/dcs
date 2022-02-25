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
    MESSAGE:New( "MAGIC est actif sur 265.000Mhz", 5 ):ToAll()
    local group = GROUP:FindByName( "Magic" )
    group:Activate()
end

local function ActivateOverlord()
    MESSAGE:New( "OVERLORD est actif sur 266.000Mhz", 5 ):ToAll()
    local group = GROUP:FindByName( "Overlord" )
    group:Activate()
end

local function ActivateTexaco()
    MESSAGE:New( "TEXACO est actif : 265.000Mhz / TCN 1X A22 300kts", 10 ):ToAll()
    local group = GROUP:FindByName( "Texaco" )
    group:Activate()
end

local function ActivateArco()
    MESSAGE:New( "ARCO est actif : 266.000Mhz / TCN 2X A22 300kts", 10 ):ToAll()
    local group = GROUP:FindByName( "Arco" )
    group:Activate()
end

local function ActivateRedCap( groupName )

    local PatrolZones = {}

    US_PlanesClientSet = SET_CLIENT:New():FilterCoalitions( "blue" ):FilterCategories( "plane" ):FilterPrefixes( "TBOLT" ):FilterActive():FilterStart()

    PatrolZone = ZONE:New( "Red Zone" )
    EngageZoneGroup = GROUP:FindByName( "Yellow Zone" )
    CapEngageZone = ZONE_POLYGON:New( "Yellow Zone", EngageZoneGroup )

    RU_PlanesSpawn = SPAWN
            :NewWithAlias( groupName, "REDAI" )
            :InitRandomizeZones( { PatrolZone } )
            :OnSpawnGroup( function ( spawnGroup )

        PatrolZones[spawnGroup] = AI_CAP_ZONE:New( PatrolZone, 2000, 5000, 400, 600 )
        PatrolZones[spawnGroup]:SetControllable( spawnGroup )
        PatrolZones[spawnGroup]:SetDetectionZone( CapEngageZone )
        PatrolZones[spawnGroup]:SetEngageZone( CapEngageZone )
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

    PatrolZone = ZONE:New( "Blue Zone" )
    EngageZoneGroup = GROUP:FindByName( "Yellow Zone" )
    CapEngageZone = ZONE_POLYGON:New( "Yellow Zone", EngageZoneGroup )
    local PatrolZones = {}

    US_PlanesSpawn = SPAWN
            :NewWithAlias( "TBOLT BLUE AI " .. mode, "BLUEAI" )
            :InitCleanUp( 20 )
    local FilterName = "TBOLT"
    if (mode == "HOT") then
        FilterName = "TBOLT HOT"
    end
    US_PlanesClientSet = SET_CLIENT:New():FilterCoalitions( "blue" ):FilterCategories( "plane" ):FilterPrefixes( FilterName ):FilterStart()
    US_AI_Balancer = AI_BALANCER:New( US_PlanesClientSet, US_PlanesSpawn )
    US_AI_Balancer:InitSpawnInterval(2)
    US_AI_Balancer:ReturnToHomeAirbase( 10000 )

    function US_AI_Balancer:OnAfterSpawned( SetGroup, From, Event, To, AIGroup )

                PatrolZones[AIGroup] = AI_CAP_ZONE:New( PatrolZone, 5000, 10000, 400, 500 )
                PatrolZones[AIGroup]:SetControllable( AIGroup )
                PatrolZones[AIGroup]:SetDetectionZone( CapEngageZone )
                PatrolZones[AIGroup]:SetEngageZone( CapEngageZone )
                PatrolZones[AIGroup]:__Start( 1 )

    end
    MESSAGE:New( "TBOLT BLUE AI " .. mode .. " est actif", 10 ):ToAll()

end

local function ActivateRedAI()

    RU_PlanesClientSet = SET_CLIENT:New():FilterCountries( "Russia" ):FilterCategories( "plane" )
    RU_PlanesSpawn = SPAWN:New( "TBOLT RED AI" ):InitCleanUp( 20 )
    RU_AI_Balancer = AI_BALANCER:New( RU_PlanesClientSet, RU_PlanesSpawn )
    RU_AI_Balancer:InitSpawnInterval(5)


end

local function KillAllRed()
    RU_PlanesUnitSet = SET_UNIT:New():FilterCoalitions( "red" ):FilterCategories( "plane" ):FilterPrefixes("REDAI"):FilterActive():FilterOnce()
    RU_PlanesUnitSet:ForEachUnit(function( unitObject )
        unitObject:Destroy()
    end
    )
    MESSAGE:New( "Tous les rouges sont morts !", 10 ):ToAll()
end


local function InvincibleMode( switch )
    if(switch) then
        MESSAGE:New( "Mode Immortel activé", 10 ):ToAll()
    else
        MESSAGE:New( "Mode Immortel désactivé", 10 ):ToAll()
    end

    BlueZoneGroup = GROUP:FindByName( "Blue Zone" )
    BlueZone = ZONE_POLYGON:New( "Blue Zone", BlueZoneGroup )

    local TBOLTGroups = {
        GROUP:FindByName( "TBOLT 1-1"),
        GROUP:FindByName( "TBOLT HOT 1-1"),
        GROUP:FindByName( "TBOLT 1-2"),
        GROUP:FindByName( "TBOLT HOT 1-2"),
        GROUP:FindByName( "TBOLT 1-3"),
        GROUP:FindByName( "TBOLT HOT 1-3"),
        GROUP:FindByName( "TBOLT 1-4"),
        GROUP:FindByName( "TBOLT HOT 1-4")
    }

    local TBOLTUnits = {
        UNIT:FindByName("TBOLT 1-1"),
        UNIT:FindByName("TBOLT 1-2"),
        UNIT:FindByName("TBOLT 1-3"),
        UNIT:FindByName("TBOLT 1-4"),
        UNIT:FindByName("TBOLT HOT 1-1"),
        UNIT:FindByName("TBOLT HOT 1-2"),
        UNIT:FindByName("TBOLT HOT 1-3"),
        UNIT:FindByName("TBOLT HOT 1-4")
    }
    for i,group in pairs(TBOLTGroups) do
        if( group ~= nil) then
            group:SetCommandImmortal( switch )
        end
    end

    if( switch ) then
        for i,unit in pairs(TBOLTUnits) do
            if unit then
                unit:HandleEvent( EVENTS.Hit )
                function unit:OnEventHit( EventData )
                    if(nil == string.find(EventData.WeaponName, "weapons.shells")) then

                        MESSAGE:New( "Alerte : " .. EventData.IniTypeName .. " " .. EventData.IniUnitName .. " a tué " .. unit:GetPlayerName() .. " avec un " .. EventData.WeaponName .. " !" , 15 ):ToAll()

                        unitGroup = unit:GetGroup()
                        unitGroup:SetCommandInvisible(true)

                        MESSAGE:New( "Vous êtes mort ! Veuillez retourner en Zone Bleue", 15 ):ToGroup( unitGroup )
                    else
                        -- Hit by mike mike
                    end
                end
            end
        end

        local TestInZone = {}
        for i,group in pairs(TBOLTGroups) do
            TestInZone[group] = SCHEDULER:New( nil,
                    function()
                        if group:IsCompletelyInZone( BlueZone ) then
                            group:SetCommandInvisible(false)
                            --MESSAGE:New( "Zone Bleue atteinte, vous pouvez reprendre l'engagement",10 ):ToGroup( group )
                        end
                    end,{}, 0, 1 )
        end
    end


end

local function BlueAIFormation()
    local BlueAISet = SET_GROUP:New():FilterCoalitions("blue"):FilterCategories("plane"):FilterPrefixes("BLUEAI"):FilterStart()
    BlueAISet:Flush()
    local LeaderUnit = UNIT:FindByName( "TBOLT 1-1" )
    if(nil == LeaderUnit) then
        LeaderUnit = UNIT:FindByName( "TBOLT HOT 1-1" )
    end
    local LargeFormation = AI_FORMATION:New( LeaderUnit, BlueAISet, "Center Wing Formation", "Briefing" )
    LargeFormation:FormationCenterWing( 500, 50, 0, 0, 250, 250 )
    LargeFormation:__Start( 1 )
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
local MenuSupport = MENU_MISSION:New( "SUPPORT" )

MENU_MISSION_COMMAND:New( "Mig-21", MenuRed, ActivateRedCap, "Mig-21" )
MENU_MISSION_COMMAND:New( "Su-27", MenuRed, ActivateRedCap, "Su-27" )
MENU_MISSION_COMMAND:New( "Mig-29", MenuRed, ActivateRedCap, "Mig-29" )
MENU_MISSION_COMMAND:New( "F-16", MenuRed, ActivateRedCap, "F-16" )
MENU_MISSION_COMMAND:New( "M-2000C", MenuRed, ActivateRedCap, "M-2000C" )
MENU_MISSION_COMMAND:New( "F-16 DOGFIGHT", MenuRed, ActivateRedCap, "F-16 DF" )
MENU_MISSION_COMMAND:New( "F/A-18C DOGFIGHT", MenuRed, ActivateRedCap, "F-18 DF" )
MENU_MISSION_COMMAND:New( "RESET TOUS LES ROUGES", MenuRed, KillAllRed )

MENU_MISSION_COMMAND:New( "MODE IMMORTEL ON", MenuBlue, InvincibleMode, true )
MENU_MISSION_COMMAND:New( "MODE IMMORTEL OFF", MenuBlue, InvincibleMode, false )
MENU_MISSION_COMMAND:New( "TBOLT AI : DEPART HOT", MenuBlue, ActivateBlueAI, "HOT" )
MENU_MISSION_COMMAND:New( "TBOLT AI : DEPART COLD", MenuBlue, ActivateBlueAI, "COLD" )
MENU_MISSION_COMMAND:New( "TBOLT AI : SUIVRE TBOLT 1-1", MenuBlue, BlueAIFormation )

MENU_MISSION_COMMAND:New( "AWACS BLEU", MenuSupport, ActivateMagic )
MENU_MISSION_COMMAND:New( "AWACS ROUGE", MenuSupport, ActivateOverlord )
MENU_MISSION_COMMAND:New( "TANKER BLEU", MenuSupport, ActivateTexaco )
MENU_MISSION_COMMAND:New( "TANKER ROUGE", MenuSupport, ActivateArco )

--MENU_MISSION_COMMAND:New( "POULET BLEU", MenuTest, ActivateGroup, "poulet1" )
--MENU_MISSION_COMMAND:New( "POULET ROUGE", MenuTest, ActivateGroup, "poulet2" )
--MENU_MISSION_COMMAND:New( "PORC ROUGE", MenuTest, ActivateGroup, "porc1" )



