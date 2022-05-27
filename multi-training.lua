--
-- Menu
--

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


local function ActiveMANPADS()
	ActiveGroup("MANPAD1")
	ActiveGroup("MANPAD2")
	ActiveGroup("ZU23")
	MESSAGE:New( "DEFENSE MANPADS ACTIVE", 5 ):ToBlue()
end

local function ActiveAAA()
	ActiveGroup("ZU231")
	ActiveGroup("ZU232")
	MESSAGE:New( "DEFENSE AAA ACTIVE", 5 ):ToBlue()
end

local function RoeOffensive()
	ActiveRoeOffensive("RU2_SA2")
    ActiveRoeOffensive("RU2_SA3")
    ActiveRoeOffensive("RU2_SA6")
    ActiveRoeOffensive("RU2_SA11")
    ActiveRoeOffensive("RU2_SA15")
    ActiveRoeOffensive("RU2_SA19")
	MESSAGE:New( "SAM ROE OFFENSIF", 5 ):ToBlue()
end

local function RoeHold()
	ActiveRoeHold("RU2_SA2")
    ActiveRoeHold("RU2_SA3")
    ActiveRoeHold("RU2_SA6")
    ActiveRoeHold("RU2_SA11")
    ActiveRoeHold("RU2_SA15")
    ActiveRoeHold("RU2_SA19")
	MESSAGE:New( "SAM ROE HOLD", 5 ):ToBlue()
end

local function ActiveSmoke()
	MESSAGE:New( "FUMEE ACTIVE", 5 ):ToBlue()
	trigger.action.setUserFlag (81, 2)
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

_SETTINGS:SetPlayerMenuOff()
local MenuSupport = MENU_COALITION:New( coalition.side.BLUE, "SUPPORT" )
local MenuCap = MENU_COALITION:New( coalition.side.BLUE, "CAP" )
local MenuSead = MENU_COALITION:New( coalition.side.BLUE, "SEAD" )
local MenuTba = MENU_COALITION:New( coalition.side.BLUE, "TBA" )


---
--- AWACS, Tanker
---
MENU_COALITION_COMMAND:New( coalition.side.BLUE, "Départ Overlord", MenuSupport, StartGroup, "Overlord" )
MENU_COALITION_COMMAND:New( coalition.side.BLUE, "Départ Texaco", MenuSupport, StartGroup, "Texaco" )
MENU_COALITION_COMMAND:New( coalition.side.BLUE, "Départ Arco", MenuSupport, StartGroup, "Arco" )

---
--- SEAD
---
MENU_COALITION_COMMAND:New( coalition.side.BLUE, "Activation SAM", MenuSead, ActiveSam )
MENU_COALITION_COMMAND:New( coalition.side.BLUE, "ROE Offensif", MenuSead, RoeOffensive )
MENU_COALITION_COMMAND:New( coalition.side.BLUE, "ROE Hold", MenuSead, RoeHold )
MENU_COALITION_COMMAND:New( coalition.side.BLUE, "Anti missile ON", MenuSead, AntiMslOn )
MENU_COALITION_COMMAND:New( coalition.side.BLUE, "Anti missile OFF", MenuSead, AntiMslOff )

---
--- CAP
--- 
MENU_COALITION_COMMAND:New( coalition.side.BLUE, "Mig-21*2", MenuCap, StartGroup, "Mig-21*2" )
MENU_COALITION_COMMAND:New( coalition.side.BLUE, "F-4E", MenuCap, StartGroup, "F-4E" )
MENU_COALITION_COMMAND:New( coalition.side.BLUE, "F-16 DF", MenuCap, StartGroup, "F-16 DF" )
MENU_COALITION_COMMAND:New( coalition.side.BLUE, "F/A-18 DF", MenuCap, StartGroup, "F/A-18 DF" )
MENU_COALITION_COMMAND:New( coalition.side.BLUE, "F/A-18 BVR", MenuCap, StartGroup, "F/A-18 BVR" )
MENU_COALITION_COMMAND:New( coalition.side.BLUE, "Su-27", MenuCap, StartGroup, "Su-27" )
MENU_COALITION_COMMAND:New( coalition.side.BLUE, "Mig-29", MenuCap, StartGroup, "Mig-29" )
MENU_COALITION_COMMAND:New( coalition.side.BLUE, "Mi-8*3", MenuCap, StartGroup, "Mi-8*3" )

---
--- TBA
---
MENU_COALITION_COMMAND:New( coalition.side.BLUE, "Activation du radar de tracking", MenuTba, ActiveRadar )
MENU_COALITION_COMMAND:New( coalition.side.BLUE, "Fumée sur objectif", MenuTba, ActiveSmoke )
MENU_COALITION_COMMAND:New( coalition.side.BLUE, "Activation MANPADS", MenuTba, ActiveMANPADS )
MENU_COALITION_COMMAND:New( coalition.side.BLUE, "Activation AAA", MenuTba, ActiveAAA )


---
--- Restart mission
---
local SchedulerAddRestart = SCHEDULER:New( nil, AddRestartMenu, {}, 1800, 0 )


---
--- Rescue Helos
---

local RescueHeloRoosevelt = RESCUEHELO:New("Roosevelt", "Rescue Helo")
RescueHeloRoosevelt:SetOffsetX(100)
RescueHeloRoosevelt:SetOffsetZ(-300)
RescueHeloRoosevelt:Start()


local RescueHeloStennis = RESCUEHELO:New("Stennis", "Rescue Helo")
RescueHeloStennis:SetOffsetX(100)
RescueHeloStennis:SetOffsetZ(-300)
RescueHeloStennis:Start()

