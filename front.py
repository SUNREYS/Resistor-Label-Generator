from PIL import Image, ImageDraw, ImageFont

def get_resistor_data(ohms, color_hex_list):
    color_names = [str(h).capitalize() for h in color_hex_list]

    bands = { "Black": 0, "Brown": 1, "Red": 2, "Orange": 3, "Yellow": 4,
              "Green": 5, "Blue": 6, "Violet": 7, "Grey": 8, "White": 9 }
    
    mults = { "Black": 1, "Brown": 10, "Red": 100, "Orange": 1000, "Yellow": 10000,
              "Green": 100000, "Blue": 1000000, "Violet": 10000000, "Grey": 10000000000, 
              "Gold": 0.1, "Silver": 0.01 }
    
    tols =  { "Brown": "1%", "Red": "2%", "Green": "0.5%", "Blue": "0.25%",
              "Violet": "0.1%", "Grey": "0.05%", "Gold": "5%", "Silver": "10%" }
    
    ppms =  { "Black": "250ppm", "Brown": "100ppm", "Red": "50ppm", "Orange": "15ppm",
              "Yellow": "25ppm", "Blue": "10ppm", "Violet": "5ppm", "Grey": "1ppm" }

    try:
        tolerance = tols.get(color_names[3])
        ppm_text = ""
        if len(color_hex_list) == 6:
            ppm_text = ppms.get(color_names[5], "")

        # Formatting Output Text
        print(ohms)
        if ohms >= 1000000000:
            val_text = f"{ohms/1_000_000_000:.2f}GΩ".replace(".00", "")
        elif ohms >= 1_000_000:
            val_text = f"{ohms/1_000_000:.2f}MΩ".replace(".00", "")
        elif ohms >= 1_000:
            val_text = f"{ohms/1_000:.2f}kΩ".replace(".00", "")
        else:
            val_text = f"{ohms:.2f}Ω".replace(".00", "")

        # #FIX: Background Color Logic
        if ohms < 1000:      bg_color = "#54B67E"
        elif ohms < 10000:   bg_color = "#5CBEFF"
        elif ohms < 100000:  bg_color = "#F4D03F"
        elif ohms < 1000000: bg_color = "#FF8F2C"
        else:               bg_color = "#FF5F4D"

        return val_text, tolerance, bg_color, ppm_text

    except (IndexError, AttributeError):
        return "---", "---", "#CCCCCC", ""
    
# Helper for body themes
def get_theme(style):
    if style == "blue":
        return {"base": "#7FAED9", "shadow": "#5F8DB5", "highlight": "#A9C8E8"}
    else:
        return {"base": "#DDC7A0", "shadow": "#D4BA8D", "highlight": "#E1CCA9"}

# Resistor Visualizer
def draw_resistor_img(colorList, width=900, body_style="beige"):
    base_w = 300
    scale = width / base_w
    height = int(width * 0.33)
    
    img = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    def s(v): return int(v * scale)

    # Leads
    draw.line((0, s(50), width, s(50)), fill="#B8B8B8", width=s(4))
    draw.line((0, s(50), width, s(50)), fill="#CACACA", width=s(3))
    draw.line((0, s(50), width, s(50)), fill="#D1D1D1", width=s(2)) 
    # Body Drawing
    theme = get_theme(body_style)
    ow = s(2) 
    r_base = s(12)
    r_outline = r_base + ow

    # Body Outline
    draw.rounded_rectangle((s(70)-ow, s(22)-ow, s(110)+ow, s(78)+ow), radius=r_outline, fill=theme["shadow"])
    draw.rounded_rectangle((s(190)-ow, s(22)-ow, s(230)+ow, s(78)+ow), radius=r_outline, fill=theme["shadow"])
    draw.rectangle((s(90), s(30)-ow, s(210), s(70)+ow), fill=theme["shadow"])
    # Fill
    draw.rectangle((s(90), s(30), s(210), s(70)), fill=theme["base"])
    draw.rounded_rectangle((s(70), s(22), s(110), s(78)), radius=r_base, fill=theme["base"])
    draw.rounded_rectangle((s(190), s(22), s(230), s(78)), radius=r_base, fill=theme["base"])
    # Highlight
    draw.line((s(70), s(35), s(230), s(35)), fill=theme["highlight"], width=s(3))
    # Bands logic
    if len(colorList) == 6:
        positions = [86, 114, 130, 146, 162, 205] 
    elif len(colorList) == 5:
        positions = [86, 114, 130, 146, 162]
    else:
        positions = [86, 114, 130, 158]

    for i, color in enumerate(colorList):
        if i < len(positions):
            x = s(positions[i])
            orig_x = positions[i]
            on_bulb = (orig_x < 110 or orig_x > 190)
            
            y1 = s(19) if on_bulb else s(27)
            y2 = s(81) if on_bulb else s(73)
            
            draw.rectangle((x, y1+s(1), x + s(10), y2-s(1)), fill=color)

    return img

# Label Generator
def draw_resistor_label(raw_ohms, colorList, body_style="beige", watt="0.25"):
    w, h = 1800, 300
    img = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    # Get data
    val_text, tol_text, bg_color, ppm_text = get_resistor_data(raw_ohms, colorList)
    zone_1 = int(w * 0.30)
    zone_2 = int(w * 0.70)
    draw.rectangle((0, 0, zone_1, h), fill=bg_color)
    draw.rectangle((zone_1, 0, zone_2, h), fill="#212121")
    draw.rectangle((zone_2, 0, w, h), fill=bg_color)

    large_size = 120 if len(val_text) <= 5 else 90
    font_large = ImageFont.truetype("osifont.ttf", large_size)
    font_small = ImageFont.truetype("osifont.ttf", 60)

    specs_y = []
    if len(colorList) == 6:
        specs_y = [h/2 - 75, h/2 - 5, h/2 + 60] # Watt, Tolerance, PPM
    else:
        specs_y = [h/2 - 60, h/2 + 30] # Watt, Tolerance
        if ppm_text:
            specs_y.append(h/2 + 75)

    draw.text((zone_1 / 2, h / 2), val_text, fill="black", font=font_large, anchor="mm")
    # Draw Watt
    draw.text((zone_2 + (w - zone_2)/2, specs_y[0]), watt + "W", fill="black", font=font_small, anchor="mm")
    # Draw Tolerance
    draw.text((zone_2 + (w - zone_2)/2, specs_y[1]), tol_text, fill="black", font=font_small, anchor="mm")
    # Draw PPM (if exists)
    if ppm_text:
        draw.text((zone_2 + (w - zone_2)/2, specs_y[-1]), ppm_text, fill="black", font=font_small, anchor="mm")

    # Resistor Drawing
    cx, cy = w / 2, h / 2
    res_scale = 3.5
    def sl(v): return int(v * res_scale)
    def get_x(orig_x): return cx + (orig_x - 150) * res_scale

    theme = get_theme(body_style)

    draw.line((zone_1, cy, zone_2, cy), fill="#B8B8B8", width=sl(4))
    draw.line((zone_1, cy, zone_2, cy), fill="#CACACA", width=sl(3))
    draw.line((zone_1, cy, zone_2, cy), fill="#D1D1D1", width=sl(2)) 
    ow = sl(3)
    r_base = sl(12)
    r_outline = r_base + ow

    # Outline
    draw.rounded_rectangle((get_x(70)-ow, cy - sl(28)-ow, get_x(110)+ow, cy + sl(28)+ow), radius=r_outline, fill=theme["shadow"])
    draw.rounded_rectangle((get_x(190)-ow, cy - sl(28)-ow, get_x(230)+ow, cy + sl(28)+ow), radius=r_outline, fill=theme["shadow"])
    draw.rectangle((get_x(90), cy - sl(20)-ow, get_x(210), cy + sl(20)+ow), fill=theme["shadow"])
    # Fill
    draw.rectangle((get_x(90), cy - sl(20), get_x(210), cy + sl(20)), fill=theme["base"])
    draw.rounded_rectangle((get_x(70), cy - sl(28), get_x(110), cy + sl(28)), radius=r_base, fill=theme["base"])
    draw.rounded_rectangle((get_x(190), cy - sl(28), get_x(230), cy + sl(28)), radius=r_base, fill=theme["base"])
    # Highlight
    draw.line((get_x(70), cy - sl(15), get_x(230), cy - sl(15)), fill=theme["highlight"], width=sl(3))

    if len(colorList) == 6:
        # Scaled positions for 6 bands
        positions = [86, 114, 130, 146, 162, 205] 
    elif len(colorList) == 5:
        positions = [86, 114, 130, 146, 162]
    else:
        positions = [86, 114, 130, 158]

    for i, color in enumerate(colorList):
        if i < len(positions):
            bx = get_x(positions[i])
            orig_x = positions[i]
            on_bulb = (orig_x < 100 or orig_x > 190)
            by1 = cy - (sl(32) if on_bulb else sl(24))
            by2 = cy + (sl(32) if on_bulb else sl(24))
            draw.rectangle((bx, by1+sl(1), bx + sl(10), by2-sl(1)), fill=color)

    return img