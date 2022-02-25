--
-- Menu
--

_SETTINGS:SetPlayerMenuOff()
local MenuAwacs = MENU_COALITION:New( coalition.side.BLUE, "AWACS" )
local MenuTanker = MENU_COALITION:New( coalition.side.BLUE, "Tanker" )
local MenuCap = MENU_COALITION:New( coalition.side.BLUE, "CAP" )
local MenuSead = MENU_COALITION:New( coalition.side.BLUE, "SEAD" )
local MenuTba = MENU_COALITION:New( coalition.side.BLUE, "TBA" )
local MenuSamOptions = MENU_COALITION:New( coalition.side.BLUE, "Options", MenuSead )

local MenuRestart


local function StartGroup( groupName )
	MESSAGE:New( groupName .. " DEPART EN COURS", 5 ):ToBlue()
	local group = GROUP:FindByName( groupName )
	group:StartUncontrolled()
end

local function ActiveGroup( groupName )
	local group = GROUP:FindByName( groupName )
	group:Activate()
end

local function ActiveRoeOffensive( groupName )
	local group = GROUP:FindByName( groupName )
	group:OptionROEOpenFireWeaponFree()
end

local function ActiveRoeHold( groupName )
	local group = GROUP:FindByName( groupName )
	group:OptionROEHoldFire()
end

local function ActiveSam()
    ActiveGroup("RU2_SA2")
    ActiveGroup("RU2_SA3")
    ActiveGroup("RU2_SA6")
    ActiveGroup("RU2_SA11")
    ActiveGroup("RU2_SA15")
    ActiveGroup("RU2_SA19")
	MESSAGE:New( "SAM ACTIF", 5 ):ToBlue()
end

local function ActiveRadar()
	ActiveGroup("SA6 0 TBA")
	MESSAGE:New( "RADAR ACTIF", 5 ):ToBlue()
end

local function ActiveSmoke()
	--local static = STATIC:FindByName( "Static Ammo-T1" )
	--local positionObject = static:GetDCSObject()
	--local position = positionObject:getPosition()
	--local coords = COORDINATE.NewFromVec3(position)
	--coords:SmokeGreen()
	MESSAGE:New( "FUMEE ACTIVE", 5 ):ToBlue()
	trigger.action.setUserFlag (81, 2)
end

local function ActiveAA()
	ActiveGroup("MANPAD")
	ActiveGroup("ZU23")
	MESSAGE:New( "DEFENSE AA ACTIVE", 5 ):ToBlue()
end

local function RoeOffensive()
	ActiveRoeOffensive("RU2_SA2")
    ActiveRoeOffensive("RU2_SA3")
    ActiveRoeOffensive("RU2_SA6")
    ActiveRoeOffensive("RU2_SA11")
    ActiveRoeOffensive("RU2_SA15")
    ActiveRoeOffensive("RU2_SA19")
	MESSAGE:New( "SAM ROE OFFENSIF", 5 ):ToBlue()
	--trigger.action.setUserFlag (51, 1)
end

local function RoeHold()
	ActiveRoeHold("RU2_SA2")
    ActiveRoeHold("RU2_SA3")
    ActiveRoeHold("RU2_SA6")
    ActiveRoeHold("RU2_SA11")
    ActiveRoeHold("RU2_SA15")
    ActiveRoeHold("RU2_SA19")
	MESSAGE:New( "SAM ROE HOLD", 5 ):ToBlue()
	--trigger.action.setUserFlag (51, 5)
end

local function AntiMslOn()
	MESSAGE:New( "SAM ANTI-MISSILE ON", 5 ):ToBlue()
	trigger.action.setUserFlag (61, 3)
end

local function AntiMslOff()
	MESSAGE:New( "SAM ANTI-MISSILE OFF", 5 ):ToBlue()
	trigger.action.setUserFlag (61, 4)
end

local function RestartMission()
	MESSAGE:New( "RESTART MISSION DANS 5 MINUTES", 5 ):ToBlue()
	trigger.action.setUserFlag (92, 1)
end

local function AddRestartMenu()
	MENU_COALITION_COMMAND:New( coalition.side.BLUE, "Restart mission", nil, RestartMission)
end

--
-- Overlord, Texaco
--
local CommandAwacsStart = MENU_COALITION_COMMAND:New( coalition.side.BLUE, "Départ Overlord", MenuAwacs, StartGroup, "Overlord" )
local CommandTankerStart = MENU_COALITION_COMMAND:New( coalition.side.BLUE, "Départ Texaco", MenuTanker, StartGroup, "Texaco" )

---
--- SEAD
---
local CommandActiveSam = MENU_COALITION_COMMAND:New( coalition.side.BLUE, "Activation SAM", MenuSead, ActiveSam )
local CommandRoeOffensive = MENU_COALITION_COMMAND:New( coalition.side.BLUE, "ROE Offensif", MenuSamOptions, RoeOffensive )
local CommandRoeHold = MENU_COALITION_COMMAND:New( coalition.side.BLUE, "ROE Hold", MenuSamOptions, RoeHold )
local CommandAntiOn = MENU_COALITION_COMMAND:New( coalition.side.BLUE, "Anti missile ON", MenuSamOptions, AntiMslOn )
local CommandAntiOff = MENU_COALITION_COMMAND:New( coalition.side.BLUE, "Anti missile OFF", MenuSamOptions, AntiMslOff )

---
--- CAP
---
local CommandActiveMig212 = MENU_COALITION_COMMAND:New( coalition.side.BLUE, "Mig-21*2", MenuCap, StartGroup, "Mig-21*2" )
local CommandActiveF4 = MENU_COALITION_COMMAND:New( coalition.side.BLUE, "F-4E", MenuCap, StartGroup, "F-4E" )
local CommandActiveF16df = MENU_COALITION_COMMAND:New( coalition.side.BLUE, "F-16 DF", MenuCap, StartGroup, "F-16 DF" )
local CommandActiveF18df = MENU_COALITION_COMMAND:New( coalition.side.BLUE, "F/A-18 DF", MenuCap, StartGroup, "F/A-18 DF" )
local CommandActiveF18bvr = MENU_COALITION_COMMAND:New( coalition.side.BLUE, "F/A-18 BVR", MenuCap, StartGroup, "F/A-18 BVR" )
local CommandActiveSu27 = MENU_COALITION_COMMAND:New( coalition.side.BLUE, "Su-27", MenuCap, StartGroup, "Su-27" )
local CommandActiveMig29 = MENU_COALITION_COMMAND:New( coalition.side.BLUE, "Mig-29", MenuCap, StartGroup, "Mig-29" )
local CommandActiveMi8 = MENU_COALITION_COMMAND:New( coalition.side.BLUE, "Mi-8*3", MenuCap, StartGroup, "Mi-8*3" )

---
--- TBA
---
local CommandActiveRadar = MENU_COALITION_COMMAND:New( coalition.side.BLUE, "Activation du radar", MenuTba, ActiveRadar )
local CommandActiveSmoke = MENU_COALITION_COMMAND:New( coalition.side.BLUE, "Fumée sur objectif", MenuTba, ActiveSmoke )
local CommandActiveAA = MENU_COALITION_COMMAND:New( coalition.side.BLUE, "Activation des défenses AA", MenuTba, ActiveAA )

---
--- Restart mission
---
local SchedulerAddRestart = SCHEDULER:New( nil, AddRestartMenu, {}, 1800 )


--
-- Rescue Helos
--

local RescueHeloRoosevelt = RESCUEHELO:New("Roosevelt", "Rescue Helo")
RescueHeloRoosevelt:Start()

local RescueHeloStennis = RESCUEHELO:New("Stennis", "Rescue Helo")
RescueHeloStennis:Start()

UNIT:FindByName("Roosevelt"):PatrolRoute()
UNIT:FindByName("Stennis"):PatrolRoute()
