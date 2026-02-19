from PIL import Image, ImageDraw, ImageFont
import sys
import os
import resistor_data

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def prefix_conversion(val):
    if val >= 1_000_000_000: return f"{val/1_000_000_000:g}G"
    if val >= 1_000_000: return f"{val/1_000_000:g}M"
    elif val >= 1_000: return f"{val/1_000:g}k"
    else: return f"{val:g}"

def get_resistor_data(ohms, color_list):
    color_names = [str(h).capitalize() for h in color_list]
    try:
        tol_idx = 4 if len(color_list) >= 5 else 3
        tolerance = resistor_data.TOLS.get(color_names[tol_idx], "---")
        ppm_text = resistor_data.PPMS.get(color_names[5], "") if len(color_list) == 6 else ""
        val_text = f"{prefix_conversion(ohms)}Ω"

        if ohms < 1000:      bg_color = "#008000"
        elif ohms < 10000:   bg_color = "#00A7EC"
        elif ohms < 100000:  bg_color = "#F4D03F"
        elif ohms < 1000000: bg_color = "#FF8F2C"
        else:                bg_color = "#C30010"

        return val_text, tolerance, bg_color, ppm_text
    except (IndexError, AttributeError):
        return "---", "---", "#CCCCCC", ""
def get_theme(style):
    if "Metal Film" in style: 
        return {"base": "#7FAED9", "shadow": "#5F8DB5", "highlight": "#A9C8E8"}
    # Default to Carbon Film
    return {"base": "#DDC7A0", "shadow": "#D4BA8D", "highlight": "#E7D0A9"}
def draw_resistor_body(draw, cx, cy, scale, theme, colorList, lead_x1, lead_x2):

    def s(v): return int(v * scale)
    # Calculate position relative to center
    def x(orig_x): return cx + s(orig_x - 150)
    
    # Leads
    draw.line((lead_x1, cy, lead_x2, cy), fill="#B8B8B8", width=s(4))
    draw.line((lead_x1, cy, lead_x2, cy), fill="#CACACA", width=s(3))
    draw.line((lead_x1, cy, lead_x2, cy), fill="#D1D1D1", width=s(2)) 
    
    ow = s(2 if scale < 2 else 3); r_base = s(12); r_outline = r_base + ow

    # Outline
    draw.rounded_rectangle((x(70)-ow, cy-s(28)-ow, x(110)+ow, cy+s(28)+ow), radius=r_outline, fill=theme["shadow"])
    draw.rounded_rectangle((x(190)-ow, cy-s(28)-ow, x(230)+ow, cy+s(28)+ow), radius=r_outline, fill=theme["shadow"])
    draw.rectangle((x(90), cy-s(20)-ow, x(210), cy+s(20)+ow), fill=theme["shadow"])
    # Fill
    draw.rectangle((x(90), cy-s(20), x(210), cy+s(20)), fill=theme["base"])
    draw.rounded_rectangle((x(70), cy-s(28), x(110), cy+s(28)), radius=r_base, fill=theme["base"])
    draw.rounded_rectangle((x(190), cy-s(28), x(230), cy+s(28)), radius=r_base, fill=theme["base"])
    # Highlight
    draw.line((x(70), cy-s(15), x(230), cy-s(15)), fill=theme["highlight"], width=s(3))

    # Bands
    positions = [86, 114, 130, 146, 162, 205] if len(colorList) == 6 else \
                [86, 114, 130, 146, 162] if len(colorList) == 5 else \
                [86, 114, 130, 158]

    for i, color in enumerate(colorList):
        if i < len(positions):
            bx = x(positions[i])
            on_bulb = (positions[i] < 110 or positions[i] > 190)
            by1 = cy - (s(32) if on_bulb else s(24))
            by2 = cy + (s(32) if on_bulb else s(24))
            draw.rectangle((bx, by1+s(1), bx + s(10), by2-s(1)), fill=color)

def draw_resistor_img(colorList, width=900, body_style="beige"):
    height, scale = int(width * 0.33), width / 300
    img = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw_resistor_body(ImageDraw.Draw(img), cx=width/2, cy=height/2, scale=scale, 
                        theme=get_theme(body_style), colorList=colorList, lead_x1=0, lead_x2=width)
    return img

def draw_resistor_label(raw_ohms, colorList, body_style="beige", watt="0.25"):
    # Label size
    w, h = 1600, 300
    img = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    
    val_text, tol_text, bg_color, ppm_text = get_resistor_data(raw_ohms, colorList)
    zone_1, zone_2 = int(w * 0.30), int(w * 0.70)
    
    draw.rectangle((0, 0, zone_1, h), fill=bg_color)
    draw.rectangle((zone_1, 0, zone_2, h), fill="#212121")
    draw.rectangle((zone_2, 0, w, h), fill=bg_color)

    try:
        font_large = ImageFont.truetype(resource_path("font/osifont.ttf"), 120 if len(val_text) <= 5 else 90)
        font_small = ImageFont.truetype(resource_path("font/osifont.ttf"), 60)
    except:
        font_large = font_small = ImageFont.load_default()

    draw.text((zone_1 / 2, (h+20) / 2), val_text, fill="black", font=font_large, anchor="mm")
    
    specs_y = [h/2 - 65, h/2 - 1, h/2 + 65] if len(colorList) == 6 else [h/2 - 60, h/2 + 30]
    draw.text((zone_2 + (w - zone_2)/2, specs_y[0]), watt + "W", fill="black", font=font_small, anchor="mm")
    draw.text((zone_2 + (w - zone_2)/2, specs_y[1]), tol_text, fill="black", font=font_small, anchor="mm")
    if ppm_text and len(specs_y) == 3:
        draw.text((zone_2 + (w - zone_2)/2, specs_y[2]), ppm_text, fill="black", font=font_small, anchor="mm")

    draw_resistor_body(draw, cx=w/2, cy=h/2, scale=3.1, 
                        theme=get_theme(body_style), colorList=colorList, lead_x1=zone_1, lead_x2=zone_2)
    return img