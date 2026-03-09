#!/usr/bin/env python3
"""
Generate kneeboard PNG pages for Operation Sledgehammer.
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
    paths = [
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/SFMono-Regular.otf",
        "/Library/Fonts/SF-Mono-Regular.otf",
        "/System/Library/Fonts/Monaco.dfont",
        "/System/Library/Fonts/Courier.dfont",
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

def draw_footer(draw, page_num, total):
    draw.line([(30, H - 40), (W - 30, H - 40)], fill=LINE_COLOR, width=1)
    draw.text((W // 2, H - 25), f"OP SLEDGEHAMMER  -  Page {page_num}/{total}", fill=DIM, font=fonts["small"], anchor="mt")

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
# PAGE 1: MISSION BRIEF
# =========================================
def page_mission_brief():
    img, d = new_page()
    y = draw_header(d, "MISSION BRIEF", "OPERATION BURNING STRAITS - MISSION 1")

    y = draw_section(d, y, "OVERVIEW")
    y = draw_row(d, y, "Operation", "SLEDGEHAMMER")
    y = draw_row(d, y, "Type", "SEAD / DEAD")
    y = draw_row(d, y, "Date/Time", "15 APR 1995 / 0430L")
    y = draw_row(d, y, "Theatre", "Persian Gulf")
    y = draw_row(d, y, "Weather", "Clear, wind 340/02kt, 25C")
    y += 8

    y = draw_section(d, y, "OBJECTIVE")
    y = draw_text(d, y, "Degrade Iranian IADS to enable")
    y = draw_text(d, y, "follow-on strike operations.")
    y += 5
    y = draw_text(d, y, "PRI: SA-6 Kub on Abu Musa Island", ORANGE)
    y = draw_text(d, y, "PRI: HAWK on Greater Tunb Island", ORANGE)
    y = draw_text(d, y, "OPT: 1L13 EWR on Qeshm (WITCHER)", DIM)
    y = draw_text(d, y, "OPT: ZSU-23 AAA Abu Musa (OUTLAWS)", DIM)
    y += 8

    y = draw_section(d, y, "PACKAGE COMPOSITION")
    y = draw_text(d, y, "WARHAWKS 1   F-16C   SEAD (Player)", ORANGE)
    y = draw_text(d, y, "BLACKSHEEP 1 F/A-18C DEAD x4 (Client)", WHITE)
    y = draw_text(d, y, "WITCHER 1    M-2000C Sweep (Client)", WHITE)
    y = draw_text(d, y, "OUTLAWS 1    AH-64D  CAS x2 (Client)", WHITE)
    y = draw_text(d, y, "PANTHER 1    F-15C   Escort x2 (AI)", DIM)
    y = draw_text(d, y, "OVERLORD     E-3A    AWACS (AI)", DIM)
    y = draw_text(d, y, "SHELL 1      KC-135  Tanker (AI)", DIM)
    y += 8

    y = draw_section(d, y, "TIMELINE")
    y = draw_text(d, y, "0430L  Package airborne at assembly")
    y = draw_text(d, y, "0440L  Push - WARHAWKS lead, SEAD")
    y = draw_text(d, y, "0445L  BLACKSHEEP IP for Abu Musa")
    y = draw_text(d, y, "0445L  OUTLAWS low-level approach")
    y = draw_text(d, y, "       WITCHER sweep eastern flank")
    y = draw_text(d, y, "0500L  Egress SW, RTB Al Dhafra")

    y += 8
    y = draw_section(d, y, "ROE")
    y = draw_text(d, y, "Weapons FREE on radiating SAMs", GREEN)
    y = draw_text(d, y, "PID required on all air contacts", YELLOW)
    y = draw_text(d, y, "OVERLORD controls intercepts", WHITE)

    draw_footer(d, 1, 5)
    return img

# =========================================
# PAGE 2: COMMS CARD
# =========================================
def page_comms():
    img, d = new_page()
    y = draw_header(d, "COMMS CARD", "FREQUENCIES / CALLSIGNS / SUPPORT")

    y = draw_section(d, y, "FLIGHT FREQUENCIES")
    # Table header
    d.text((55, y), "CALLSIGN", fill=CYAN, font=fonts["small"])
    d.text((230, y), "FREQ", fill=CYAN, font=fonts["small"])
    d.text((370, y), "MOD", fill=CYAN, font=fonts["small"])
    d.text((440, y), "ROLE", fill=CYAN, font=fonts["small"])
    y += 20
    draw_line = lambda d, y: (d.line([(50, y-2), (W-50, y-2)], fill=LINE_COLOR), y)

    rows = [
        ("WARHAWKS 1", "305.0", "AM", "SEAD", ORANGE),
        ("BLACKSHEEP 1", "270.0", "AM", "DEAD", WHITE),
        ("WITCHER 1", "282.0", "AM", "SWEEP/STRIKE", WHITE),
        ("OUTLAWS 1", "127.5", "FM", "CAS/AAA", WHITE),
        ("PANTHER 1", "325.0", "AM", "ESCORT (AI)", DIM),
    ]
    for callsign, freq, mod, role, color in rows:
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

    draw_footer(d, 2, 5)
    return img

# =========================================
# PAGE 3: THREAT CARD
# =========================================
def page_threats():
    img, d = new_page()
    y = draw_header(d, "THREAT CARD", "ENEMY ORDER OF BATTLE / IADS")

    y = draw_section(d, y, "SURFACE-TO-AIR THREATS")
    # SA-6
    d.rectangle([50, y, 56, y+6], fill=RED)
    d.text((65, y - 3), "SA-6 KUB  -  Abu Musa Island", fill=RED, font=fonts["heading"])
    y += 26
    y = draw_text(d, y, "Tracking: 1S91 SURN (CW + pulse)")
    y = draw_text(d, y, "Search:   P-19 Flat Face")
    y = draw_text(d, y, "Launchers: 4x 2P25 (3 missiles each)")
    y = draw_text(d, y, "Range: 24 km  |  Alt: 100-14000m", YELLOW)
    y = draw_text(d, y, "NOTE: PRIMARY TARGET", ORANGE)
    y += 6

    # HAWK
    d.rectangle([50, y, 56, y+6], fill=RED)
    d.text((65, y - 3), "HAWK  -  Greater Tunb Island", fill=RED, font=fonts["heading"])
    y += 26
    y = draw_text(d, y, "Track: AN/MPQ-46 High Power Illum.")
    y = draw_text(d, y, "Search: AN/MPQ-50")
    y = draw_text(d, y, "Launchers: 3x M192")
    y = draw_text(d, y, "Range: 40 km  |  Alt: 60-18000m", YELLOW)
    y = draw_text(d, y, "COVERS EGRESS LANE", ORANGE)
    y += 6

    # SA-2
    d.rectangle([50, y, 56, y+6], fill=ORANGE)
    d.text((65, y - 3), "SA-2 GUIDELINE  -  Qeshm Island", fill=ORANGE, font=fonts["heading"])
    y += 26
    y = draw_text(d, y, "Track: SNR-75 Fan Song")
    y = draw_text(d, y, "Launchers: 6x S-75M")
    y = draw_text(d, y, "Range: 40 km  |  Alt: 500-25000m", YELLOW)
    y += 6

    # AAA
    d.rectangle([50, y, 56, y+6], fill=ORANGE)
    d.text((65, y - 3), "ZSU-23-4 AAA  -  Abu Musa", fill=ORANGE, font=fonts["heading"])
    y += 26
    y = draw_text(d, y, "4x Shilka  |  Range: 2.5 km")
    y = draw_text(d, y, "LETHAL below 8000ft AGL", RED)
    y += 6

    # EWR
    d.rectangle([50, y, 56, y+6], fill=DIM)
    d.text((65, y - 3), "1L13 EWR  -  Qeshm Island", fill=DIM, font=fonts["heading"])
    y += 26
    y = draw_text(d, y, "Early warning radar - feeds GCI", DIM)
    y = draw_text(d, y, "Optional target for WITCHER", DIM)
    y += 8

    y = draw_section(d, y, "AIR THREATS")
    d.rectangle([50, y, 56, y+6], fill=RED)
    d.text((65, y - 3), "MiG-29A FULCRUM  x2", fill=RED, font=fonts["heading"])
    y += 26
    y = draw_text(d, y, "Base: Bandar Abbas")
    y = draw_text(d, y, "Weapons: R-27R/T (BVR), R-73 (WVR)")
    y = draw_text(d, y, "SCRAMBLE ~8min after first shots", RED)
    y = draw_text(d, y, "PANTHER will engage, stay aware", YELLOW)

    draw_footer(d, 3, 5)
    return img

# =========================================
# PAGE 4: FLIGHT PLANS (Fixed Wing)
# =========================================
def page_flightplan_fixedwing():
    img, d = new_page()
    y = draw_header(d, "FLIGHT PLANS", "WAYPOINTS - FIXED WING")

    # WARHAWKS
    y = draw_section(d, y, "WARHAWKS 1  (F-16C / SEAD)")
    d.text((55, y), "WP", fill=CYAN, font=fonts["small"])
    d.text((90, y), "NAME", fill=CYAN, font=fonts["small"])
    d.text((310, y), "ALT", fill=CYAN, font=fonts["small"])
    d.text((400, y), "SPD", fill=CYAN, font=fonts["small"])
    d.text((490, y), "ACTION", fill=CYAN, font=fonts["small"])
    y += 18
    wps_w = [
        ("0", "ASSEMBLY", "FL200", "430kt", "Form up"),
        ("1", "PUSH", "FL180", "410kt", "SEAD engage"),
        ("2", "ABU MUSA", "FL180", "410kt", "Kill SA-6 radar"),
        ("3", "GREATER TUNB", "FL180", "410kt", "Kill HAWK radar"),
        ("4", "RTB AL DHAFRA", "SFC", "---", "Landing"),
    ]
    for wp, name, alt, spd, action in wps_w:
        d.text((55, y), wp, fill=WHITE, font=fonts["body"])
        d.text((90, y), name, fill=WHITE, font=fonts["body"])
        d.text((310, y), alt, fill=DIM, font=fonts["body"])
        d.text((400, y), spd, fill=DIM, font=fonts["body"])
        d.text((490, y), action, fill=DIM, font=fonts["body"])
        y += 20
    y += 10

    # BLACKSHEEP
    y = draw_section(d, y, "BLACKSHEEP 1  (F/A-18C x4 / DEAD)")
    d.text((55, y), "WP", fill=CYAN, font=fonts["small"])
    d.text((90, y), "NAME", fill=CYAN, font=fonts["small"])
    d.text((310, y), "ALT", fill=CYAN, font=fonts["small"])
    d.text((400, y), "SPD", fill=CYAN, font=fonts["small"])
    d.text((490, y), "ACTION", fill=CYAN, font=fonts["small"])
    y += 18
    wps_b = [
        ("0", "ASSEMBLY", "FL200", "430kt", "Form up"),
        ("1", "PUSH", "FL200", "410kt", "---"),
        ("2", "IP", "16400ft", "390kt", "Descend, setup"),
        ("3", "ABU MUSA SA-6", "16400ft", "390kt", "BOMB SA-6"),
        ("4", "RTB AL DHAFRA", "SFC", "---", "Landing"),
    ]
    for wp, name, alt, spd, action in wps_b:
        d.text((55, y), wp, fill=WHITE, font=fonts["body"])
        d.text((90, y), name, fill=WHITE, font=fonts["body"])
        d.text((310, y), alt, fill=DIM, font=fonts["body"])
        d.text((400, y), spd, fill=DIM, font=fonts["body"])
        d.text((490, y), action, fill=DIM, font=fonts["body"])
        y += 20
    y += 10

    # WITCHER
    y = draw_section(d, y, "WITCHER 1  (M-2000C / SWEEP + OPT)")
    d.text((55, y), "WP", fill=CYAN, font=fonts["small"])
    d.text((90, y), "NAME", fill=CYAN, font=fonts["small"])
    d.text((310, y), "ALT", fill=CYAN, font=fonts["small"])
    d.text((490, y), "ACTION", fill=CYAN, font=fonts["small"])
    y += 18
    wps_v = [
        ("0", "EAST FLANK", "FL200", "Depart east"),
        ("1", "SWEEP AHEAD", "FL200", "A/A sweep"),
        ("2", "OPT: QESHM EWR", "16400ft", "Bomb EWR"),
        ("3", "EGRESS", "FL200", "Turn south"),
        ("4", "RTB AL DHAFRA", "SFC", "Landing"),
    ]
    for wp, name, alt, action in wps_v:
        d.text((55, y), wp, fill=WHITE, font=fonts["body"])
        d.text((90, y), name, fill=WHITE, font=fonts["body"])
        d.text((310, y), alt, fill=DIM, font=fonts["body"])
        d.text((490, y), action, fill=DIM, font=fonts["body"])
        y += 20

    draw_footer(d, 4, 5)
    return img

# =========================================
# PAGE 5: FLIGHT PLAN (OUTLAWS) + NOTES
# =========================================
def page_flightplan_helo():
    img, d = new_page()
    y = draw_header(d, "FLIGHT PLAN / NOTES", "OUTLAWS + MISSION NOTES")

    y = draw_section(d, y, "OUTLAWS 1  (AH-64D x2 / OPT CAS)")
    d.text((55, y), "WP", fill=CYAN, font=fonts["small"])
    d.text((90, y), "NAME", fill=CYAN, font=fonts["small"])
    d.text((310, y), "ALT", fill=CYAN, font=fonts["small"])
    d.text((490, y), "ACTION", fill=CYAN, font=fonts["small"])
    y += 18
    wps_o = [
        ("0", "HOLD SOUTH", "500ft AGL", "Hold / await"),
        ("1", "APPROACH", "300ft AGL", "Low level"),
        ("2", "ABU MUSA SHORE", "150ft AGL", "Engage ZSU-23"),
        ("3", "EGRESS SOUTH", "300ft AGL", "Withdraw"),
    ]
    for wp, name, alt, action in wps_o:
        d.text((55, y), wp, fill=WHITE, font=fonts["body"])
        d.text((90, y), name, fill=WHITE, font=fonts["body"])
        d.text((310, y), alt, fill=DIM, font=fonts["body"])
        d.text((490, y), action, fill=DIM, font=fonts["body"])
        y += 20
    y += 5
    y = draw_text_small(d, y, "OUTLAWS: Coordinate with BLACKSHEEP timing.", YELLOW)
    y = draw_text_small(d, y, "AAA must be suppressed before DEAD flight crosses beach.", YELLOW)
    y += 12

    y = draw_section(d, y, "SEAD TACTICS - WARHAWKS")
    y = draw_text(d, y, "1. Monitor HTS for emitters on push")
    y = draw_text(d, y, "2. Priority: SA-6 SURN (1S91)")
    y = draw_text(d, y, "   Fire HARM on tracking radar")
    y = draw_text(d, y, "3. Secondary: HAWK TR on Greater Tunb")
    y = draw_text(d, y, "4. Conserve 1 HARM for egress cover")
    y = draw_text(d, y, "5. SA-2 on Qeshm - avoid, not tasked", DIM)
    y += 10

    y = draw_section(d, y, "DEAD TACTICS - BLACKSHEEP")
    y = draw_text(d, y, "1. Hold at IP until WARHAWKS calls")
    y = draw_text(d, y, "   'Magnum' (HARM away)")
    y = draw_text(d, y, "2. Roll in on SA-6 launchers + radar")
    y = draw_text(d, y, "3. Use precision weapons if loaded")
    y = draw_text(d, y, "4. Stay above 8000ft (AAA)")
    y = draw_text(d, y, "5. Egress SW immediately after drop")
    y += 10

    y = draw_section(d, y, "CRITICAL NOTES")
    y = draw_text(d, y, "- MiG-29 scramble ~8 min after push", RED)
    y = draw_text(d, y, "- PANTHER will engage, maintain SA", RED)
    y = draw_text(d, y, "- HAWK covers egress - stay low or", YELLOW)
    y = draw_text(d, y, "  ensure WARHAWKS has killed TR", YELLOW)
    y = draw_text(d, y, "- Tanker SHELL 1 on 317.0 / 57X", WHITE)

    draw_footer(d, 5, 5)
    return img


# =========================================
# GENERATE AND PACKAGE
# =========================================
if __name__ == "__main__":
    outdir = os.path.expanduser("~/Projects/dcs-burning-straits/kneeboards")
    os.makedirs(outdir, exist_ok=True)

    pages = [
        ("01_mission_brief.png", page_mission_brief),
        ("02_comms_card.png", page_comms),
        ("03_threat_card.png", page_threats),
        ("04_flightplan_fixedwing.png", page_flightplan_fixedwing),
        ("05_flightplan_helo_notes.png", page_flightplan_helo),
    ]

    for fname, gen_func in pages:
        img = gen_func()
        path = os.path.join(outdir, fname)
        img.save(path)
        print(f"  Created: {path}")

    # Also inject into the .miz file
    miz_path = os.path.expanduser("~/Projects/dcs-burning-straits/Operation_Sledgehammer.miz")
    if os.path.exists(miz_path):
        import zipfile
        # Read existing miz
        tmp_miz = miz_path + ".tmp"
        with zipfile.ZipFile(miz_path, 'r') as zin:
            with zipfile.ZipFile(tmp_miz, 'w') as zout:
                for item in zin.infolist():
                    zout.writestr(item, zin.read(item.filename))
                # Add kneeboard images
                for fname, _ in pages:
                    img_path = os.path.join(outdir, fname)
                    arcname = f"KNEEBOARD/IMAGES/{fname}"
                    zout.write(img_path, arcname)
                    print(f"  Added to .miz: {arcname}")
        shutil.move(tmp_miz, miz_path)
        print(f"\n  Updated: {miz_path}")
    else:
        print(f"\n  WARNING: {miz_path} not found, kneeboards saved to {outdir}/ only")

    print("\nDone.")
