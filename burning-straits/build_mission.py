#!/usr/bin/env python3
"""Build Burning Straits campaign .miz files (Missions 1-5)."""

import os
import zipfile

OUT_DIR = os.path.dirname(os.path.abspath(__file__))


# ============================================================
# DCS-native Lua serializer
# Matches the exact format DCS Mission Editor produces:
#   ["key"] = value,
#   -- end of ["key"]
# ============================================================
def lua_value(val, indent=0):
    """Serialize a Python value to DCS-native Lua string."""
    tab = "\t" * indent

    if isinstance(val, dict):
        if not val:
            return "{}"
        lines = []
        lines.append("")  # newline before opening brace
        lines.append(tab + "{")
        items = list(val.items())
        for key, v in items:
            if isinstance(key, int):
                kstr = f"[{key}]"
            else:
                kstr = f'["{key}"]'
            vstr = lua_value(v, indent + 1)
            if isinstance(v, dict) and v:
                lines.append(f"{tab}\t{kstr} = {vstr}")
                lines.append(f"{tab}\t}}, -- end of {kstr}")
            else:
                lines.append(f"{tab}\t{kstr} = {vstr},")
        # Fix: the dict closing brace is handled by the caller
        # Remove trailing lines and close
        # Actually, we need to return the content between { and }
        result = "\n".join(lines)
        return result + "\n" + tab + "}"

    elif isinstance(val, bool):
        return "true" if val else "false"

    elif isinstance(val, int):
        return str(val)

    elif isinstance(val, float):
        if val == int(val) and abs(val) < 1e15:
            return str(int(val))
        return str(val)

    elif isinstance(val, str):
        escaped = val.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
        return f'"{escaped}"'

    else:
        return str(val)


def lua_serialize(data, varname, indent=0):
    """Serialize a top-level dict to DCS Lua format."""
    tab = "\t" * indent
    lines = [f"{varname} = "]
    lines.append("{")

    items = list(data.items())
    for key, val in items:
        if isinstance(key, int):
            kstr = f"[{key}]"
        else:
            kstr = f'["{key}"]'

        vstr = _serialize_val(val, 1)
        if isinstance(val, dict) and val:
            lines.append(f"\t{kstr} = ")
            lines.append("\t{")
            _dict_body(val, 2, lines)
            lines.append(f"\t}}, -- end of {kstr}")
        else:
            lines.append(f"\t{kstr} = {vstr},")

    lines.append(f"}} -- end of {varname}")
    return "\n".join(lines) + "\n"


def _serialize_val(val, indent):
    """Serialize a single value."""
    if isinstance(val, dict):
        if not val:
            return "{}"
        return None  # handled by caller
    elif isinstance(val, bool):
        return "true" if val else "false"
    elif isinstance(val, int):
        return str(val)
    elif isinstance(val, float):
        if val == int(val) and abs(val) < 1e15:
            return str(int(val))
        return str(val)
    elif isinstance(val, str):
        escaped = val.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
        return f'"{escaped}"'
    return str(val)


def _dict_body(data, indent, lines):
    """Write the contents of a dict (between { and })."""
    tab = "\t" * indent
    for key, val in data.items():
        if isinstance(key, int):
            kstr = f"[{key}]"
        else:
            kstr = f'["{key}"]'

        if isinstance(val, dict) and val:
            lines.append(f"{tab}{kstr} = ")
            lines.append(f"{tab}{{")
            _dict_body(val, indent + 1, lines)
            lines.append(f"{tab}}}, -- end of {kstr}")
        else:
            vstr = _serialize_val(val, indent)
            lines.append(f"{tab}{kstr} = {vstr},")


def to_lua(data, varname):
    """Top-level serializer matching DCS ME native output."""
    lines = []
    lines.append(f"{varname} = ")
    lines.append("{")
    _dict_body(data, 1, lines)
    lines.append(f"}} -- end of {varname}")
    return "\n".join(lines) + "\n"


# ============================================================
# Constants
# ============================================================
AIM9M = "{6CEB49FC-DED8-4DED-B053-E1F033FF72D3}"
AGM88 = "{B06DD79A-F21E-4EB9-BD9D-AB3844618C93}"
FT370 = "{F376DBEE-4CAE-41BA-ADD9-B2910AC95DEC}"

AL_DHAFRA_X, AL_DHAFRA_Y = -174571, -211656
ABU_MUSA_X, ABU_MUSA_Y = -13000, -140000
GREATER_TUNB_X, GREATER_TUNB_Y = 26000, -99000
QESHM_X, QESHM_Y = 79000, -13000
BANDAR_X, BANDAR_Y = 116587, 57590
AIRDROME_AL_DHAFRA = 4

# Ship positions
CARRIER_X, CARRIER_Y = -80000, -240000   # CVN-74, Gulf of Oman
FRIGATE_X, FRIGATE_Y = -40000, -180000   # DDG-62, Strait patrol

# Ship unit IDs (referenced by aircraft for carrier/deck ops)
CVN74_ID = 1001
DDG62_ID = 1101


# ============================================================
# Helpers
# ============================================================
def make_waypoint(x, y, alt, speed, name, wp_type="Turning Point",
                  action="Turning Point", alt_type="BARO", eta=0,
                  eta_locked=False, tasks=None, airdrome_id=None,
                  helipad_id=None, link_unit=None):
    wp = {
        "alt": alt,
        "action": action,
        "alt_type": alt_type,
        "speed": speed,
        "task": {
            "id": "ComboTask",
            "params": {
                "tasks": tasks if tasks else {},
            },
        },
        "type": wp_type,
        "ETA": eta,
        "ETA_locked": eta_locked,
        "y": y,
        "x": x,
        "speed_locked": True,
        "formation_template": "",
        "name": name,
    }
    if airdrome_id is not None:
        wp["airdromeId"] = airdrome_id
    if helipad_id is not None:
        wp["helipadId"] = helipad_id
    if link_unit is not None:
        wp["linkUnit"] = link_unit
    return wp


def make_air_unit(unit_id, name, utype, x, y, alt, heading, speed, skill,
                  onboard_num, callsign, payload, alt_type="BARO", props=None):
    return {
        "alt": alt,
        "alt_type": alt_type,
        "livery_id": "default",
        "skill": skill,
        "speed": speed,
        "type": utype,
        "unitId": unit_id,
        "psi": -heading if heading != 0 else 0,
        "onboard_num": onboard_num,
        "x": x,
        "y": y,
        "name": name,
        "payload": payload,
        "heading": heading,
        "callsign": callsign,
        "AddPropAircraft": props if props else {},
    }


def make_air_group(group_id, name, freq, task, x, y, units, waypoints,
                   late_activation=False):
    return {
        "modulation": 0,
        "tasks": {},
        "radioSet": False,
        "task": task,
        "uncontrolled": False,
        "taskSelected": True,
        "route": {
            "routeRelativeTOT": True,
            "points": {i+1: wp for i, wp in enumerate(waypoints)},
        },
        "groupId": group_id,
        "hidden": False,
        "units": {i+1: u for i, u in enumerate(units)},
        "y": y,
        "x": x,
        "name": name,
        "communication": True,
        "start_time": 0,
        "frequency": freq,
        "lateActivation": late_activation,
    }


def make_ground_unit(unit_id, name, utype, x, y, heading=0, skill="Average"):
    return {
        "unitId": unit_id,
        "type": utype,
        "name": name,
        "x": x,
        "y": y,
        "heading": heading,
        "skill": skill,
        "playerCanDrive": False,
    }


def make_ground_group(group_id, name, x, y, units):
    return {
        "visible": False,
        "tasks": {},
        "uncontrollable": False,
        "task": "Ground Nothing",
        "taskSelected": True,
        "route": {
            "spans": {},
            "points": {
                1: {
                    "alt": 0,
                    "type": "Turning Point",
                    "action": "Off Road",
                    "alt_type": "BARO",
                    "ETA": 0,
                    "ETA_locked": True,
                    "y": y,
                    "x": x,
                    "speed": 0,
                    "speed_locked": True,
                    "formation_template": "",
                    "task": {
                        "id": "ComboTask",
                        "params": {"tasks": {}},
                    },
                },
            },
        },
        "groupId": group_id,
        "hidden": False,
        "dead": False,
        "units": {i+1: u for i, u in enumerate(units)},
        "y": y,
        "x": x,
        "name": name,
        "start_time": 0,
        "lateActivation": False,
    }


def make_ship_unit(unit_id, name, utype, x, y, heading=0):
    return {
        "unitId": unit_id,
        "type": utype,
        "name": name,
        "x": x,
        "y": y,
        "heading": heading,
        "skill": "Average",
        "transportable": {"randomTransportable": False},
    }


def make_ship_group(group_id, name, x, y, units, waypoints=None, speed=5):
    if waypoints is None:
        waypoints = [
            make_waypoint(x, y, 0, speed, "WP1", eta_locked=True),
        ]
    return {
        "visible": True,
        "tasks": {},
        "uncontrollable": False,
        "task": "Nothing",
        "taskSelected": True,
        "route": {
            "routeRelativeTOT": True,
            "points": {i+1: wp for i, wp in enumerate(waypoints)},
        },
        "groupId": group_id,
        "hidden": False,
        "units": {i+1: u for i, u in enumerate(units)},
        "y": y,
        "x": x,
        "name": name,
        "communication": True,
        "start_time": 0,
        "frequency": 127,
    }


# ============================================================
# Payloads
# ============================================================
F16_SEAD_PAYLOAD = {
    "pylons": {
        1: {"CLSID": AIM9M},
        3: {"CLSID": AGM88},
        5: {"CLSID": FT370},
        7: {"CLSID": AGM88},
        9: {"CLSID": AIM9M},
    },
    "fuel": 3249,
    "flare": 60,
    "chaff": 60,
    "gun": 100,
}

FA18_PAYLOAD = {
    "pylons": {
        1: {"CLSID": AIM9M},
        9: {"CLSID": AIM9M},
    },
    "fuel": 4900,
    "flare": 60,
    "chaff": 60,
    "gun": 100,
}

M2000_PAYLOAD = {
    "pylons": {},
    "fuel": 3165,
    "flare": 32,
    "chaff": 48,
    "gun": 100,
}

AH64_PAYLOAD = {
    "pylons": {},
    "fuel": 1524,
    "flare": 60,
    "chaff": 60,
    "gun": 100,
}

F15_PAYLOAD = {
    "pylons": {
        1: {"CLSID": AIM9M},
        9: {"CLSID": AIM9M},
    },
    "fuel": 6103,
    "flare": 60,
    "chaff": 120,
    "gun": 100,
}

E3A_PAYLOAD = {"pylons": {}, "fuel": 65000, "flare": 0, "chaff": 0, "gun": 0}
KC135_PAYLOAD = {"pylons": {}, "fuel": 90700, "flare": 0, "chaff": 0, "gun": 0}
MIG29_PAYLOAD = {"pylons": {}, "fuel": 3376, "flare": 60, "chaff": 60, "gun": 100}


# ============================================================
# BLUE AIR GROUPS
# ============================================================

# WARHAWKS 1 (F-16C, Player SEAD — cold start Al Dhafra)
warhawks = make_air_group(1, "WARHAWKS 1", 305, "SEAD",
    AL_DHAFRA_X, AL_DHAFRA_Y,
    [make_air_unit(101, "WARHAWKS 1-1", "F-16C_50",
                   AL_DHAFRA_X, AL_DHAFRA_Y, 25,
                   0.785, 0, "Player", "010",
                   {1: 4, 2: 1, 3: 1, "name": "WARHAWKS11"}, F16_SEAD_PAYLOAD)],
    [make_waypoint(AL_DHAFRA_X, AL_DHAFRA_Y, 25, 0, "AL DHAFRA",
                   wp_type="TakeOffParking", action="From Parking Area",
                   eta_locked=True, airdrome_id=AIRDROME_AL_DHAFRA),
     make_waypoint(-30000, -155000, 5486, 210, "PUSH", tasks={
         1: {"enabled": True, "auto": False, "id": "EngageTargets", "number": 1,
             "params": {"targetTypes": {1: "Air Defence"}, "priority": 0}}}),
     make_waypoint(ABU_MUSA_X, ABU_MUSA_Y, 5486, 210, "ABU MUSA"),
     make_waypoint(GREATER_TUNB_X, GREATER_TUNB_Y, 5486, 210, "GREATER TUNB"),
     make_waypoint(AL_DHAFRA_X, AL_DHAFRA_Y, 25, 80, "RTB AL DHAFRA",
                   wp_type="Land", action="Landing", airdrome_id=AIRDROME_AL_DHAFRA)])

# BLACKSHEEP 1 (F/A-18C x4, Client DEAD — cold start CVN-74)
bs_units = []
for i in range(4):
    bs_units.append(make_air_unit(
        201+i, f"BLACKSHEEP 1-{i+1}", "FA-18C_hornet",
        CARRIER_X, CARRIER_Y, 20,
        0.785, 0, "Client", f"10{i+1}",
        {1: 5, 2: 1, 3: i+1, "name": f"BLACKSHEEP1{i+1}"}, FA18_PAYLOAD))

blacksheep = make_air_group(2, "BLACKSHEEP 1", 270, "Ground Attack",
    CARRIER_X, CARRIER_Y, bs_units,
    [make_waypoint(CARRIER_X, CARRIER_Y, 20, 0, "CVN-74 STENNIS",
                   wp_type="TakeOffParkingHot", action="From Parking Area Hot",
                   eta_locked=True, helipad_id=CVN74_ID, link_unit=CVN74_ID),
     make_waypoint(-25000, -152000, 6096, 210, "PUSH"),
     make_waypoint(-18000, -145000, 5000, 200, "IP"),
     make_waypoint(ABU_MUSA_X, ABU_MUSA_Y, 5000, 200, "ABU MUSA - BOMB SA-6", tasks={
         1: {"enabled": True, "auto": False, "id": "Bombing", "number": 1,
             "params": {"direction": 0, "attackQtyLimit": False, "attackQty": 4,
                        "expend": "All", "y": ABU_MUSA_Y, "groupAttack": True,
                        "altitude": 5000, "directionEnabled": False,
                        "weaponType": 2147485694, "x": ABU_MUSA_X}}}),
     make_waypoint(CARRIER_X, CARRIER_Y, 20, 80, "RTB CARRIER",
                   wp_type="Land", action="Landing",
                   helipad_id=CVN74_ID, link_unit=CVN74_ID)])

# WITCHER (M-2000C, Client sweep — cold start Al Dhafra)
witcher = make_air_group(3, "WITCHER 1", 290, "CAP",
    AL_DHAFRA_X, AL_DHAFRA_Y,
    [make_air_unit(301, "WITCHER 1-1", "M-2000C",
                   AL_DHAFRA_X, AL_DHAFRA_Y, 25,
                   0.785, 0, "Client", "201",
                   {1: 7, 2: 1, 3: 1, "name": "WITCHER11"}, M2000_PAYLOAD)],
    [make_waypoint(AL_DHAFRA_X, AL_DHAFRA_Y, 25, 0, "AL DHAFRA",
                   wp_type="TakeOffParking", action="From Parking Area",
                   eta_locked=True, airdrome_id=AIRDROME_AL_DHAFRA),
     make_waypoint(-25000, -145000, 7000, 230, "SWEEP"),
     make_waypoint(GREATER_TUNB_X, GREATER_TUNB_Y, 6096, 220, "GREATER TUNB AREA"),
     make_waypoint(QESHM_X, QESHM_Y, 5000, 210, "OPT: QESHM EWR"),
     make_waypoint(AL_DHAFRA_X, AL_DHAFRA_Y, 25, 80, "RTB",
                   wp_type="Land", action="Landing", airdrome_id=AIRDROME_AL_DHAFRA)])

# OUTLAWS (AH-64D x2, Client CAS — cold start DDG-62)
outlaws = make_air_group(4, "OUTLAWS 1", 124, "CAS",
    FRIGATE_X, FRIGATE_Y,
    [make_air_unit(401, "OUTLAWS 1-1", "AH-64D_BLK_II",
                   FRIGATE_X, FRIGATE_Y, 10,
                   0.785, 0, "Client", "301",
                   {1: 9, 2: 1, 3: 1, "name": "OUTLAWS11"}, AH64_PAYLOAD,
                   props={"HumanOrchestra": False}),
     make_air_unit(402, "OUTLAWS 1-2", "AH-64D_BLK_II",
                   FRIGATE_X, FRIGATE_Y, 10,
                   0.785, 0, "Client", "302",
                   {1: 9, 2: 1, 3: 2, "name": "OUTLAWS12"}, AH64_PAYLOAD,
                   props={"HumanOrchestra": False})],
    [make_waypoint(FRIGATE_X, FRIGATE_Y, 10, 0, "DDG-62 FITZGERALD",
                   wp_type="TakeOffParkingHot", action="From Parking Area Hot",
                   eta_locked=True, helipad_id=DDG62_ID, link_unit=DDG62_ID),
     make_waypoint(-25000, -148000, 100, 55, "INGRESS LOW"),
     make_waypoint(-15000, -142000, 50, 50, "OPT: ABU MUSA AAA"),
     make_waypoint(FRIGATE_X, FRIGATE_Y, 10, 50, "RTB DDG-62",
                   wp_type="Land", action="Landing",
                   helipad_id=DDG62_ID, link_unit=DDG62_ID)])

# PANTHER 1 (F-15C x2, AI Sweep)
panther = make_air_group(5, "PANTHER 1", 325, "CAP", -10000, -150000,
    [make_air_unit(501, "PANTHER 1-1", "F-15C", -10000, -150000, 7620,
                   0.785, 240, "High", "401",
                   {1: 8, 2: 1, 3: 1, "name": "PANTHER11"}, F15_PAYLOAD),
     make_air_unit(502, "PANTHER 1-2", "F-15C", -9970, -149970, 7620,
                   0.785, 240, "High", "402",
                   {1: 8, 2: 1, 3: 2, "name": "PANTHER12"}, F15_PAYLOAD)],
    [make_waypoint(-10000, -150000, 7620, 240, "SWEEP START", eta_locked=True,
                   tasks={1: {"enabled": True, "auto": False, "id": "EngageTargets",
                              "number": 1,
                              "params": {"targetTypes": {1: "Planes"}, "priority": 0}}}),
     make_waypoint(30000, -110000, 7620, 240, "SWEEP END / CAP"),
     make_waypoint(AL_DHAFRA_X, AL_DHAFRA_Y, 25, 80, "RTB",
                   wp_type="Land", action="Landing", airdrome_id=AIRDROME_AL_DHAFRA)])

# OVERLORD (E-3A, AI AWACS)
overlord = make_air_group(6, "OVERLORD", 251, "AWACS", -100000, -185000,
    [make_air_unit(601, "OVERLORD", "E-3A", -100000, -185000, 9144,
                   0, 130, "High", "500",
                   {1: 1, 2: 1, 3: 1, "name": "OVERLORD"}, E3A_PAYLOAD)],
    [make_waypoint(-100000, -185000, 9144, 130, "ORBIT 1", eta_locked=True,
                   tasks={1: {"enabled": True, "auto": False, "id": "AWACS",
                              "number": 1, "params": {}},
                          2: {"enabled": True, "auto": False, "id": "Orbit",
                              "number": 2, "params": {"altitude": 9144,
                              "pattern": "Race-Track", "speed": 130,
                              "speedEdited": True}}}),
     make_waypoint(-85000, -170000, 9144, 130, "ORBIT 2")])

# SHELL 1 (KC-135, AI Tanker)
shell = make_air_group(7, "SHELL 1", 317, "Refueling", -130000, -200000,
    [make_air_unit(701, "SHELL 1-1", "KC135MPRS", -130000, -200000, 6706,
                   0.785, 150, "High", "600",
                   {1: 3, 2: 1, 3: 1, "name": "SHELL11"}, KC135_PAYLOAD)],
    [make_waypoint(-130000, -200000, 6706, 150, "TRACK EXXON 1", eta_locked=True,
                   tasks={1: {"enabled": True, "auto": False, "id": "Tanker",
                              "number": 1, "params": {}},
                          2: {"enabled": True, "auto": False, "id": "Orbit",
                              "number": 2, "params": {"altitude": 6706,
                              "pattern": "Race-Track", "speed": 150,
                              "speedEdited": True}},
                          3: {"enabled": True, "auto": False, "id": "WrappedAction",
                              "number": 3, "params": {"action": {
                                  "id": "ActivateBeacon", "params": {
                                      "type": 4, "AA": True, "callsign": "SHL",
                                      "channel": 57, "modeChannel": "X",
                                      "system": 4, "bearing": True}}}}}),
     make_waypoint(-115000, -185000, 6706, 150, "TRACK EXXON 2")])


# ============================================================
# RED GROUND
# ============================================================
sa6 = make_ground_group(20, "Abu Musa SA-6", ABU_MUSA_X, ABU_MUSA_Y, [
    make_ground_unit(2001, "SA-6 SR", "Kub 1S91 str", ABU_MUSA_X, ABU_MUSA_Y),
    make_ground_unit(2002, "SA-6 LN 1", "Kub 2P25 ln", ABU_MUSA_X+50, ABU_MUSA_Y+50),
    make_ground_unit(2003, "SA-6 LN 2", "Kub 2P25 ln", ABU_MUSA_X-50, ABU_MUSA_Y+50),
    make_ground_unit(2004, "SA-6 LN 3", "Kub 2P25 ln", ABU_MUSA_X, ABU_MUSA_Y-60),
    make_ground_unit(2005, "SA-6 EWR", "p-19 rd", ABU_MUSA_X-200, ABU_MUSA_Y-200)])

aaa = make_ground_group(21, "Abu Musa AAA", ABU_MUSA_X+300, ABU_MUSA_Y+300, [
    make_ground_unit(2101, "ZSU-1", "ZSU-23-4 Shilka", ABU_MUSA_X+300, ABU_MUSA_Y+300),
    make_ground_unit(2102, "ZSU-2", "ZSU-23-4 Shilka", ABU_MUSA_X-300, ABU_MUSA_Y-300),
    make_ground_unit(2103, "ZSU-3", "ZSU-23-4 Shilka", ABU_MUSA_X+400, ABU_MUSA_Y-200)])

hawk = make_ground_group(22, "Greater Tunb HAWK", GREATER_TUNB_X, GREATER_TUNB_Y, [
    make_ground_unit(2201, "HAWK SR", "Hawk sr", GREATER_TUNB_X, GREATER_TUNB_Y),
    make_ground_unit(2202, "HAWK TR", "Hawk tr", GREATER_TUNB_X+30, GREATER_TUNB_Y+30),
    make_ground_unit(2203, "HAWK PCP", "Hawk pcp", GREATER_TUNB_X-30, GREATER_TUNB_Y-30),
    make_ground_unit(2204, "HAWK CWAR", "Hawk cwar", GREATER_TUNB_X+60, GREATER_TUNB_Y-30),
    make_ground_unit(2205, "HAWK LN 1", "Hawk ln", GREATER_TUNB_X-50, GREATER_TUNB_Y+50),
    make_ground_unit(2206, "HAWK LN 2", "Hawk ln", GREATER_TUNB_X+50, GREATER_TUNB_Y-50)])

sa2 = make_ground_group(23, "Qeshm SA-2", QESHM_X, QESHM_Y, [
    make_ground_unit(2301, "SA-2 TR", "SNR_75V", QESHM_X, QESHM_Y),
    make_ground_unit(2302, "SA-2 LN 1", "S_75M_Volhov", QESHM_X+50, QESHM_Y+50),
    make_ground_unit(2303, "SA-2 LN 2", "S_75M_Volhov", QESHM_X-50, QESHM_Y+50),
    make_ground_unit(2304, "SA-2 LN 3", "S_75M_Volhov", QESHM_X, QESHM_Y-60)])

ewr = make_ground_group(24, "Qeshm EWR", QESHM_X-500, QESHM_Y-500, [
    make_ground_unit(2401, "EWR Qeshm", "1L13 EWR", QESHM_X-500, QESHM_Y-500)])


# ============================================================
# RED AIR (late activation MiG-29)
# ============================================================
mig = make_air_group(30, "BANDIT 1", 124, "CAP", BANDAR_X, BANDAR_Y,
    [make_air_unit(3001, "BANDIT 1-1", "MiG-29A", BANDAR_X, BANDAR_Y, 7000,
                   3.14, 250, "Good", "701",
                   {1: 1, 2: 1, 3: 1, "name": "701"}, MIG29_PAYLOAD),
     make_air_unit(3002, "BANDIT 1-2", "MiG-29A", BANDAR_X-30, BANDAR_Y-30, 7000,
                   3.14, 250, "Good", "702",
                   {1: 1, 2: 1, 3: 2, "name": "702"}, MIG29_PAYLOAD)],
    [make_waypoint(BANDAR_X, BANDAR_Y, 7000, 250, "TAKEOFF", eta_locked=True),
     make_waypoint(GREATER_TUNB_X, GREATER_TUNB_Y, 8000, 280, "INTERCEPT",
                   tasks={1: {"enabled": True, "auto": False, "id": "EngageTargets",
                              "number": 1,
                              "params": {"targetTypes": {1: "Planes"}, "priority": 0}}}),
     make_waypoint(BANDAR_X, BANDAR_Y, 25, 80, "RTB",
                   wp_type="Land", action="Landing")],
    late_activation=True)


# ============================================================
# BLUE NAVAL
# ============================================================

# CVN-74 Stennis carrier group (carrier + Ticonderoga escort)
carrier_group = make_ship_group(8, "CVN-74 Stennis", CARRIER_X, CARRIER_Y,
    [make_ship_unit(CVN74_ID, "CVN-74 Stennis", "Stennis",
                    CARRIER_X, CARRIER_Y, 5.93),      # heading ~340 deg (into wind)
     make_ship_unit(1002, "CG-52 Bunker Hill", "TICONDEROG",
                    CARRIER_X-300, CARRIER_Y+500, 5.93)],
    waypoints=[
        make_waypoint(CARRIER_X, CARRIER_Y, 0, 8, "STATION", eta_locked=True),
        make_waypoint(CARRIER_X+20000, CARRIER_Y-5000, 0, 8, "RECOVERY"),
    ])

# DDG-62 Fitzgerald (Arleigh Burke, helo ops for OUTLAWS)
ddg_group = make_ship_group(9, "DDG-62 Fitzgerald", FRIGATE_X, FRIGATE_Y,
    [make_ship_unit(DDG62_ID, "DDG-62 Fitzgerald", "USS_Arleigh_Burke_IIa",
                    FRIGATE_X, FRIGATE_Y, 5.93)],
    waypoints=[
        make_waypoint(FRIGATE_X, FRIGATE_Y, 0, 5, "PATROL", eta_locked=True),
        make_waypoint(FRIGATE_X+10000, FRIGATE_Y-5000, 0, 5, "PATROL 2"),
    ])


# ============================================================
# Al Dhafra warehouse entry
# ============================================================
al_dhafra_warehouse = {
    "allowHotStart": True,
    "unlimitedMunitions": True,
    "OperatingLevel_Air": 10,
    "methanol_mixture": {"InitFuel": 100},
    "diesel": {"InitFuel": 100},
    "speed": 16.666666,
    "dynamicSpawn": True,
    "unlimitedAircrafts": True,
    "unlimitedFuel": True,
    "jet_fuel": {"InitFuel": 100},
    "periodicity": 30,
    "suppliers": {},
    "coalition": "BLUE",
    "dynamicCargo": False,
    "OperatingLevel_Eqp": 10,
    "gasoline": {"InitFuel": 100},
    "size": 100,
    "OperatingLevel_Fuel": 10,
    "weapons": {},
    "aircrafts": {},
}


# ============================================================
# MISSION CONFIGURATIONS
# ============================================================
MISSIONS = [
    {
        "number": 1,
        "codename": "Sledgehammer",
        "filename": "M1_Sledgehammer.miz",
        "day": 15, "month": 4, "year": 1995,
        "start_time": 16200,   # 0430L
        "sortie": "Operation Sledgehammer",
        "description": (
            "Operation Burning Straits - Mission 1: Sledgehammer\n"
            "SEAD/DEAD strike against Iranian IADS.\n2-5 Players"),
        "blue_task": (
            "Degrade Iranian IADS to enable follow-on strike operations. "
            "Destroy SA-6 battery on Abu Musa Island and HAWK site on Greater Tunb."),
        "red_task": "Defend Persian Gulf approaches. Maintain air defense network integrity.",
        "completion_groups": [20, 22],
        "destroy_messages": [
            (20, "OVERLORD: Abu Musa SA-6 confirmed destroyed. Good hits, good hits."),
            (22, "OVERLORD: Greater Tunb HAWK is down. Threat neutralized."),
        ],
    },
    {
        "number": 2,
        "codename": "Iron Fist",
        "filename": "M2_Iron_Fist.miz",
        "day": 16, "month": 4, "year": 1995,
        "start_time": 18000,   # 0500L
        "sortie": "Operation Iron Fist",
        "description": (
            "Operation Burning Straits - Mission 2: Iron Fist\n"
            "Follow-up DEAD/CAS strike. Exploit IADS gaps.\n2-5 Players"),
        "blue_task": (
            "Exploit gaps in Iranian IADS. Destroy Abu Musa AAA "
            "and Qeshm SA-2 to open low-level corridors."),
        "red_task": "Reinforce air defenses. Counter coalition SEAD operations.",
        "completion_groups": [21, 23],
        "destroy_messages": [
            (21, "OVERLORD: Abu Musa AAA neutralized. Area clear for low-level ops."),
            (23, "OVERLORD: Qeshm SA-2 site destroyed. Good work."),
        ],
    },
    {
        "number": 3,
        "codename": "Blind Eagle",
        "filename": "M3_Blind_Eagle.miz",
        "day": 17, "month": 4, "year": 1995,
        "start_time": 14400,   # 0400L
        "sortie": "Operation Blind Eagle",
        "description": (
            "Operation Burning Straits - Mission 3: Blind Eagle\n"
            "Destroy enemy early warning radar network.\n2-5 Players"),
        "blue_task": (
            "Blind Iranian radar network. Destroy Qeshm EWR "
            "to enable undetected deep strike operations."),
        "red_task": "Maintain radar coverage. Detect and engage coalition aircraft.",
        "completion_groups": [24],
        "destroy_messages": [
            (24, "OVERLORD: Qeshm EWR destroyed. Enemy radar network is blind. Outstanding."),
        ],
    },
    {
        "number": 4,
        "codename": "Thunder Run",
        "filename": "M4_Thunder_Run.miz",
        "day": 18, "month": 4, "year": 1995,
        "start_time": 50400,   # 1400L afternoon
        "sortie": "Operation Thunder Run",
        "description": (
            "Operation Burning Straits - Mission 4: Thunder Run\n"
            "Deep strike to eliminate remaining air defenses.\n2-5 Players"),
        "blue_task": (
            "Destroy all remaining Iranian air defense installations "
            "in the Strait of Hormuz area."),
        "red_task": "Last-ditch defense. Protect remaining air defense assets at all costs.",
        "completion_groups": [20, 21, 22, 23, 24],
        "destroy_messages": [
            (20, "OVERLORD: Abu Musa SA-6 destroyed."),
            (21, "OVERLORD: Abu Musa AAA neutralized."),
            (22, "OVERLORD: Greater Tunb HAWK destroyed."),
            (23, "OVERLORD: Qeshm SA-2 destroyed."),
            (24, "OVERLORD: Qeshm EWR destroyed."),
        ],
    },
    {
        "number": 5,
        "codename": "Persian Storm",
        "filename": "M5_Persian_Storm.miz",
        "day": 19, "month": 4, "year": 1995,
        "start_time": 19800,   # 0530L
        "sortie": "Operation Persian Storm",
        "description": (
            "Operation Burning Straits - Mission 5: Persian Storm\n"
            "Final operation. Secure the Strait of Hormuz.\n2-5 Players"),
        "blue_task": (
            "Final sweep of the Strait of Hormuz. Eliminate all "
            "remaining threats to secure passage for naval operations."),
        "red_task": "Defend the Strait at all costs. Deny coalition forces control of the waterway.",
        "completion_groups": [20, 21, 22, 23, 24],
        "destroy_messages": [
            (20, "OVERLORD: Abu Musa SA-6 confirmed destroyed."),
            (21, "OVERLORD: Abu Musa AAA eliminated."),
            (22, "OVERLORD: Greater Tunb HAWK is down."),
            (23, "OVERLORD: Qeshm SA-2 neutralized."),
            (24, "OVERLORD: Qeshm EWR destroyed. Strait is clear!"),
        ],
    },
]

# Weather presets per mission
WEATHER = {
    1: {  # Dawn, clear
        "atmosphere_type": 0,
        "wind": {
            "at8000": {"speed": 6, "dir": 320},
            "at2000": {"speed": 4, "dir": 330},
            "atGround": {"speed": 2, "dir": 340},
        },
        "enable_fog": False,
        "season": {"temperature": 25},
        "type_weather": 0,
        "qnh": 760,
        "cyclones": {},
        "name": "Custom",
        "fog": {"thickness": 0, "visibility": 0},
        "visibility": {"distance": 80000},
        "dust_density": 0,
        "enable_dust": False,
        "clouds": {"thickness": 200, "density": 0, "base": 5000, "iprecptns": 0},
        "groundTurbulence": 0,
        "halo": {"preset": "auto"},
    },
    2: {  # Morning, light haze
        "atmosphere_type": 0,
        "wind": {
            "at8000": {"speed": 8, "dir": 300},
            "at2000": {"speed": 5, "dir": 310},
            "atGround": {"speed": 3, "dir": 320},
        },
        "enable_fog": False,
        "season": {"temperature": 28},
        "type_weather": 0,
        "qnh": 758,
        "cyclones": {},
        "name": "Custom",
        "fog": {"thickness": 0, "visibility": 0},
        "visibility": {"distance": 60000},
        "dust_density": 300,
        "enable_dust": True,
        "clouds": {"thickness": 400, "density": 2, "base": 6000, "iprecptns": 0},
        "groundTurbulence": 3,
        "halo": {"preset": "auto"},
    },
    3: {  # Pre-dawn, thin overcast
        "atmosphere_type": 0,
        "wind": {
            "at8000": {"speed": 10, "dir": 280},
            "at2000": {"speed": 6, "dir": 290},
            "atGround": {"speed": 4, "dir": 300},
        },
        "enable_fog": False,
        "season": {"temperature": 22},
        "type_weather": 0,
        "qnh": 755,
        "cyclones": {},
        "name": "Custom",
        "fog": {"thickness": 0, "visibility": 0},
        "visibility": {"distance": 70000},
        "dust_density": 0,
        "enable_dust": False,
        "clouds": {"thickness": 600, "density": 4, "base": 4000, "iprecptns": 0},
        "groundTurbulence": 2,
        "halo": {"preset": "auto"},
    },
    4: {  # Afternoon, hot & dusty
        "atmosphere_type": 0,
        "wind": {
            "at8000": {"speed": 12, "dir": 260},
            "at2000": {"speed": 8, "dir": 270},
            "atGround": {"speed": 5, "dir": 280},
        },
        "enable_fog": False,
        "season": {"temperature": 35},
        "type_weather": 0,
        "qnh": 756,
        "cyclones": {},
        "name": "Custom",
        "fog": {"thickness": 0, "visibility": 0},
        "visibility": {"distance": 50000},
        "dust_density": 500,
        "enable_dust": True,
        "clouds": {"thickness": 200, "density": 1, "base": 7000, "iprecptns": 0},
        "groundTurbulence": 5,
        "halo": {"preset": "auto"},
    },
    5: {  # Dawn, scattered clouds
        "atmosphere_type": 0,
        "wind": {
            "at8000": {"speed": 7, "dir": 310},
            "at2000": {"speed": 4, "dir": 320},
            "atGround": {"speed": 2, "dir": 330},
        },
        "enable_fog": False,
        "season": {"temperature": 26},
        "type_weather": 0,
        "qnh": 760,
        "cyclones": {},
        "name": "Custom",
        "fog": {"thickness": 0, "visibility": 0},
        "visibility": {"distance": 80000},
        "dust_density": 0,
        "enable_dust": False,
        "clouds": {"thickness": 300, "density": 3, "base": 5500, "iprecptns": 0},
        "groundTurbulence": 1,
        "halo": {"preset": "auto"},
    },
}


# ============================================================
# TRIGGER GENERATOR
# ============================================================
def make_triggers(cfg):
    """Build trig dict and trigrules dict for a mission config."""
    mission_num = cfg["number"]
    completion_groups = cfg["completion_groups"]
    destroy_messages = cfg["destroy_messages"]

    actions = {}
    conditions = {}
    func = {}
    funcStartup = {}
    flag = {}
    trigrules = {}
    idx = 1

    # Helper: add a triggerOnce trigger (both func and funcStartup)
    def add_trigger(action_str, condition_str, trigrule):
        nonlocal idx
        actions[idx] = action_str
        conditions[idx] = condition_str
        func[idx] = (f"if mission.trig.conditions[{idx}]() then "
                     f"mission.trig.actions[{idx}]() end")
        funcStartup[idx] = (f"if mission.trig.conditions[{idx}]() then "
                            f"mission.trig.actions[{idx}]() "
                            f"mission.trig.func[{idx}]=nil end")
        flag[idx] = True
        trigrules[idx] = trigrule
        idx += 1

    # 1: MiG-29 Scramble - Activate
    add_trigger(
        "a_activate_group(30)",
        'return(c_part_of_coalition_in_zone("blue", 1) )',
        {"rules": {1: {"coalitionlist": "blue", "zone": 1,
                        "predicate": "c_part_of_coalition_in_zone"}},
         "comment": "MiG-29 Scramble - Activate", "eventlist": "",
         "actions": {1: {"predicate": "a_activate_group", "group": 30}},
         "predicate": "triggerOnce", "colorItem": "0xffff0000"})

    # 2: AWACS Warning
    add_trigger(
        'a_out_text_delay("OVERLORD: All flights, bandits scrambling Bandar Abbas. '
        'Two Fulcrums heading south.", 15, false)',
        'return(c_part_of_coalition_in_zone("blue", 1) )',
        {"rules": {1: {"coalitionlist": "blue", "zone": 1,
                        "predicate": "c_part_of_coalition_in_zone"}},
         "comment": "MiG-29 Scramble - AWACS Warning", "eventlist": "",
         "actions": {1: {"predicate": "a_out_text_delay",
                         "text": "OVERLORD: All flights, bandits scrambling "
                                 "Bandar Abbas. Two Fulcrums heading south.",
                         "seconds": 15}},
         "predicate": "triggerOnce", "colorItem": "0xffff0000"})

    # 3: Set Mission Number (T+1)
    set_num = f"BS = BS or {{}}; BS.MISSION_NUMBER = {mission_num}"
    add_trigger(
        f'a_do_script("{set_num}")',
        "return(c_time_after(1) )",
        {"rules": {1: {"predicate": "c_time_after", "seconds": 1}},
         "comment": f"Set Mission Number ({mission_num})", "eventlist": "",
         "actions": {1: {"predicate": "a_do_script", "text": set_num}},
         "predicate": "triggerOnce", "colorItem": "0xff00ffff"})

    # 4: Load Persistence Script (T+3)
    add_trigger(
        'a_do_script_file(getValueResourceByKey("persistence.lua"))',
        "return(c_time_after(3) )",
        {"rules": {1: {"predicate": "c_time_after", "seconds": 3}},
         "comment": "Load Persistence Script", "eventlist": "",
         "actions": {1: {"predicate": "a_do_script_file",
                         "file": "persistence.lua"}},
         "predicate": "triggerOnce", "colorItem": "0xff00ffff"})

    # 5: State Applied Notification (T+5)
    add_trigger(
        'a_do_script("trigger.action.outText(\'Campaign state applied.\', 10)")',
        "return(c_time_after(5) )",
        {"rules": {1: {"predicate": "c_time_after", "seconds": 5}},
         "comment": "State Applied Notification", "eventlist": "",
         "actions": {1: {"predicate": "a_do_script",
                         "text": "trigger.action.outText("
                                 "'Campaign state applied.', 10)"}},
         "predicate": "triggerOnce", "colorItem": "0xff00ffff"})

    # 6+: Group destroyed messages (per-mission)
    for group_id, message in destroy_messages:
        add_trigger(
            f'a_out_text_delay("{message}", 10, false)',
            f"return(c_group_dead({group_id}) )",
            {"rules": {1: {"predicate": "c_group_dead", "groupid": group_id}},
             "comment": f"Group {group_id} Destroyed",
             "eventlist": "",
             "actions": {1: {"predicate": "a_out_text_delay",
                             "text": message, "seconds": 10}},
             "predicate": "triggerOnce", "colorItem": "0xff00ff00"})

    # Last: Mission Complete
    comp_cond = " and ".join(f"c_group_dead({g})" for g in completion_groups)
    comp_rules = {}
    for i, gid in enumerate(completion_groups, 1):
        comp_rules[i] = {"predicate": "c_group_dead", "groupid": gid}
    add_trigger(
        'a_do_script("BS.completeMission()")',
        f"return({comp_cond} )",
        {"rules": comp_rules,
         "comment": "Mission Complete - Primary Objectives",
         "eventlist": "",
         "actions": {1: {"predicate": "a_do_script",
                         "text": "BS.completeMission()"}},
         "predicate": "triggerOnce", "colorItem": "0xff00ff00"})

    trig = {
        "actions": actions,
        "conditions": conditions,
        "func": func,
        "funcStartup": funcStartup,
        "customStartup": {},
        "events": {},
        "flag": flag,
    }
    return trig, trigrules


# ============================================================
# MISSION TABLE BUILDER
# ============================================================
def make_mission_table(cfg):
    """Build the full DCS mission dict for a given config."""
    trig, trigrules = make_triggers(cfg)

    return {
        "groundControl": {
            "passwords": {
                "artillery_commander": {},
                "instructor": {},
                "observer": {},
                "forward_observer": {},
            },
            "roles": {
                "artillery_commander": {"neutrals": 0, "blue": 0, "red": 0},
                "instructor": {"neutrals": 0, "blue": 0, "red": 0},
                "observer": {"neutrals": 0, "blue": 0, "red": 0},
                "forward_observer": {"neutrals": 0, "blue": 0, "red": 0},
            },
            "isPilotControlVehicles": False,
            "roles_prohibitions": {},
        },
        "requiredModules": {},
        "date": {
            "Day": cfg["day"],
            "Year": cfg["year"],
            "Month": cfg["month"],
        },
        "trig": trig,
        "maxDictId": 0,
        "result": {
            "offline": {"conditions": {}, "actions": {}, "func": {}},
            "total": 0,
            "blue": {"conditions": {}, "actions": {}, "func": {}},
            "red": {"conditions": {}, "actions": {}, "func": {}},
        },
        "pictureFileNameN": {},
        "descriptionNeutralsTask": "",
        "pictureFileNameServer": {},
        "weather": WEATHER[cfg["number"]],
        "theatre": "PersianGulf",
        "triggers": {
            "zones": {
                1: {
                    "radius": 120000,
                    "zoneId": 1,
                    "x": 30000,
                    "y": -80000,
                    "name": "SCRAMBLE_ZONE",
                    "type": 0,
                    "color": {1: 1, 2: 0, 3: 0, 4: 0.15},
                    "hidden": True,
                    "properties": {},
                },
            },
        },
        "map": {
            "centerY": -130000,
            "zoom": 512000,
            "centerX": -20000,
        },
        "coalitions": {
            "blue": {1: 2, 2: 5},
            "red": {1: 34},
            "neutrals": {1: 18},
        },
        "descriptionText": cfg["description"],
        "pictureFileNameR": {},
        "descriptionBlueTask": cfg["blue_task"],
        "goals": {},
        "descriptionRedTask": cfg["red_task"],
        "pictureFileNameB": {},
        "coalition": {
            "neutrals": {
                "bullseye": {"y": 0, "x": 0},
                "nav_points": {},
                "name": "neutrals",
                "country": {},
            },
            "blue": {
                "bullseye": {"y": -100000, "x": 20000},
                "nav_points": {},
                "name": "blue",
                "country": {
                    1: {
                        "id": 2,
                        "name": "USA",
                        "plane": {
                            "group": {
                                1: warhawks,
                                2: blacksheep,
                                3: panther,
                                4: overlord,
                                5: shell,
                            },
                        },
                        "helicopter": {
                            "group": {
                                1: outlaws,
                            },
                        },
                        "ship": {
                            "group": {
                                1: carrier_group,
                                2: ddg_group,
                            },
                        },
                    },
                    2: {
                        "id": 5,
                        "name": "France",
                        "plane": {
                            "group": {
                                1: witcher,
                            },
                        },
                    },
                },
            },
            "red": {
                "bullseye": {"y": 0, "x": 0},
                "nav_points": {},
                "name": "red",
                "country": {
                    1: {
                        "id": 34,
                        "name": "Iran",
                        "vehicle": {
                            "group": {
                                1: sa6,
                                2: aaa,
                                3: hawk,
                                4: sa2,
                                5: ewr,
                            },
                        },
                        "plane": {
                            "group": {
                                1: mig,
                            },
                        },
                    },
                },
            },
        },
        "sortie": cfg["sortie"],
        "version": 21,
        "trigrules": trigrules,
        "currentKey": 3100,
        "failures": {},
        "forcedOptions": {},
        "start_time": cfg["start_time"],
    }


# ============================================================
# SUPPORTING DATA
# ============================================================
options = {
    "playerName": "Player",
    "miscellaneous": {
        "allow_ownship_export": True,
        "headmove": False,
        "f_awacs_enabled": True,
        "f5_nearest_ac": True,
    },
    "difficulty": {
        "labels": 0,
        "fuel": False,
        "easyRadar": False,
        "miniHUD": False,
        "optionsView": "optview_all",
        "setGlobal": True,
        "avionicsLanguage": "native",
        "cockpitVisualRM": False,
        "map": True,
        "spectatorExternalViews": True,
        "userSnapView": True,
        "iconsTheme": "nato",
        "weapons": False,
        "padlock": False,
        "birds": 0,
        "permitCrash": True,
        "immortal": False,
        "cockpitStatusBarAllowed": False,
        "wakeTurbulence": False,
        "easyFlight": False,
        "hideStick": False,
        "radio": False,
        "geffect": "realistic",
        "easyCommunication": True,
        "reports": True,
        "tips": True,
        "autoTrimmer": False,
        "externalViews": True,
        "RBDAI": True,
        "civTraffic": "",
        "units": "imperial",
    },
    "VR": {},
}

warehouses = {
    "airports": {
        AIRDROME_AL_DHAFRA: al_dhafra_warehouse,
    },
    "warehouses": {},
}


# ============================================================
# BUILD ALL MISSIONS
# ============================================================
options_lua = to_lua(options, "options")
warehouses_lua = to_lua(warehouses, "warehouses")

persistence_path = os.path.join(OUT_DIR, "persistence.lua")
kb_dir = os.path.join(OUT_DIR, "kneeboards")

for cfg in MISSIONS[:1]:
    miz_path = os.path.join(OUT_DIR, cfg["filename"])
    mission = make_mission_table(cfg)
    mission_lua = to_lua(mission, "mission")

    print(f"Building {cfg['filename']} (Mission {cfg['number']}: {cfg['codename']})...")

    with zipfile.ZipFile(miz_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("mission", mission_lua)
        zf.writestr("options", options_lua)
        zf.writestr("warehouses", warehouses_lua)
        zf.writestr("l10n/DEFAULT/dictionary", to_lua({}, "dictionary"))
        zf.writestr("l10n/DEFAULT/mapResource", to_lua({}, "mapResource"))
        zf.writestr("theatre", "PersianGulf")

        # Bundle persistence script
        if os.path.isfile(persistence_path):
            zf.write(persistence_path, "l10n/DEFAULT/persistence.lua")
        else:
            print("  WARNING: persistence.lua not found!")

        # Add kneeboards (per-mission subfolder: kneeboards/m1, m2, ...)
        mission_kb_dir = os.path.join(kb_dir, f"m{cfg['number']}")
        if os.path.isdir(mission_kb_dir):
            for fname in sorted(os.listdir(mission_kb_dir)):
                if fname.endswith(".png"):
                    fpath = os.path.join(mission_kb_dir, fname)
                    for ac in ["F-16C_50", "FA-18C_hornet", "M-2000C",
                                "AH-64D_BLK_II"]:
                        zf.write(fpath, f"KNEEBOARD/{ac}/{fname}")

    print(f"  -> {os.path.getsize(miz_path)} bytes, "
          f"{len(cfg['completion_groups'])} completion objectives, "
          f"{len(cfg['destroy_messages'])} destroy messages")

print(f"\nDone! Built {len(MISSIONS)} missions.")
