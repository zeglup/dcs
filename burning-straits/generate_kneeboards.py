#!/usr/bin/env python3
"""
Generate kneeboard PNG pages for all Burning Straits campaign missions.
DCS kneeboard format: 768x1024 PNG, dark background, light text.
"""

from PIL import Image, ImageDraw, ImageFont
import os, zipfile, shutil

W, H = 768, 1024
BG = (30, 32, 36)
WHITE = (230, 230, 230)
CYAN = (76, 208, 222)
ORANGE = (240, 160, 60)
RED = (220, 80, 80)
GREEN = (100, 200, 100)
YELLOW = (230, 210, 90)
DIM = (140, 145, 155)
LINE_COLOR = (70, 75, 85)

# Use monospace system font or fallback
def get_fonts():
    # Windows monospace fonts
    win_fonts = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
    paths = [
        # Windows
        os.path.join(win_fonts, "consola.ttf"),   # Consolas
        os.path.join(win_fonts, "lucon.ttf"),      # Lucida Console
        os.path.join(win_fonts, "cour.ttf"),       # Courier New
        os.path.join(win_fonts, "CascadiaMono.ttf"),  # Cascadia Mono
        # macOS
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/SFMono-Regular.otf",
        "/Library/Fonts/SF-Mono-Regular.otf",
        "/System/Library/Fonts/Monaco.dfont",
        "/System/Library/Fonts/Courier.dfont",
        # Linux
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                from PIL import ImageFont as IF
                return {
                    "title": IF.truetype(p, 28),
                    "heading": IF.truetype(p, 20),
                    "body": IF.truetype(p, 16),
                    "small": IF.truetype(p, 13),
                    "big": IF.truetype(p, 34),
                }
            except:
                continue
    # fallback to default
    return {
        "title": ImageFont.load_default(),
        "heading": ImageFont.load_default(),
        "body": ImageFont.load_default(),
        "small": ImageFont.load_default(),
        "big": ImageFont.load_default(),
    }

fonts = get_fonts()

def new_page():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    return img, draw

def draw_header(draw, title, subtitle=None):
    # Top border
    draw.rectangle([0, 0, W, 3], fill=ORANGE)
    draw.text((W // 2, 20), title, fill=ORANGE, font=fonts["big"], anchor="mt")
    y = 58
    if subtitle:
        draw.text((W // 2, y), subtitle, fill=DIM, font=fonts["small"], anchor="mt")
        y += 20
    draw.line([(30, y + 5), (W - 30, y + 5)], fill=LINE_COLOR, width=1)
    return y + 15

def draw_footer(draw, page_num, total, op_name="BURNING STRAITS"):
    draw.line([(30, H - 40), (W - 30, H - 40)], fill=LINE_COLOR, width=1)
    draw.text((W // 2, H - 25), f"OP {op_name}  -  Page {page_num}/{total}", fill=DIM, font=fonts["small"], anchor="mt")

def draw_section(draw, y, heading):
    draw.text((40, y), heading, fill=CYAN, font=fonts["heading"])
    y += 26
    draw.line([(40, y), (W - 40, y)], fill=LINE_COLOR, width=1)
    return y + 8

def draw_row(draw, y, label, value, label_color=DIM, value_color=WHITE):
    draw.text((55, y), label, fill=label_color, font=fonts["body"])
    draw.text((280, y), value, fill=value_color, font=fonts["body"])
    return y + 22

def draw_text(draw, y, text, color=WHITE, indent=55):
    draw.text((indent, y), text, fill=color, font=fonts["body"])
    return y + 22

def draw_text_small(draw, y, text, color=DIM, indent=55):
    draw.text((indent, y), text, fill=color, font=fonts["small"])
    return y + 18

# =========================================
# MISSION DATA (all 5 missions)
# =========================================
MISSION_DATA = {
    1: {
        "codename": "SLEDGEHAMMER",
        "type": "SEAD / DEAD",
        "datetime": "15 APR 1995 / 0430L",
        "weather": "Clear, wind 340/02kt, 25C",
        "objective_lines": [
            ("Degrade Iranian IADS to enable", WHITE),
            ("follow-on strike operations.", WHITE),
        ],
        "pri_objectives": [
            "SA-6 Kub on Abu Musa Island",
            "HAWK on Greater Tunb Island",
        ],
        "opt_objectives": [
            "1L13 EWR on Qeshm (WITCHER)",
            "ZSU-23 AAA Abu Musa (OUTLAWS)",
        ],
        "package": [
            ("WARHAWKS 1   F-16C   SEAD (Player)", ORANGE),
            ("BLACKSHEEP 1 F/A-18C DEAD x4 (Client)", WHITE),
            ("WITCHER 1    M-2000C Sweep (Client)", WHITE),
            ("OUTLAWS 1    AH-64D  CAS x2 (Client)", WHITE),
            ("PANTHER 1    F-15C   Escort x2 (AI)", DIM),
            ("OVERLORD     E-3A    AWACS (AI)", DIM),
            ("SHELL 1      KC-135  Tanker (AI)", DIM),
        ],
        "timeline": [
            "0430L  Package airborne at assembly",
            "0440L  Push - WARHAWKS lead, SEAD",
            "0445L  BLACKSHEEP IP for Abu Musa",
            "0445L  OUTLAWS low-level approach",
            "       WITCHER sweep eastern flank",
            "0500L  Egress SW, RTB Al Dhafra",
        ],
        "roe": [
            ("Weapons FREE on radiating SAMs", GREEN),
            ("PID required on all air contacts", YELLOW),
            ("OVERLORD controls intercepts", WHITE),
        ],
        "comms_roles": [
            ("WARHAWKS 1", "305.0", "AM", "SEAD", ORANGE),
            ("BLACKSHEEP 1", "270.0", "AM", "DEAD", WHITE),
            ("WITCHER 1", "282.0", "AM", "SWEEP/STRIKE", WHITE),
            ("OUTLAWS 1", "127.5", "FM", "CAS/AAA", WHITE),
            ("PANTHER 1", "325.0", "AM", "ESCORT (AI)", DIM),
        ],
        "sam_threats": [
            {"name": "SA-6 KUB  -  Abu Musa Island", "color": RED, "lines": [
                ("Tracking: 1S91 SURN (CW + pulse)", WHITE),
                ("Search:   P-19 Flat Face", WHITE),
                ("Launchers: 4x 2P25 (3 missiles each)", WHITE),
                ("Range: 24 km  |  Alt: 100-14000m", YELLOW),
                ("NOTE: PRIMARY TARGET", ORANGE),
            ]},
            {"name": "HAWK  -  Greater Tunb Island", "color": RED, "lines": [
                ("Track: AN/MPQ-46 High Power Illum.", WHITE),
                ("Search: AN/MPQ-50", WHITE),
                ("Launchers: 3x M192", WHITE),
                ("Range: 40 km  |  Alt: 60-18000m", YELLOW),
                ("COVERS EGRESS LANE", ORANGE),
            ]},
            {"name": "SA-2 GUIDELINE  -  Qeshm Island", "color": ORANGE, "lines": [
                ("Track: SNR-75 Fan Song", WHITE),
                ("Launchers: 6x S-75M", WHITE),
                ("Range: 40 km  |  Alt: 500-25000m", YELLOW),
            ]},
            {"name": "ZSU-23-4 AAA  -  Abu Musa", "color": ORANGE, "lines": [
                ("4x Shilka  |  Range: 2.5 km", WHITE),
                ("LETHAL below 8000ft AGL", RED),
            ]},
        ],
        "ewr_threats": [
            {"name": "1L13 EWR  -  Qeshm Island", "lines": [
                "Early warning radar - feeds GCI",
                "Optional target for WITCHER",
            ]},
        ],
        "air_threats": [
            {"name": "MiG-29A FULCRUM  x2", "lines": [
                ("Base: Bandar Abbas", WHITE),
                ("Weapons: R-27R/T (BVR), R-73 (WVR)", WHITE),
                ("SCRAMBLE ~8min after first shots", RED),
                ("PANTHER will engage, stay aware", YELLOW),
            ]},
        ],
        "warhawks_wps": [
            ("0", "ASSEMBLY", "FL200", "430kt", "Form up"),
            ("1", "PUSH", "FL180", "410kt", "SEAD engage"),
            ("2", "ABU MUSA", "FL180", "410kt", "Kill SA-6 radar"),
            ("3", "GREATER TUNB", "FL180", "410kt", "Kill HAWK radar"),
            ("4", "RTB AL DHAFRA", "SFC", "---", "Landing"),
        ],
        "warhawks_role": "SEAD",
        "blacksheep_wps": [
            ("0", "ASSEMBLY", "FL200", "430kt", "Form up"),
            ("1", "PUSH", "FL200", "410kt", "---"),
            ("2", "IP", "16400ft", "390kt", "Descend, setup"),
            ("3", "ABU MUSA SA-6", "16400ft", "390kt", "BOMB SA-6"),
            ("4", "RTB AL DHAFRA", "SFC", "---", "Landing"),
        ],
        "blacksheep_role": "DEAD",
        "witcher_wps": [
            ("0", "EAST FLANK", "FL200", "Depart east"),
            ("1", "SWEEP AHEAD", "FL200", "A/A sweep"),
            ("2", "OPT: QESHM EWR", "16400ft", "Bomb EWR"),
            ("3", "EGRESS", "FL200", "Turn south"),
            ("4", "RTB AL DHAFRA", "SFC", "Landing"),
        ],
        "witcher_role": "SWEEP + OPT",
        "outlaws_wps": [
            ("0", "HOLD SOUTH", "500ft AGL", "Hold / await"),
            ("1", "APPROACH", "300ft AGL", "Low level"),
            ("2", "ABU MUSA SHORE", "150ft AGL", "Engage ZSU-23"),
            ("3", "EGRESS SOUTH", "300ft AGL", "Withdraw"),
        ],
        "outlaws_role": "OPT CAS",
        "outlaws_notes": [
            ("OUTLAWS: Coordinate with BLACKSHEEP timing.", YELLOW),
            ("AAA must be suppressed before DEAD flight crosses beach.", YELLOW),
        ],
        "tactics": [
            {"heading": "SEAD TACTICS - WARHAWKS", "lines": [
                ("1. Monitor HTS for emitters on push", WHITE),
                ("2. Priority: SA-6 SURN (1S91)", WHITE),
                ("   Fire HARM on tracking radar", WHITE),
                ("3. Secondary: HAWK TR on Greater Tunb", WHITE),
                ("4. Conserve 1 HARM for egress cover", WHITE),
                ("5. SA-2 on Qeshm - avoid, not tasked", DIM),
            ]},
            {"heading": "DEAD TACTICS - BLACKSHEEP", "lines": [
                ("1. Hold at IP until WARHAWKS calls", WHITE),
                ("   'Magnum' (HARM away)", WHITE),
                ("2. Roll in on SA-6 launchers + radar", WHITE),
                ("3. Use precision weapons if loaded", WHITE),
                ("4. Stay above 8000ft (AAA)", WHITE),
                ("5. Egress SW immediately after drop", WHITE),
            ]},
        ],
        "critical_notes": [
            ("- MiG-29 scramble ~8 min after push", RED),
            ("- PANTHER will engage, maintain SA", RED),
            ("- HAWK covers egress - stay low or", YELLOW),
            ("  ensure WARHAWKS has killed TR", YELLOW),
            ("- Tanker SHELL 1 on 317.0 / 57X", WHITE),
        ],
    },
    2: {
        "codename": "IRON FIST",
        "type": "Anti-Ship Strike",
        "datetime": "16 APR 1995 / 0500L",
        "weather": "Light haze, wind 320/03kt, 28C",
        "objective_lines": [
            ("Neutralize Iranian coastal AShM", WHITE),
            ("infrastructure before fleet transit.", WHITE),
        ],
        "pri_objectives": [
            "Silkworm battery on Qeshm Island",
            "C-802 battery on Abu Musa Island",
        ],
        "opt_objectives": [
            "Houdong anchorage at Sirri (WITCHER)",
            "Boghammar staging Abu Musa (OUTLAWS)",
        ],
        "package": [
            ("WARHAWKS 1   F-16C   SEAD escort (Player)", ORANGE),
            ("BLACKSHEEP 1 F/A-18C Strike x4 (Client)", WHITE),
            ("WITCHER 1    M-2000C Armed recon (Client)", WHITE),
            ("OUTLAWS 1    AH-64D  Anti-surface x2 (Client)", WHITE),
            ("PANTHER 1    F-15C   Barrier CAP x2 (AI)", DIM),
            ("OVERLORD     E-3A    AWACS (AI)", DIM),
            ("SHELL 1      KC-135  Tanker (AI)", DIM),
        ],
        "timeline": [
            "0500L  Package airborne",
            "0510L  WARHAWKS push, suppress coastal SAMs",
            "0515L  BLACKSHEEP standoff strike Qeshm",
            "0520L  BLACKSHEEP re-attack Abu Musa C-802",
            "0520L  OUTLAWS littoral sweep Abu Musa",
            "       WITCHER armed recon toward Sirri",
            "0540L  Egress, RTB",
        ],
        "roe": [
            ("Cleared to engage military targets", GREEN),
            ("Avoid civilian port infrastructure", YELLOW),
            ("PID required before Harpoon launch", YELLOW),
            ("Shipping lanes active - caution", WHITE),
        ],
        "comms_roles": [
            ("WARHAWKS 1", "305.0", "AM", "SEAD ESC", ORANGE),
            ("BLACKSHEEP 1", "270.0", "AM", "STRIKE", WHITE),
            ("WITCHER 1", "282.0", "AM", "ARMED RECON", WHITE),
            ("OUTLAWS 1", "127.5", "FM", "ANTI-SURF", WHITE),
            ("PANTHER 1", "325.0", "AM", "BAR CAP (AI)", DIM),
        ],
        "sam_threats": [
            {"name": "Surviving SAMs (Mission 1 dependent)", "color": ORANGE, "lines": [
                ("SA-6, HAWK may still be active", WHITE),
                ("Check campaign status at mission start", YELLOW),
            ]},
            {"name": "Silkworm HY-2  -  Qeshm Island", "color": RED, "lines": [
                ("Anti-ship missile battery", WHITE),
                ("Defended by AAA and MANPADS", WHITE),
                ("PRIMARY TARGET", ORANGE),
            ]},
            {"name": "C-802 AShM  -  Abu Musa Island", "color": RED, "lines": [
                ("Anti-ship cruise missile", WHITE),
                ("PRIMARY TARGET", ORANGE),
            ]},
        ],
        "ewr_threats": [],
        "air_threats": [
            {"name": "F-14A TOMCAT  x2", "lines": [
                ("Base: Bandar Abbas", WHITE),
                ("Weapons: AIM-54A (BVR)", WHITE),
                ("Long-range intercept threat", RED),
                ("PANTHER on barrier CAP", YELLOW),
            ]},
        ],
        "warhawks_wps": [
            ("0", "ASSEMBLY", "FL200", "430kt", "Form up"),
            ("1", "PUSH", "FL180", "410kt", "SEAD suppress"),
            ("2", "QESHM COAST", "FL180", "410kt", "Cover strike"),
            ("3", "ABU MUSA", "FL180", "410kt", "Cover strike"),
            ("4", "RTB AL DHAFRA", "SFC", "---", "Landing"),
        ],
        "warhawks_role": "SEAD ESCORT",
        "blacksheep_wps": [
            ("0", "ASSEMBLY", "FL200", "430kt", "Form up"),
            ("1", "IP SOUTH", "FL200", "410kt", "Setup"),
            ("2", "QESHM SILKWORM", "16400ft", "390kt", "Standoff strike"),
            ("3", "ABU MUSA C-802", "16400ft", "390kt", "Strike"),
            ("4", "RTB CARRIER", "SFC", "---", "Landing"),
        ],
        "blacksheep_role": "ANTI-SHIP STRIKE",
        "witcher_wps": [
            ("0", "DEPART EAST", "FL200", "Sweep ahead"),
            ("1", "SIRRI ISLAND", "10000ft", "Armed recon"),
            ("2", "OPT: ANCHORAGE", "5000ft", "Attack boats"),
            ("3", "EGRESS SW", "FL200", "Turn south"),
            ("4", "RTB AL DHAFRA", "SFC", "Landing"),
        ],
        "witcher_role": "ARMED RECON",
        "outlaws_wps": [
            ("0", "HOLD SOUTH", "500ft AGL", "Hold / await"),
            ("1", "LITTORAL", "200ft AGL", "Low level"),
            ("2", "ABU MUSA EAST", "150ft AGL", "Interdict boats"),
            ("3", "EGRESS SOUTH", "300ft AGL", "Withdraw"),
        ],
        "outlaws_role": "ANTI-SURFACE",
        "outlaws_notes": [
            ("OUTLAWS: Use Longbow radar for PID.", YELLOW),
            ("Distinguish military from civilian traffic.", YELLOW),
        ],
        "tactics": [
            {"heading": "ANTI-SHIP TACTICS - BLACKSHEEP", "lines": [
                ("1. Standoff engagement preferred", WHITE),
                ("2. Harpoon/SLAM-ER on Silkworm site", WHITE),
                ("3. Re-attack Abu Musa C-802 battery", WHITE),
                ("4. Avoid overflying defended islands", WHITE),
                ("5. Watch for civilian shipping", YELLOW),
            ]},
            {"heading": "SEAD ESCORT - WARHAWKS", "lines": [
                ("1. Suppress surviving coastal SAMs", WHITE),
                ("2. Protect BLACKSHEEP during attack", WHITE),
                ("3. Monitor HTS - new emitters possible", WHITE),
                ("4. Stay between SAMs and strikers", WHITE),
            ]},
        ],
        "critical_notes": [
            ("- F-14A intercept from Bandar Abbas", RED),
            ("- Civilian shipping HEAVY in strait", RED),
            ("- PID mandatory before all launches", YELLOW),
            ("- Silkworm sites have AAA + MANPADS", YELLOW),
            ("- Tanker SHELL 1 on 317.0 / 57X", WHITE),
        ],
    },
    3: {
        "codename": "BLIND EAGLE",
        "type": "Defensive Counter-Air",
        "datetime": "17 APR 1995 / 0400L",
        "weather": "Thin overcast, wind 300/04kt, 22C",
        "objective_lines": [
            ("Maintain air superiority over the", WHITE),
            ("Strait. Defend fleet and tanker assets.", WHITE),
        ],
        "pri_objectives": [
            "Air superiority over central Strait",
            "Protect fleet and support assets",
        ],
        "opt_objectives": [
            "Intercept F-5E low-level raid (WITCHER)",
            "Defend FARP from amphibious assault (OUTLAWS)",
        ],
        "package": [
            ("WARHAWKS 1   F-16C   High CAP (Player)", ORANGE),
            ("BLACKSHEEP 1 F/A-18C Primary CAP x4 (Client)", WHITE),
            ("WITCHER 1    M-2000C Low CAP (Client)", WHITE),
            ("OUTLAWS 1    AH-64D  FARP defense x2 (Client)", WHITE),
            ("PANTHER 1    F-15C   Western CAP x2 (AI)", DIM),
            ("OVERLORD     E-3A    AWACS / GCI (AI)", DIM),
            ("SHELL 1      KC-135  Tanker (AI)", DIM),
        ],
        "timeline": [
            "0400L  CAP stations manned",
            "       BLACKSHEEP FL250 central Strait",
            "       WARHAWKS FL280 northeast",
            "       PANTHER covers Sirri Island axis",
            "0415L  First fighter wave expected",
            "       MiG-29A / F-14A from Bandar Abbas",
            "0430L  F-5E low-level raid from Bushehr",
            "0445L  Rotate / RTB for fuel",
        ],
        "roe": [
            ("Weapons FREE inside kill box", GREEN),
            ("PID required outside kill box", YELLOW),
            ("OVERLORD controls intercepts", WHITE),
        ],
        "comms_roles": [
            ("WARHAWKS 1", "305.0", "AM", "HIGH CAP", ORANGE),
            ("BLACKSHEEP 1", "270.0", "AM", "PRI CAP", WHITE),
            ("WITCHER 1", "282.0", "AM", "LOW CAP", WHITE),
            ("OUTLAWS 1", "127.5", "FM", "FARP DEF", WHITE),
            ("PANTHER 1", "325.0", "AM", "WEST CAP (AI)", DIM),
        ],
        "sam_threats": [
            {"name": "Surviving SAMs (campaign dependent)", "color": ORANGE, "lines": [
                ("Check campaign status at mission start", YELLOW),
                ("HTS provides SA on surviving SAMs", WHITE),
            ]},
        ],
        "ewr_threats": [],
        "air_threats": [
            {"name": "MiG-29A FULCRUM  x2-4", "lines": [
                ("R-27R/T (BVR), R-73 (WVR)", WHITE),
                ("Most dangerous - 2-4 ship formations", RED),
                ("GCI-directed if EWR survived", YELLOW),
            ]},
            {"name": "F-14A TOMCAT  x2", "lines": [
                ("AIM-54A (BVR) - long range threat", WHITE),
                ("Limited serviceability, 2-ship", WHITE),
            ]},
            {"name": "F-4E PHANTOM II", "lines": [
                ("AIM-7E (BVR) - medium altitude", WHITE),
                ("Hit-and-run tactics", WHITE),
            ]},
            {"name": "F-5E TIGER II (low raid)", "lines": [
                ("Hard to detect at low altitude", RED),
                ("Close-in anti-ship attack", WHITE),
                ("WITCHER tasked to intercept", YELLOW),
            ]},
        ],
        "warhawks_wps": [
            ("0", "STATION NE", "FL280", "430kt", "On-station CAP"),
            ("1", "CAP ORBIT 1", "FL280", "410kt", "Patrol"),
            ("2", "CAP ORBIT 2", "FL280", "410kt", "Patrol"),
            ("3", "INTERCEPT", "As req", "As req", "GCI vector"),
            ("4", "RTB AL DHAFRA", "SFC", "---", "Landing"),
        ],
        "warhawks_role": "HIGH CAP / INTERCEPT",
        "blacksheep_wps": [
            ("0", "STATION CTR", "FL250", "430kt", "On-station CAP"),
            ("1", "CAP ORBIT 1", "FL250", "410kt", "Patrol"),
            ("2", "CAP ORBIT 2", "FL250", "410kt", "Patrol"),
            ("3", "INTERCEPT", "As req", "As req", "GCI vector"),
            ("4", "RTB CARRIER", "SFC", "---", "Landing"),
        ],
        "blacksheep_role": "PRIMARY CAP",
        "witcher_wps": [
            ("0", "STATION LOW", "FL150", "Screen fleet"),
            ("1", "LOW CAP ORB", "FL150", "Patrol"),
            ("2", "INTERCEPT", "Low alt", "F-5E raid"),
            ("3", "EGRESS", "FL200", "RTB"),
            ("4", "RTB AL DHAFRA", "SFC", "Landing"),
        ],
        "witcher_role": "LOW CAP / F-5E INTERCEPT",
        "outlaws_wps": [
            ("0", "FARP OASIS", "SFC", "Deploy"),
            ("1", "PATROL NORTH", "200ft AGL", "Screen"),
            ("2", "ENGAGE", "150ft AGL", "Defend FARP"),
            ("3", "HOLD FARP", "SFC", "Maintain station"),
        ],
        "outlaws_role": "FARP DEFENSE",
        "outlaws_notes": [
            ("OUTLAWS: Defend FARP from amphibious assault.", YELLOW),
            ("Engage Zodiacs/landing craft from the north.", YELLOW),
        ],
        "tactics": [
            {"heading": "CAP TACTICS", "lines": [
                ("1. Maintain station, conserve fuel", WHITE),
                ("2. OVERLORD assigns targets via GCI", WHITE),
                ("3. BVR engagement preferred", WHITE),
                ("4. Watch for low-level leakers", YELLOW),
                ("5. Rotate for tanker as needed", WHITE),
            ]},
            {"heading": "THREAT PRIORITIES", "lines": [
                ("1. MiG-29A - highest threat, engage BVR", WHITE),
                ("2. F-14A - AIM-54 range, defeat early", WHITE),
                ("3. F-4E - medium threat, hit-and-run", WHITE),
                ("4. F-5E - low/fast, hard to acquire", RED),
            ]},
        ],
        "critical_notes": [
            ("- Multiple axis attack expected", RED),
            ("- MiG-29s may have GCI support", RED),
            ("- F-5E raid is LOW and FAST", YELLOW),
            ("- Protect the fleet at all costs", YELLOW),
            ("- Tanker SHELL 1 on 317.0 / 57X", WHITE),
        ],
    },
    4: {
        "codename": "THUNDER RUN",
        "type": "Anti-Surface / Littoral Strike",
        "datetime": "18 APR 1995 / 1400L",
        "weather": "Hot & dusty, wind 280/05kt, 35C",
        "objective_lines": [
            ("Locate and destroy IRGC Boghammar", WHITE),
            ("swarms threatening coalition warships.", WHITE),
        ],
        "pri_objectives": [
            "Destroy Boghammar groups in Strait",
            "Protect coalition naval forces",
        ],
        "opt_objectives": [
            "IRGC command boat near Qeshm (WITCHER)",
            "Boghammar staging at Larak (OUTLAWS)",
        ],
        "package": [
            ("WARHAWKS 1   F-16C   Sweep/strike (Player)", ORANGE),
            ("BLACKSHEEP 1 F/A-18C Armed recon x4 (Client)", WHITE),
            ("WITCHER 1    M-2000C Fwd spotter (Client)", WHITE),
            ("OUTLAWS 1    AH-64D  Anti-surface x2 (Client)", WHITE),
            ("PANTHER 1    F-15C   High cover x2 (AI)", DIM),
            ("OVERLORD     E-3A    AWACS (AI)", DIM),
            ("SHELL 1      KC-135  Tanker (AI)", DIM),
        ],
        "timeline": [
            "1400L  Package airborne",
            "1410L  WARHAWKS sanitizes airspace",
            "1415L  BLACKSHEEP armed recon Strait",
            "1415L  OUTLAWS push along island chain",
            "       WITCHER spots Qeshm coastline",
            "1445L  Egress, RTB",
        ],
        "roe": [
            ("PID MANDATORY - heavy civilian traffic", RED),
            ("Cleared hot on confirmed IRGC vessels", GREEN),
            ("ATFLIR for PID at range", YELLOW),
        ],
        "comms_roles": [
            ("WARHAWKS 1", "305.0", "AM", "SWEEP/STRK", ORANGE),
            ("BLACKSHEEP 1", "270.0", "AM", "ARMED RECON", WHITE),
            ("WITCHER 1", "282.0", "AM", "FWD SPOT", WHITE),
            ("OUTLAWS 1", "127.5", "FM", "ANTI-SURF", WHITE),
            ("PANTHER 1", "325.0", "AM", "HIGH COV (AI)", DIM),
        ],
        "sam_threats": [
            {"name": "MANPADS  -  Islands / boats", "color": ORANGE, "lines": [
                ("Effective below 5000ft AGL", YELLOW),
                ("Expected on islands and boats", WHITE),
                ("Use terrain masking", WHITE),
            ]},
        ],
        "ewr_threats": [],
        "air_threats": [
            {"name": "Residual fighter threat", "lines": [
                ("PANTHER provides air umbrella", WHITE),
                ("Reduced threat if prior missions successful", DIM),
            ]},
        ],
        "warhawks_wps": [
            ("0", "ASSEMBLY", "FL200", "430kt", "Form up"),
            ("1", "SWEEP", "FL200", "430kt", "Sanitize"),
            ("2", "LITTORAL", "10000ft", "350kt", "Assist strike"),
            ("3", "SURFACE TGTS", "8000ft", "300kt", "Light strike"),
            ("4", "RTB AL DHAFRA", "SFC", "---", "Landing"),
        ],
        "warhawks_role": "SWEEP / LIGHT STRIKE",
        "blacksheep_wps": [
            ("0", "ASSEMBLY", "FL200", "430kt", "Form up"),
            ("1", "RECON START", "12000ft", "350kt", "ATFLIR search"),
            ("2", "STRAIT CTR", "10000ft", "300kt", "Engage boats"),
            ("3", "STRAIT EAST", "10000ft", "300kt", "Engage boats"),
            ("4", "RTB CARRIER", "SFC", "---", "Landing"),
        ],
        "blacksheep_role": "ARMED RECON",
        "witcher_wps": [
            ("0", "QESHM COAST", "10000ft", "Recon"),
            ("1", "OIL PLATFORMS", "8000ft", "Search"),
            ("2", "OPT: CMD BOAT", "5000ft", "GBU-12"),
            ("3", "EGRESS SW", "FL200", "RTB"),
            ("4", "RTB AL DHAFRA", "SFC", "Landing"),
        ],
        "witcher_role": "FWD SPOTTER / OPT STRIKE",
        "outlaws_wps": [
            ("0", "HOLD SOUTH", "500ft AGL", "Hold / await"),
            ("1", "ISLAND CHAIN", "200ft AGL", "Low level"),
            ("2", "OPT: LARAK", "150ft AGL", "Attack staging"),
            ("3", "EGRESS SOUTH", "300ft AGL", "Withdraw"),
        ],
        "outlaws_role": "ANTI-SURFACE / DEEP",
        "outlaws_notes": [
            ("OUTLAWS: MANPADS expected at Larak.", YELLOW),
            ("Use terrain masking, max Hellfire range.", YELLOW),
        ],
        "tactics": [
            {"heading": "ANTI-SURFACE TACTICS", "lines": [
                ("1. ATFLIR PID at max range", WHITE),
                ("2. Rockeye/Mk-82 on boat groups", WHITE),
                ("3. Boghammars use oil platforms as cover", YELLOW),
                ("4. Stay above 5000ft (MANPADS)", WHITE),
                ("5. Watch for dhow traffic (civilian)", YELLOW),
            ]},
            {"heading": "BOGHAMMAR IDENTIFICATION", "lines": [
                ("- Military: wake pattern, weapons visible", WHITE),
                ("- RPGs, heavy MG, some C-701 AShM", WHITE),
                ("- Groups of 3-5 boats = military", WHITE),
                ("- Single boats may be civilian", YELLOW),
            ]},
        ],
        "critical_notes": [
            ("- PID MANDATORY - civilian boats present", RED),
            ("- Boghammars use oil platforms as cover", RED),
            ("- Below 5000ft AGL = MANPADS range", YELLOW),
            ("- Command boat kill disrupts swarm", YELLOW),
            ("- Tanker SHELL 1 on 317.0 / 57X", WHITE),
        ],
    },
    5: {
        "codename": "PERSIAN STORM",
        "type": "Deep Strike (Night)",
        "datetime": "19 APR 1995 / 0530L",
        "weather": "Clear, scattered clouds, wind 330/02kt, 26C",
        "objective_lines": [
            ("Night strike on Bandar Abbas airfield.", WHITE),
            ("Degrade Iranian air regeneration capability.", WHITE),
        ],
        "pri_objectives": [
            "Bandar Abbas: HAS shelters, runway, fuel",
            "Suppress Bandar Abbas SA-15 and SA-2",
        ],
        "opt_objectives": [
            "Qeshm radar complex (WITCHER)",
            "Interdict fleeing Houdong boats (OUTLAWS)",
        ],
        "package": [
            ("WARHAWKS 1   F-16C   SEAD lead (Player)", ORANGE),
            ("BLACKSHEEP 1 F/A-18C Night strike x4 (Client)", WHITE),
            ("WITCHER 1    M-2000C OPT strike (Client)", WHITE),
            ("OUTLAWS 1    AH-64D  Ambush x2 (Client)", WHITE),
            ("PANTHER 1    F-15C   Night sweep x2 (AI)", DIM),
            ("OVERLORD     E-3A    AWACS (AI)", DIM),
            ("SHELL 1      KC-135  Tanker (AI)", DIM),
        ],
        "timeline": [
            "0530L  Package airborne, NVG flight",
            "0540L  Low level ingress through Strait",
            "0550L  Pop-up at IP COBRA (30nm south)",
            "0555L  WARHAWKS SEAD - suppress SA-15",
            "0600L  BLACKSHEEP strike Bandar Abbas",
            "       WITCHER breaks for Qeshm radar",
            "       OUTLAWS ambush in narrows",
            "0615L  Egress SW over water, RTB",
        ],
        "roe": [
            ("Weapons FREE on military targets in box", GREEN),
            ("Avoid civilian terminal (east side)", RED),
            ("Precision weapons only near city", YELLOW),
        ],
        "comms_roles": [
            ("WARHAWKS 1", "305.0", "AM", "SEAD LEAD", ORANGE),
            ("BLACKSHEEP 1", "270.0", "AM", "NIGHT STRK", WHITE),
            ("WITCHER 1", "282.0", "AM", "OPT STRIKE", WHITE),
            ("OUTLAWS 1", "127.5", "FM", "AMBUSH", WHITE),
            ("PANTHER 1", "325.0", "AM", "NIT SWEEP (AI)", DIM),
        ],
        "sam_threats": [
            {"name": "SA-15 TOR  -  Bandar Abbas airfield", "color": RED, "lines": [
                ("IR-GUIDED - NO RWR WARNING", RED),
                ("Range: 12 km  |  Alt: 10-6000m", YELLOW),
                ("Use HTS for co-located acq radar", WHITE),
                ("PRIORITY SEAD TARGET", ORANGE),
            ]},
            {"name": "SA-2 GUIDELINE  -  Bandar Abbas", "color": RED, "lines": [
                ("Track: SNR-75 Fan Song", WHITE),
                ("Range: 40 km", YELLOW),
                ("Secondary SEAD target", WHITE),
            ]},
            {"name": "Dense AAA  -  Bandar Abbas airfield", "color": ORANGE, "lines": [
                ("ZSU-23-4, AAA batteries", WHITE),
                ("Lethal below 8000ft", RED),
            ]},
        ],
        "ewr_threats": [
            {"name": "Qeshm radar complex (OPT target)", "lines": [
                "Tall King EWR + Flat Face search radar",
                "WITCHER optional target",
            ]},
        ],
        "air_threats": [
            {"name": "F-4E PHANTOM II (night CAP)", "lines": [
                ("GCI-directed from Shiraz", WHITE),
                ("PANTHER sweeps ingress corridor", YELLOW),
            ]},
        ],
        "warhawks_wps": [
            ("0", "ASSEMBLY", "FL200", "430kt", "Form up NVG"),
            ("1", "LOW LEVEL", "500ft AGL", "280kt", "Ingress"),
            ("2", "IP COBRA", "5000ft", "410kt", "Pop-up"),
            ("3", "BANDAR ABBAS", "FL180", "410kt", "SEAD SA-15"),
            ("4", "RTB AL DHAFRA", "SFC", "---", "Landing"),
        ],
        "warhawks_role": "SEAD LEAD",
        "blacksheep_wps": [
            ("0", "ASSEMBLY", "FL200", "430kt", "Form up NVG"),
            ("1", "LOW LEVEL", "500ft AGL", "280kt", "Ingress"),
            ("2", "IP COBRA", "5000ft", "350kt", "Pop-up"),
            ("3", "BANDAR ABBAS", "16400ft", "390kt", "JDAM/LGB"),
            ("4", "RTB CARRIER", "SFC", "---", "Landing"),
        ],
        "blacksheep_role": "NIGHT STRIKE",
        "witcher_wps": [
            ("0", "WITH PACKAGE", "FL200", "Follow package"),
            ("1", "BREAK SOUTH", "FL150", "Split 50nm out"),
            ("2", "OPT: QESHM", "5000ft", "ATLIS/GBU-12"),
            ("3", "EGRESS SW", "FL200", "RTB"),
            ("4", "RTB AL DHAFRA", "SFC", "Landing"),
        ],
        "witcher_role": "OPT RADAR STRIKE",
        "outlaws_wps": [
            ("0", "NARROWS", "200ft AGL", "Deploy NVG"),
            ("1", "AMBUSH POS", "150ft AGL", "Set ambush"),
            ("2", "ENGAGE", "150ft AGL", "Hellfire boats"),
            ("3", "EGRESS SOUTH", "300ft AGL", "Withdraw"),
        ],
        "outlaws_role": "AMBUSH / ANTI-SHIP",
        "outlaws_notes": [
            ("OUTLAWS: NVG flight in the narrows.", YELLOW),
            ("Do NOT proceed north - friendly traffic overhead.", YELLOW),
        ],
        "tactics": [
            {"heading": "NIGHT SEAD - WARHAWKS", "lines": [
                ("1. SA-15 is IR-guided - NO RWR WARNING", RED),
                ("2. Use HTS to find acquisition radar", WHITE),
                ("3. HARM the co-located radar first", WHITE),
                ("4. Secondary: SA-2 at Bandar Abbas", WHITE),
                ("5. Lead the package in", WHITE),
            ]},
            {"heading": "NIGHT STRIKE - BLACKSHEEP", "lines": [
                ("1. Low level ingress, pop at IP COBRA", WHITE),
                ("2. JDAM on HAS shelters + runway", WHITE),
                ("3. LGB on fuel depot (ATFLIR lase)", WHITE),
                ("4. Precision weapons ONLY near city", YELLOW),
                ("5. Avoid civilian terminal (east side)", RED),
            ]},
        ],
        "critical_notes": [
            ("- SA-15 = IR guided, NO RWR WARNING", RED),
            ("- Dense AAA around Bandar Abbas", RED),
            ("- Avoid civilian terminal (east side)", YELLOW),
            ("- Night favors coalition - use NVG", YELLOW),
            ("- Tanker SHELL 1 post-strike 317.0/57X", WHITE),
        ],
    },
}


# =========================================
# PAGE GENERATORS (data-driven)
# =========================================
def page_mission_brief(m):
    img, d = new_page()
    y = draw_header(d, "MISSION BRIEF", f"OPERATION BURNING STRAITS - MISSION {m['_num']}")

    y = draw_section(d, y, "OVERVIEW")
    y = draw_row(d, y, "Operation", m["codename"])
    y = draw_row(d, y, "Type", m["type"])
    y = draw_row(d, y, "Date/Time", m["datetime"])
    y = draw_row(d, y, "Theatre", "Persian Gulf")
    y = draw_row(d, y, "Weather", m["weather"])
    y += 8

    y = draw_section(d, y, "OBJECTIVE")
    for line, color in m["objective_lines"]:
        y = draw_text(d, y, line, color)
    y += 5
    for obj in m["pri_objectives"]:
        y = draw_text(d, y, f"PRI: {obj}", ORANGE)
    for obj in m["opt_objectives"]:
        y = draw_text(d, y, f"OPT: {obj}", DIM)
    y += 8

    y = draw_section(d, y, "PACKAGE COMPOSITION")
    for line, color in m["package"]:
        y = draw_text(d, y, line, color)
    y += 8

    y = draw_section(d, y, "TIMELINE")
    for line in m["timeline"]:
        y = draw_text(d, y, line)

    y += 8
    y = draw_section(d, y, "ROE")
    for line, color in m["roe"]:
        y = draw_text(d, y, line, color)

    draw_footer(d, 1, 5, m["codename"])
    return img


def page_comms(m):
    img, d = new_page()
    y = draw_header(d, "COMMS CARD", "FREQUENCIES / CALLSIGNS / SUPPORT")

    y = draw_section(d, y, "FLIGHT FREQUENCIES")
    d.text((55, y), "CALLSIGN", fill=CYAN, font=fonts["small"])
    d.text((230, y), "FREQ", fill=CYAN, font=fonts["small"])
    d.text((370, y), "MOD", fill=CYAN, font=fonts["small"])
    d.text((440, y), "ROLE", fill=CYAN, font=fonts["small"])
    y += 20

    for callsign, freq, mod, role, color in m["comms_roles"]:
        d.text((55, y), callsign, fill=color, font=fonts["body"])
        d.text((230, y), freq, fill=WHITE, font=fonts["body"])
        d.text((370, y), mod, fill=DIM, font=fonts["body"])
        d.text((440, y), role, fill=DIM, font=fonts["body"])
        y += 22
    y += 10

    y = draw_section(d, y, "SUPPORT ASSETS")
    d.text((55, y), "ASSET", fill=CYAN, font=fonts["small"])
    d.text((230, y), "FREQ", fill=CYAN, font=fonts["small"])
    d.text((370, y), "TACAN", fill=CYAN, font=fonts["small"])
    d.text((500, y), "ALT", fill=CYAN, font=fonts["small"])
    y += 20

    support = [
        ("OVERLORD (AWACS)", "251.0 AM", "---", "FL300"),
        ("SHELL 1 (Tanker)", "317.0 AM", "57X", "FL220"),
    ]
    for name, freq, tacan, alt in support:
        d.text((55, y), name, fill=WHITE, font=fonts["body"])
        d.text((230, y), freq, fill=WHITE, font=fonts["body"])
        d.text((370, y), tacan, fill=YELLOW, font=fonts["body"])
        d.text((500, y), alt, fill=DIM, font=fonts["body"])
        y += 22
    y += 10

    y = draw_section(d, y, "TANKER DETAILS")
    y = draw_row(d, y, "Track", "EXXON")
    y = draw_row(d, y, "Type", "KC-135 MPRS (boom)")
    y = draw_row(d, y, "TACAN", "57X  (SHL)", value_color=YELLOW)
    y = draw_row(d, y, "Altitude", "FL220")
    y = draw_row(d, y, "Speed", "290 KTAS")
    y += 10

    y = draw_section(d, y, "BULLSEYE")
    y = draw_text(d, y, "BLUE:  Strait reference point", YELLOW)
    y = draw_text_small(d, y, "All threat calls from OVERLORD reference bullseye")
    y += 10

    y = draw_section(d, y, "AUTHENTICATION")
    y = draw_text(d, y, "IFF Mode 3:  As briefed")
    y = draw_text(d, y, "Challenge:   SUNRISE / DELTA")

    draw_footer(d, 2, 5, m["codename"])
    return img


def page_threats(m):
    img, d = new_page()
    y = draw_header(d, "THREAT CARD", "ENEMY ORDER OF BATTLE / IADS")

    y = draw_section(d, y, "SURFACE-TO-AIR THREATS")
    for threat in m["sam_threats"]:
        d.rectangle([50, y, 56, y+6], fill=threat["color"])
        d.text((65, y - 3), threat["name"], fill=threat["color"], font=fonts["heading"])
        y += 26
        for line, color in threat["lines"]:
            y = draw_text(d, y, line, color)
        y += 6

    for ewr in m.get("ewr_threats", []):
        d.rectangle([50, y, 56, y+6], fill=DIM)
        d.text((65, y - 3), ewr["name"], fill=DIM, font=fonts["heading"])
        y += 26
        for line in ewr["lines"]:
            y = draw_text(d, y, line, DIM)
        y += 6

    if m["air_threats"]:
        y += 2
        y = draw_section(d, y, "AIR THREATS")
        for threat in m["air_threats"]:
            d.rectangle([50, y, 56, y+6], fill=RED)
            d.text((65, y - 3), threat["name"], fill=RED, font=fonts["heading"])
            y += 26
            for line, color in threat["lines"]:
                y = draw_text(d, y, line, color)
            y += 6

    draw_footer(d, 3, 5, m["codename"])
    return img


def page_flightplan_fixedwing(m):
    img, d = new_page()
    y = draw_header(d, "FLIGHT PLANS", "WAYPOINTS - FIXED WING")

    def draw_wp_table_5col(section_title, waypoints):
        nonlocal y
        y = draw_section(d, y, section_title)
        d.text((55, y), "WP", fill=CYAN, font=fonts["small"])
        d.text((90, y), "NAME", fill=CYAN, font=fonts["small"])
        d.text((310, y), "ALT", fill=CYAN, font=fonts["small"])
        d.text((400, y), "SPD", fill=CYAN, font=fonts["small"])
        d.text((490, y), "ACTION", fill=CYAN, font=fonts["small"])
        y += 18
        for wp, name, alt, spd, action in waypoints:
            d.text((55, y), wp, fill=WHITE, font=fonts["body"])
            d.text((90, y), name, fill=WHITE, font=fonts["body"])
            d.text((310, y), alt, fill=DIM, font=fonts["body"])
            d.text((400, y), spd, fill=DIM, font=fonts["body"])
            d.text((490, y), action, fill=DIM, font=fonts["body"])
            y += 20
        y += 10

    def draw_wp_table_4col(section_title, waypoints):
        nonlocal y
        y = draw_section(d, y, section_title)
        d.text((55, y), "WP", fill=CYAN, font=fonts["small"])
        d.text((90, y), "NAME", fill=CYAN, font=fonts["small"])
        d.text((310, y), "ALT", fill=CYAN, font=fonts["small"])
        d.text((490, y), "ACTION", fill=CYAN, font=fonts["small"])
        y += 18
        for wp, name, alt, action in waypoints:
            d.text((55, y), wp, fill=WHITE, font=fonts["body"])
            d.text((90, y), name, fill=WHITE, font=fonts["body"])
            d.text((310, y), alt, fill=DIM, font=fonts["body"])
            d.text((490, y), action, fill=DIM, font=fonts["body"])
            y += 20
        y += 10

    draw_wp_table_5col(
        f"WARHAWKS 1  (F-16C / {m['warhawks_role']})", m["warhawks_wps"])
    draw_wp_table_5col(
        f"BLACKSHEEP 1  (F/A-18C x4 / {m['blacksheep_role']})", m["blacksheep_wps"])
    draw_wp_table_4col(
        f"WITCHER 1  (M-2000C / {m['witcher_role']})", m["witcher_wps"])

    draw_footer(d, 4, 5, m["codename"])
    return img


def page_flightplan_helo(m):
    img, d = new_page()
    y = draw_header(d, "FLIGHT PLAN / NOTES", "OUTLAWS + MISSION NOTES")

    y = draw_section(d, y, f"OUTLAWS 1  (AH-64D x2 / {m['outlaws_role']})")
    d.text((55, y), "WP", fill=CYAN, font=fonts["small"])
    d.text((90, y), "NAME", fill=CYAN, font=fonts["small"])
    d.text((310, y), "ALT", fill=CYAN, font=fonts["small"])
    d.text((490, y), "ACTION", fill=CYAN, font=fonts["small"])
    y += 18
    for wp, name, alt, action in m["outlaws_wps"]:
        d.text((55, y), wp, fill=WHITE, font=fonts["body"])
        d.text((90, y), name, fill=WHITE, font=fonts["body"])
        d.text((310, y), alt, fill=DIM, font=fonts["body"])
        d.text((490, y), action, fill=DIM, font=fonts["body"])
        y += 20
    y += 5
    for line, color in m["outlaws_notes"]:
        y = draw_text_small(d, y, line, color)
    y += 12

    for tactic in m["tactics"]:
        y = draw_section(d, y, tactic["heading"])
        for line, color in tactic["lines"]:
            y = draw_text(d, y, line, color)
        y += 10

    y = draw_section(d, y, "CRITICAL NOTES")
    for line, color in m["critical_notes"]:
        y = draw_text(d, y, line, color)

    draw_footer(d, 5, 5, m["codename"])
    return img


# =========================================
# GENERATE AND PACKAGE
# =========================================
if __name__ == "__main__":
    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kneeboards")

    for num, mdata in MISSION_DATA.items():
        mdata["_num"] = num
        mission_dir = os.path.join(outdir, f"m{num}")
        os.makedirs(mission_dir, exist_ok=True)

        pages = [
            ("01_mission_brief.png", page_mission_brief),
            ("02_comms_card.png", page_comms),
            ("03_threat_card.png", page_threats),
            ("04_flightplan_fixedwing.png", page_flightplan_fixedwing),
            ("05_flightplan_helo_notes.png", page_flightplan_helo),
        ]

        print(f"Mission {num}: {mdata['codename']}")
        for fname, gen_func in pages:
            img = gen_func(mdata)
            path = os.path.join(mission_dir, fname)
            img.save(path)
            print(f"  Created: {path}")

    print(f"\nDone! Generated kneeboards for {len(MISSION_DATA)} missions.")
