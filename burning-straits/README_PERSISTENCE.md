# Burning Straits Campaign Persistence

## Overview

The persistence system saves mission outcomes (destroyed SAMs, EWR status, losses) to a file between missions, so Mission 2's battlefield reflects what happened in Mission 1.

## Server Setup

### 1. Desanitize MissionScripting.lua

Edit the file at:
```
<DCS Install>/Scripts/MissionScripting.lua
```

Comment out (add `--` before) these three lines:

```lua
-- sanitizeModule('io')
-- sanitizeModule('lfs')
-- _G['io'] = nil
```

**Before:**
```lua
sanitizeModule('io')
sanitizeModule('lfs')
_G['io'] = nil
```

**After:**
```lua
--sanitizeModule('io')
--sanitizeModule('lfs')
--_G['io'] = nil
```

Save and restart DCS.

### 2. Verify

Load any Burning Straits mission. You should see a campaign status message at mission start showing active/neutralized threats. If you see an error about `io` or `lfs` not being available, the desanitization didn't work.

## State File

Campaign state is saved at:
```
<Saved Games>/DCS/Missions/BurningStrait/campaign_state.lua
```

The file is auto-saved every 5 minutes and when a mission is completed.

## Resetting the Campaign

Delete the state file to start fresh:
```
<Saved Games>/DCS/Missions/BurningStrait/campaign_state.lua
```

Or delete the entire directory:
```
<Saved Games>/DCS/Missions/BurningStrait/
```

## How It Works

1. Each mission loads `persistence.lua` at T+3 seconds
2. The script reads the saved campaign state
3. Groups destroyed in previous missions are removed from the current mission
4. An event handler tracks unit deaths during gameplay
5. When primary objectives are met, `BS.completeMission()` saves state and advances the mission counter
6. Players see a status overlay showing which threats are active vs neutralized

## Mission Completion Criteria

Mission 1 (Sledgehammer): Destroy Abu Musa SA-6 (group 20) AND Greater Tunb HAWK (group 22)

## Tracked Groups

| Group | Type | Present in Missions |
|-------|------|-------------------|
| Abu Musa SA-6 | SAM | 1-5 |
| Abu Musa AAA | AAA | 1-5 |
| Greater Tunb HAWK | SAM | 1-5 |
| Qeshm SA-2 | SAM | 1-5 |
| Qeshm EWR | EWR | 1-5 |
