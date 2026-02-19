# Copyright (C) 2026 SUNREYS
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
import image_gen
import resistor_data

root = tk.Tk()
root.geometry("1000x1000")

band_configs = [
    ("1st Band:", resistor_data.color_label_format, resistor_data.resist_multi_col_dict),
    ("2nd Band:", resistor_data.color_label_format, resistor_data.resist_multi_col_dict),
    ("3rd Band:", resistor_data.color_label_format, resistor_data.resist_multi_col_dict),
    ("Multiplier:", resistor_data.multiplier_label, resistor_data.resist_multi_col_dict),
    ("Tolerance:", resistor_data.tolerance_label, resistor_data.tol_col_dict),
    ("PPM:", resistor_data.ppm_label, resistor_data.ppm_col_dict)
]

def create_band(parent, label_text, default_text, options, color_dict):
    frame = tk.Frame(parent)
    tk.Label(frame, text=label_text, font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=5)
    var = tk.StringVar(parent); var.set(default_text)
    menu = tk.OptionMenu(frame, var, *options); menu.pack(side=tk.LEFT)
    
    for i, bg in enumerate(color_dict[:len(options)]):
        fg = "white" if bg in ["black", "brown", "blue", "red"] else "black"
        menu["menu"].entryconfigure(i, label=options[i], background=bg, foreground=fg)
    return var, frame, menu

resistor_canvas = tk.Label(root); resistor_canvas.pack(pady=20)

created_bands = [create_band(root, title, "Select...", opts, colors) for title, opts, colors in band_configs]

(band1_val, band1_frame, band1_menu), \
(band2_val, band2_frame, band2_menu), \
(band3_val, band3_frame, band3_menu), \
(multiplier_val, multiplier_frame, multiplier_menu), \
(tolerance_val, tolerance_frame, tolerance_menu), \
(ppm_val, ppm_frame, ppm_menu) = created_bands

for f in [band1_frame, band2_frame, multiplier_frame, tolerance_frame]: f.pack(pady=5)

# Setup Config Frames
def make_config_frame(label_text, default_val, options_list):
    frame = tk.Frame(root); frame.pack(pady=10)
    tk.Label(frame, text=label_text, font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=5)
    var = tk.StringVar(root); var.set(default_val)
    tk.OptionMenu(frame, var, *options_list).pack(side=tk.LEFT)
    return var

num_bands_val = make_config_frame("Number of Bands:", "4", resistor_data.num_bands_list)
body_col_val = make_config_frame("Body Color:", "Carbon Film (Beige)", resistor_data.body_col_list)
watt_val = make_config_frame("Watt:", "0.25", resistor_data.watt_list)

resistance_frame = tk.Frame(root); resistance_frame.pack(pady=5)
tk.Label(resistance_frame, text="Resistance Value:", font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=5)
resistance_val = ttk.Entry(resistance_frame, font=("Arial", 10)); resistance_val.pack(side=tk.LEFT)

# Update Resistor Image
def update_canvas_image(canvas, pil_image, size):
    img = pil_image.copy()
    img.thumbnail(size, resample=Image.LANCZOS)
    tk_img = ImageTk.PhotoImage(img)
    canvas.config(image=tk_img)
    canvas.image = tk_img

def update_calc(*args):
    global raw_ohms, active_colors
    raw_ohms = 0
    def get_idx(var):
        try: return int(var.get().split(":")[0]) if ":" in var.get() else None
        except: return None
        
    d1, d2, d3 = get_idx(band1_val), get_idx(band2_val), get_idx(band3_val)
    m_idx, t_idx, p_idx = get_idx(multiplier_val), get_idx(tolerance_val), get_idx(ppm_val)
    num_bands = num_bands_val.get()
    
    # Calculate Ohms
    res_digits = f"{d1}{d2}" if (d1 is not None and d2 is not None) else ""
    if res_digits and num_bands in ["5", "6"] and d3 is not None: res_digits += str(d3)
    
    if res_digits and m_idx is not None:
        power = m_idx
        res_int = int(res_digits)
        raw_ohms = res_int * 0.1 if power == 10 else res_int * 0.01 if power == 11 else res_int * (10 ** power)
            
        display_ohms = image_gen.prefix_conversion(raw_ohms)
        tol_text = f" ±{resistor_data.tolerance_label[t_idx].split('±')[1].strip()}" if t_idx is not None else ""
        ppm_text = f" {resistor_data.ppm_label[p_idx].split(':')[1].strip()}" if (num_bands == "6" and p_idx is not None) else ""
        resistance_val.delete(0, tk.END)
        resistance_val.insert(0, f"{display_ohms} Ω {tol_text} {ppm_text}")
    else:
        resistance_val.delete(0, tk.END)

    # Apply Menu Colors
    menus_to_update = [
        (d1, band1_menu, resistor_data.resist_multi_col_dict),
        (d2, band2_menu, resistor_data.resist_multi_col_dict),
        (m_idx, multiplier_menu, resistor_data.resist_multi_col_dict),
        (t_idx, tolerance_menu, resistor_data.tol_col_dict)
    ]
    if num_bands in ["5", "6"]: menus_to_update.append((d3, band3_menu, resistor_data.resist_multi_col_dict))
    if num_bands == "6": menus_to_update.append((p_idx, ppm_menu, resistor_data.ppm_col_dict))

    for val, menu, color_dict in menus_to_update:
        if val is not None:
            bg = color_dict[val]
            fg = "white" if bg.lower() in {"black", "brown", "blue", "violet", "red"} else "black"
            menu.config(bg=bg, fg=fg, activebackground=bg, activeforeground=fg)

    def get_c(val, c_dict):
        if val is not None:
            return c_dict[val]
        else:
            c = image_gen.get_theme(body_col_val.get())
            return c["base"]
    
    active_colors = [get_c(d1, resistor_data.resist_multi_col_dict), get_c(d2, resistor_data.resist_multi_col_dict)]
    if num_bands in ["5", "6"]: 
        active_colors.append(get_c(d3, resistor_data.resist_multi_col_dict))
    active_colors.append(get_c(m_idx, resistor_data.resist_multi_col_dict))
    active_colors.append(get_c(t_idx, resistor_data.tol_col_dict))
    if num_bands == "6": 
        active_colors.append(get_c(p_idx, resistor_data.ppm_col_dict))

    # Render Images
    root.update_idletasks()
    req_size = (max(300, int(root.winfo_width() * 0.8)), 300)

    update_canvas_image(resistor_canvas, image_gen.draw_resistor_img(active_colors, body_style=body_col_val.get()), req_size)
    update_canvas_image(resistor_canvas_label, image_gen.draw_resistor_label(raw_ohms, active_colors, body_style=body_col_val.get(), watt=watt_val.get()), req_size)
def toggle_bands(*args):
    val = num_bands_val.get()
    band3_frame.pack(after=band2_frame, pady=5) if val in ["5", "6"] else band3_frame.pack_forget()
    ppm_frame.pack(after=band3_frame, pady=5) if val == "6" else ppm_frame.pack_forget()
    update_calc()

num_bands_val.trace_add("write", toggle_bands)

for var in [band1_val, band2_val, band3_val, multiplier_val, tolerance_val, ppm_val, body_col_val, watt_val]:
    var.trace_add("write", update_calc)

def save_label_image():
    img = image_gen.draw_resistor_label(raw_ohms, active_colors, body_style=body_col_val.get(), watt=watt_val.get())
    if file_path := filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG image", "*.png")], title="Save resistor label"):
        img.save(file_path, dpi=(300, 300))

tk.Button(root, text='Save Label', command=save_label_image).pack(pady=10)
resistor_canvas_label = tk.Label(root); resistor_canvas_label.pack(pady=20)

root.bind("<Configure>", lambda e: update_calc())
update_calc()
root.mainloop()