-- ============================================================
-- Burning Straits Campaign Persistence System
-- Loaded via DO SCRIPT FILE at mission start (T+3s)
-- Requires desanitized io and lfs in MissionScripting.lua
-- ============================================================

BS = BS or {}

-- ============================================================
-- Configuration
-- ============================================================
BS.SAVE_INTERVAL = 300  -- auto-save every 5 minutes
BS.MISSION_NUMBER = 1   -- overridden by campaign state on load

-- Groups tracked across all 5 missions (group names must match .miz)
BS.TRACKED_GROUPS = {
    "Abu Musa SA-6",
    "Abu Musa AAA",
    "Greater Tunb HAWK",
    "Qeshm SA-2",
    "Qeshm EWR",
}

-- Default state for a fresh campaign
BS.DEFAULT_STATE = {
    lastMission = 0,
    destroyedGroups = {
        ["Abu Musa SA-6"]    = false,
        ["Abu Musa AAA"]     = false,
        ["Greater Tunb HAWK"] = false,
        ["Qeshm SA-2"]       = false,
        ["Qeshm EWR"]        = false,
    },
    mig29Activated = false,
    blueLosses = 0,
    redLosses = 0,
}

-- ============================================================
-- Lua table serializer (self-contained, no dependencies)
-- ============================================================
function BS.serialize(val, indent)
    indent = indent or 0
    local pad = string.rep("    ", indent)
    local pad1 = string.rep("    ", indent + 1)

    if type(val) == "nil" then
        return "nil"
    elseif type(val) == "boolean" then
        return val and "true" or "false"
    elseif type(val) == "number" then
        return tostring(val)
    elseif type(val) == "string" then
        return string.format("%q", val)
    elseif type(val) == "table" then
        local lines = {}
        lines[#lines + 1] = "{"

        -- collect and sort keys for deterministic output
        local keys = {}
        for k in pairs(val) do
            keys[#keys + 1] = k
        end
        table.sort(keys, function(a, b)
            if type(a) == type(b) then
                return tostring(a) < tostring(b)
            end
            return type(a) < type(b)
        end)

        for _, k in ipairs(keys) do
            local v = val[k]
            local keyStr
            if type(k) == "number" then
                keyStr = "[" .. k .. "]"
            else
                keyStr = '["' .. k .. '"]'
            end
            lines[#lines + 1] = pad1 .. keyStr .. " = " .. BS.serialize(v, indent + 1) .. ","
        end

        lines[#lines + 1] = pad .. "}"
        return table.concat(lines, "\n")
    end
    return "nil"
end

-- ============================================================
-- State file path
-- ============================================================
function BS.getStatePath()
    if lfs then
        return lfs.writedir() .. "Missions/BurningStrait/campaign_state.lua"
    end
    return nil
end

function BS.ensureDir()
    if lfs then
        local dir = lfs.writedir() .. "Missions/BurningStrait"
        lfs.mkdir(lfs.writedir() .. "Missions")
        lfs.mkdir(dir)
    end
end

-- ============================================================
-- Load state from disk
-- ============================================================
function BS.loadState()
    local path = BS.getStatePath()
    if not path then
        env.warning("[BS] Cannot load state: lfs not available")
        return BS.deepCopy(BS.DEFAULT_STATE)
    end

    local f = io.open(path, "r")
    if not f then
        env.info("[BS] No saved state found, starting fresh campaign")
        return BS.deepCopy(BS.DEFAULT_STATE)
    end
    f:close()

    env.info("[BS] Loading state from: " .. path)
    local ok, stateFunc = pcall(loadfile, path)
    if ok and stateFunc then
        local ok2, state = pcall(stateFunc)
        if ok2 and type(state) == "table" then
            -- merge with defaults to handle new fields added in updates
            for k, v in pairs(BS.DEFAULT_STATE) do
                if state[k] == nil then
                    state[k] = BS.deepCopy(v)
                end
            end
            if state.destroyedGroups then
                for k, v in pairs(BS.DEFAULT_STATE.destroyedGroups) do
                    if state.destroyedGroups[k] == nil then
                        state.destroyedGroups[k] = v
                    end
                end
            end
            env.info("[BS] State loaded. Last completed mission: " .. tostring(state.lastMission))
            return state
        end
    end

    env.warning("[BS] Failed to parse state file, starting fresh")
    return BS.deepCopy(BS.DEFAULT_STATE)
end

-- ============================================================
-- Save state to disk
-- ============================================================
function BS.saveState()
    if not io or not lfs then
        env.warning("[BS] Cannot save state: io/lfs not available")
        return false
    end

    BS.ensureDir()
    local path = BS.getStatePath()

    local content = "-- Burning Straits campaign state\n"
        .. "-- Auto-generated, do not edit while mission is running\n"
        .. "return " .. BS.serialize(BS.state) .. "\n"

    local f, err = io.open(path, "w")
    if not f then
        env.error("[BS] Failed to write state: " .. tostring(err))
        return false
    end
    f:write(content)
    f:close()
    env.info("[BS] State saved to: " .. path)
    return true
end

-- ============================================================
-- Apply state: destroy groups that were killed in prior missions
-- ============================================================
function BS.applyState()
    local count = 0
    for _, name in ipairs(BS.TRACKED_GROUPS) do
        if BS.state.destroyedGroups[name] then
            local grp = Group.getByName(name)
            if grp then
                grp:destroy()
                count = count + 1
                env.info("[BS] Removed previously destroyed group: " .. name)
            else
                env.warning("[BS] Group not found in mission: " .. name)
            end
        end
    end
    return count
end

-- ============================================================
-- Show status message to players
-- ============================================================
function BS.showStatus()
    local lines = {}
    lines[#lines + 1] = "=== BURNING STRAITS CAMPAIGN ==="
    lines[#lines + 1] = "Mission: " .. tostring(BS.MISSION_NUMBER)
    lines[#lines + 1] = "Last completed: " .. tostring(BS.state.lastMission)
    lines[#lines + 1] = ""

    local active = {}
    local destroyed = {}
    for _, name in ipairs(BS.TRACKED_GROUPS) do
        if BS.state.destroyedGroups[name] then
            destroyed[#destroyed + 1] = name
        else
            active[#active + 1] = name
        end
    end

    if #destroyed > 0 then
        lines[#lines + 1] = "Threats neutralized:"
        for _, name in ipairs(destroyed) do
            lines[#lines + 1] = "  [X] " .. name
        end
    end
    if #active > 0 then
        lines[#lines + 1] = "Active threats:"
        for _, name in ipairs(active) do
            lines[#lines + 1] = "  [ ] " .. name
        end
    end

    lines[#lines + 1] = ""
    lines[#lines + 1] = "Blue losses: " .. tostring(BS.state.blueLosses)
    lines[#lines + 1] = "Red losses: " .. tostring(BS.state.redLosses)

    trigger.action.outText(table.concat(lines, "\n"), 20)
end

-- ============================================================
-- Event handler: track S_EVENT_DEAD
-- ============================================================
BS.eventHandler = {}

function BS.eventHandler:onEvent(event)
    if event.id == world.event.S_EVENT_DEAD then
        local unit = event.initiator
        if not unit then return end

        local unitName = unit:getName()
        local group = unit:getGroup()
        local groupName = group and group:getName() or "unknown"
        local coal = unit:getCoalition()

        -- Track coalition losses (2 = blue, 1 = red in DCS)
        if coal == 2 then
            BS.state.blueLosses = BS.state.blueLosses + 1
        elseif coal == 1 then
            BS.state.redLosses = BS.state.redLosses + 1
        end

        -- Check if this was a tracked group and all units are now dead
        if BS.state.destroyedGroups[groupName] ~= nil then
            local grp = Group.getByName(groupName)
            if not grp or grp:getSize() == 0 then
                BS.state.destroyedGroups[groupName] = true
                env.info("[BS] Tracked group destroyed: " .. groupName)
                trigger.action.outText(groupName .. " confirmed destroyed.", 10)
            end
        end

        env.info("[BS] Unit killed: " .. unitName .. " (group: " .. groupName .. ")")
    end
end

-- ============================================================
-- Auto-save timer callback
-- ============================================================
function BS.autoSave(_, time)
    BS.saveState()
    return time + BS.SAVE_INTERVAL
end

-- ============================================================
-- Complete mission: save final state and advance
-- ============================================================
function BS.completeMission()
    if BS._missionCompleted then return end
    BS._missionCompleted = true

    BS.state.lastMission = BS.MISSION_NUMBER
    BS.saveState()

    local msg = "=== MISSION " .. BS.MISSION_NUMBER .. " COMPLETE ===\n"
        .. "Campaign state saved.\n"
        .. "Load Mission " .. (BS.MISSION_NUMBER + 1) .. " to continue."
    trigger.action.outText(msg, 30)
    env.info("[BS] Mission " .. BS.MISSION_NUMBER .. " completed and saved.")
end

-- ============================================================
-- Deep copy utility
-- ============================================================
function BS.deepCopy(orig)
    if type(orig) ~= "table" then return orig end
    local copy = {}
    for k, v in pairs(orig) do
        copy[k] = BS.deepCopy(v)
    end
    return copy
end

-- ============================================================
-- INIT: Run on script load
-- ============================================================
function BS.init()
    -- Check for required desanitized modules
    if not io then
        trigger.action.outText(
            "[BURNING STRAITS] ERROR: 'io' module not available!\n"
            .. "Campaign persistence DISABLED.\n"
            .. "To enable: edit DCS/Scripts/MissionScripting.lua\n"
            .. "and comment out the sanitizeModule lines for 'io' and 'lfs'.\n"
            .. "See README_PERSISTENCE.md for details.",
            30
        )
        env.error("[BS] io module not available - persistence disabled")
        return
    end

    if not lfs then
        trigger.action.outText(
            "[BURNING STRAITS] ERROR: 'lfs' module not available!\n"
            .. "Campaign persistence DISABLED.\n"
            .. "To enable: edit DCS/Scripts/MissionScripting.lua\n"
            .. "and comment out the sanitizeModule lines for 'io' and 'lfs'.",
            30
        )
        env.error("[BS] lfs module not available - persistence disabled")
        return
    end

    -- Load campaign state
    BS.state = BS.loadState()

    -- Apply state (remove groups destroyed in previous missions)
    local removed = BS.applyState()

    -- Show campaign status to players
    BS.showStatus()

    -- Register event handler
    world.addEventHandler(BS.eventHandler)
    env.info("[BS] Event handler registered")

    -- Start auto-save timer
    timer.scheduleFunction(BS.autoSave, nil, timer.getTime() + BS.SAVE_INTERVAL)
    env.info("[BS] Auto-save scheduled every " .. BS.SAVE_INTERVAL .. "s")

    env.info("[BS] Persistence system initialized. Removed " .. removed .. " groups from prior missions.")
end

-- Run init
BS.init()
