import tkinter as tk
from tkinter import * 
from tkinter import ttk
from tkinter.filedialog import asksaveasfile
from PIL import ImageTk
import front
import calc

root = tk.Tk()
root.geometry("700x700")

num_bands_list = [4, 5, 6]
color_label_format = ["0: Black", "1: Brown", "2: Red", "3: Orange", "4: Yellow", "5: Green", "6: Blue", "7: Violet", "8: Grey", "9: White"]
multiplier_label = ["0: Black ×1 Ω", "1: Brown ×10 Ω", "2: Red ×100 Ω", "3: Orange ×1 kΩ", "4: Yellow ×10 kΩ", "5: Green ×100 kΩ", "6: Blue ×1 MΩ", "7: Violet ×10 MΩ", "8: Grey ×100 MΩ", "9: White ×1 GΩ", "10: Gold ×0.1 Ω", "11: Silver ×0.01 Ω"]
tolerance_label = ["0: Brown ± 1%", "1: Red ± 2%", "2: Green ± 0.5%", "3: Blue ± 0.25%", "4: Violet ± 0.1%", "5: Grey ± 0.05%", "6: Gold ± 5%", "7: Silver ± 10%"]
ppm_label = ["0: 100ppm", "1: 50ppm", "2: 15ppm", "3: 25ppm", "4: 0.5ppm", "5: 0.25ppm", "6: 0.1ppm"]

def style_resistor_menu(menu_wid, color_label, color_dict, length):
    menu_w = menu_wid["menu"]

    for i in range(length):
        bg = color_dict[i]
        fg = "white" if bg in ["black", "brown", "blue"] else "black"
        menu_w.entryconfigure(i, label=color_label[i], background=bg, foreground=fg)

def create_band(parent, label_text, default_text, options, color_dict):
    frame = tk.Frame(parent)

    label = tk.Label(frame, text=label_text, font=("Arial", 10, "bold"))
    label.pack(side=tk.LEFT, padx=5)
    
    var = tk.StringVar(parent)
    var.set(default_text)
    
    menu = tk.OptionMenu(frame, var, *options)
    menu.pack(side=tk.LEFT)
    
    style_resistor_menu(menu, options, color_dict, len(options))
    
    # Return the variable, the frame, and menu
    return var, frame, menu

# Resistance Display
resistance_frame = tk.Frame(root)
resistance_frame.pack(pady=5)
tk.Label(resistance_frame, text="Resistance Value:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
resistance_val = ttk.Entry(root)
resistance_val.pack()

# Resistor
resistor_canvas = tk.Label(root)
resistor_canvas.pack(pady=20)

# Digit Bands
band1_val, band1_frame, band1_menu = create_band(root, "Band 1:", "Select color band 1", color_label_format, calc.resist_multi_col_dict)
band2_val, band2_frame, band2_menu = create_band(root, "Band 2:", "Select color band 2", color_label_format, calc.resist_multi_col_dict)
band3_val, band3_frame, band3_menu = create_band(root, "Band 3:", "Select color band 3", color_label_format, calc.resist_multi_col_dict)
ppm_val, ppm_frame, ppm_menu = create_band(root, "PPM:", "Select PPM", ppm_label, calc.ppm_col_dict)

# Multiplier and Tolerance
multiplier_val, multiplier_frame, multiplier_menu = create_band(root, "Multiplier:", "Select multiplier", multiplier_label, calc.resist_multi_col_dict)
tolerance_val, tolerance_frame, tolerance_menu = create_band(root, "Tolerance:", "Select tolerance", tolerance_label, calc.tol_col_dict)

# Pack the ones that are always visible
band1_frame.pack(pady=5)
band2_frame.pack(pady=5)
multiplier_frame.pack(pady=5)
tolerance_frame.pack(pady=5)

def update_calc(*args):
    def get_idx(var):
        s = var.get()
        if ":" in s:
            try:
                return int(s.split(":")[0])
            except ValueError:
                return None
        return None
    active_colors = []
    d1, d2, d3,  = get_idx(band1_val), get_idx(band2_val), get_idx(band3_val)
    m_idx, t_idx, p_idx = get_idx(multiplier_val), get_idx(tolerance_val), get_idx(ppm_val)
    num_bands = num_bands_val.get()
    menu_color = [(d1, band1_menu), (d2, band2_menu), (m_idx, multiplier_menu), (t_idx, tolerance_menu)]
    res_digits, tol_text, ppm_text = "", "", ""
    if num_bands in ["5", "6"]: menu_color.append((d3, band3_menu))
    if num_bands == "6": menu_color.append((p_idx, ppm_menu))
    if d1 is not None and d2 is not None:
            res_digits = str(d1) + str(d2)
            if num_bands in ["5", "6"] and d3 is not None:
                res_digits += str(d3)
            
            if res_digits != "" and m_idx is not None:
                power = m_idx
                res_int = int(res_digits)
                if power == 10: raw_ohms = res_int * 0.1
                elif power == 11: raw_ohms = res_int * 0.01
                else: raw_ohms = res_int * (10 ** power)
                
                display_ohms = calc.prefix_conversion(raw_ohms)
                
                if t_idx is not None:
                    tol_text = f" ±{tolerance_label[t_idx].split('±')[1].strip()}"
                if num_bands == "6" and p_idx is not None:
                    ppm_text = f" {ppm_label[p_idx].split(':')[1].strip()}"
                
                resistance_val.delete(0, tk.END)
                resistance_val.insert(0, f"{display_ohms} Ω {tol_text} {ppm_text}")
            else:
                resistance_val.delete(0, tk.END)
            
    config = [(d1, calc.resist_multi_col_dict), (d2, calc.resist_multi_col_dict)]
    if num_bands in ["5", "6"]:
        config.append((d3, calc.resist_multi_col_dict))
    config.append((m_idx, calc.resist_multi_col_dict))
    config.append((t_idx, calc.tol_col_dict))
    if num_bands == "6":
        config.append((p_idx, calc.ppm_col_dict))

    # Populate active_colors from the config
    active_colors = []
    for val, c_dict in config:
        if val is not None:
            active_colors.append(c_dict[val])
        else:
            active_colors.append("#E6D7BD") # Body beige if not selected

    # Apply menu background colors
    for val, menu in menu_color:
        if val is not None:
            if menu == tolerance_menu: bg = calc.tol_col_dict[int(val)]
            elif menu == ppm_menu: bg = calc.ppm_col_dict[int(val)]
            else: bg = calc.resist_multi_col_dict[int(val)]
            fg = "white" if bg in ["black", "brown", "blue", "violet"] else "black"
            menu.config(bg=bg, fg=fg, activebackground=bg)
                
    # Generate and display image
    pil_img = front.draw_resistor_img(active_colors)
    tk_img = ImageTk.PhotoImage(pil_img)
    resistor_canvas.config(image=tk_img)
    resistor_canvas.image = tk_img
    
    # Generate and display label image
    pil_img2 = front.draw_resistor_label(active_colors)
    tk_img2 = ImageTk.PhotoImage(pil_img2)
    resistor_canvas_label.config(image=tk_img2)
    resistor_canvas_label.image = tk_img2

# Know atleast 4 bands
def toggle_bands(*args):
    val = num_bands_val.get()

    if val in ["5", "6"]:
        band3_frame.pack(after=band2_frame, pady=5)
        if val == "6":
            ppm_frame.pack(after=band3_frame, pady=5)
        else:
            ppm_frame.pack_forget()
    else:
        band3_frame.pack_forget()
        ppm_frame.pack_forget()
    update_calc()

# Number of Bands
num_bands_frame = tk.Frame(root)
num_bands_frame.pack(pady=10)
tk.Label(num_bands_frame, text="Number of Bands:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
num_bands_val = tk.StringVar(root)

# Default number of bands
num_bands_val.set("4")
num_bands_val.trace_add("write", toggle_bands)
num_bands_menu = tk.OptionMenu(num_bands_frame, num_bands_val, *num_bands_list)
num_bands_menu.pack(side=tk.LEFT)

for menu in [band1_val, band2_val, band3_val, multiplier_val, tolerance_val, ppm_val]:
    menu.trace_add("write", update_calc)

def print_answers():
    print("Selected opt: {}".format(band1_val.get()))

submit_button = tk.Button(root, text='Submit', command=print_answers)
submit_button.pack()

# Print label on GUI
resistor_canvas_label = tk.Label(root)
resistor_canvas_label.pack(pady=20)

update_calc()
root.mainloop()
