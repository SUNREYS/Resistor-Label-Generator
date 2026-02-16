from PIL import Image, ImageDraw

# Reminder: change so we can change to blue or beige bod

def draw_resistor_img(colorList):
    width, height = 300, 100
    img = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # Draw the Leads (Gray wires)
    draw.line((0, 52, width, 52), fill="#A0A0A0", width=4) # Shadow
    draw.line((0, 50, width, 50), fill="#C0C0C0", width=4) # Main wire
    # Reminder: Add blue bod option
    # Resistor Body Colors
    body_base = "#E6D7BD"  # Main beige
    body_shadow = "#D4C3A3" # Darker tan for edges
    body_highlight = "#F5EBDb" # Lighter tan for 3D look

    # Resistor body
    draw.rectangle((90, 30, 210, 70), fill=body_base, outline=body_shadow)

    # Bulbous ends
    draw.rounded_rectangle((70, 22, 110, 78), radius=12, fill=body_base, outline=body_shadow)
    draw.rounded_rectangle((190, 22, 230, 78), radius=12, fill=body_base, outline=body_shadow)

    # 3D effect
    draw.line((75, 35, 225, 35), fill=body_highlight, width=3)

    # Draw the bands
    if len(colorList) > 0:
        x_positions = []
        num_bands = len(colorList)
        
        if num_bands >= 0:
            x_positions.append(86)  # Band 1
            x_positions.append(114) # Band 2
            if num_bands == 4:
                x_positions.append(130) # Multiplier
                x_positions.append(158) # Tolerance
            elif num_bands == 5:
                x_positions.append(130) # Band 3
                x_positions.append(146) # Multiplier
                x_positions.append(162) # Tolerance
            elif num_bands == 6:
                x_positions = [86, 114, 130, 146, 162, 205]

        for i, color in enumerate(colorList):
            if i < len(x_positions):
                x = x_positions[i]
                # Drawing the bands with a slight curve
                draw.rectangle((x, 22 if (x < 110 or x > 190) else 30, 
                                x + 8, 
                                78 if (x < 110 or x > 190) else 70), 
                               fill=color)

    return img

def draw_resistor_label(colorList):
    width, height = 400, 80
    img = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # Resistor Body Colors use blue too
    body_base = "#E6D7BD"  # Main beige
    body_shadow = "#D4C3A3" # Darker tan for edges
    body_highlight = "#F5EBDb" # Lighter tan for 3D look
     # Draw the Leads
    draw.line((0, 42, width, 42), fill="#A0A0A0", width=4) # Shadow
    draw.line((0, 40, width, 40), fill="#C0C0C0", width=4) # Main wire

    # Resistor body shape
    # Thinner middle section + 50
    draw.rectangle((140, 20, 260, 60), fill=body_base, outline=body_shadow)#
    # Bulbous ends
    draw.rounded_rectangle((120, 12, 160, 68), radius=12, fill=body_base, outline=body_shadow)#
    draw.rounded_rectangle((240, 12, 280, 68), radius=12, fill=body_base, outline=body_shadow)#

    # Highlight for 3D effect
    draw.line((125, 25, 275, 25), fill=body_highlight, width=3)
    # Reminder: Customize the color for later.
    draw.rectangle((0, 0, 100, height), fill="green")

    # Draw the bands
    if len(colorList) > 0:
        x_positions = []
        num_bands = len(colorList)
        
        if num_bands >= 0:
            x_positions.append(136)
            x_positions.append(164)
            if num_bands == 4:
                x_positions.append(180)
                x_positions.append(208)
            elif num_bands == 5:
                x_positions.append(180)
                x_positions.append(196)
                x_positions.append(212)
            elif num_bands == 6:
                x_positions = [136, 164, 180, 196, 212, 255]

        for i, color in enumerate(colorList):
            if i < len(x_positions):
                x = x_positions[i]
                # Drawing the bands with a slight curve
                draw.rectangle((x, 12 if (x < 160 or x > 212) else 20, 
                                x + 8, 
                                68 if (x < 160 or x > 212) else 60), 
                               fill=color)
    return img