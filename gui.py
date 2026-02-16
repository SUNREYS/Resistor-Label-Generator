import tkinter as tk
from tkinter import * 
from tkinter import ttk
from tkinter.filedialog import asksaveasfile
#import front
import calc

root = tk.Tk()
root.geometry("500x500")

num_bands = [4, 5, 6]
resistance_color = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
multiplier_color = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

color_label_format = ["0: Black", "1: Brown", "2: Red", "3: Orange", "4: Yellow", "5: Green", "6: Blue", "7: Violet", "8: Grey", "9: White"]
multiplier_label = ["0: Black ×1 Ω", "1: Brown ×10 Ω", "2: Red ×100 Ω", "3: Orange ×1 kΩ", "4: Yellow ×10 kΩ", "5: Green ×100 kΩ", "6: Blue ×1 MΩ", "7: Violet ×10 MΩ", "8: Grey ×100 MΩ", "9: White ×1 GΩ", "10: Gold ×0.1 Ω", "11: Silver ×0.01 Ω"]
tolerance_label = ["0: Brown ± 1%", "1: Red ± 2%", "2: Green ± 0.5%", "3: Blue ± 0.25%", "4: Violet ± 0.1%", "5: Grey ± 0.05%", "6: Gold ± 5%", "7: Silver ± 10%"]

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

# Digit Bands
band1_val, band1_frame, band1_menu = create_band(root, "Band 1:", "Select color band 1", color_label_format, calc.resist_multi_col_dict)
band2_val, band2_frame, band2_menu = create_band(root, "Band 2:", "Select color band 2", color_label_format, calc.resist_multi_col_dict)
band3_val, band3_frame, band3_menu = create_band(root, "Band 3:", "Select color band 3", color_label_format, calc.resist_multi_col_dict)
band4_val, band4_frame, band4_menu = create_band(root, "Band 4:", "Select color band 4", color_label_format, calc.resist_multi_col_dict)

# Multiplier and Tolerance
multiplier_val, multiplier_frame, multiplier_menu = create_band(root, "Multiplier:", "Select multiplier", multiplier_label, calc.resist_multi_col_dict)
tolerance_val, tolerance_frame, tolerance_menu = create_band(root, "Tolerance:", "Select tolerance", tolerance_label, calc.tol_col_dict)

# Pack the ones that are always visible
band1_frame.pack(pady=5)
band2_frame.pack(pady=5)
multiplier_frame.pack(pady=5)
tolerance_frame.pack(pady=5)

# Band 3 and 4 start hidden (not packed) and will be handled by toggle_bands()

def update_calc(*args):
    def get_digit(var):
        s = var.get()
        return s.split(":")[0] if ":" in s else ""
    
    d1 = get_digit(band1_val)
    d2 = get_digit(band2_val)
    m1 = get_digit(multiplier_val)
    t1 = get_digit(tolerance_val)
    menu_color = [(d1, band1_menu), (d2, band2_menu)]
    tol_text = f" \u00B1{t1.split(':')[0]}" if ":" in t1 else ""
    res = ""

    if num_bands_val.get() == "5" or "6":
        d3 = get_digit(band3_val)
        menu_color.append((d3, band3_menu))
        res = d1 + d2 + d3
        if num_bands_val.get() == "6":
            d4 = get_digit(band4_val)
            menu_color.append((d4, band4_menu))
            res += d4
    else:
        res = d1 + d2
    if m1 != "":
        menu_color.append((m1, multiplier_menu))
    if t1 != "":
        menu_color.append((t1, tolerance_menu))

    if res != "":
        if m1 != "":
            power = int(m1)
            res_int = int(res)
            if power == 10: # Gold
                raw_ohms = res_int * 0.1
            elif power == 11: # Silver
                raw_ohms = res_int * 0.01
            else:
                raw_ohms = res_int * (10 ** power)
            display_val = calc.prefix_conversion(raw_ohms)
        else:
            display_val = res
        resistance_val.delete(0, tk.END)
        resistance_val.insert(0, f"{display_val} \u2126{tol_text}")

    for val, menu in menu_color:
        if val != "": # Only color if a digit actually exists
            try:
                idx = int(val)
                if idx == -1: idx = 10
                if idx == -2: idx = 11
                if menu == tolerance_menu:
                    bg = calc.tol_col_dict[idx]
                else:
                    bg = calc.resist_multi_col_dict[idx]
                fg = "white" if bg in ["black", "brown", "blue"] else "black"
                menu.config(bg=bg, fg=fg, activebackground=bg)
            except (ValueError, IndexError):
                pass
#Know atleast 4 bands.
def toggle_bands(*args):
    val = num_bands_val.get()

    if val == "5" or "6":
        band3_frame.pack(after=band2_frame, pady=5)
        if val == "6":
            band4_frame.pack(after=band3_frame, pady=5)
    else:
        band3_frame.pack_forget()
        band4_frame.pack_forget()

    update_calc()

# Number of Bands
num_bands_frame = tk.Frame(root)
num_bands_frame.pack(pady=10)
tk.Label(num_bands_frame, text="Number of Bands:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)

num_bands_val = tk.StringVar(root)
# Default number of bands
num_bands_val.set("4")
num_bands_val.trace_add("write", toggle_bands)

num_bands_menu = tk.OptionMenu(num_bands_frame, num_bands_val, *num_bands)
num_bands_menu.pack(side=tk.LEFT)


band1_val.trace_add("write", update_calc)
band2_val.trace_add("write", update_calc)
band3_val.trace_add("write", update_calc)
band4_val.trace_add("write", update_calc)
multiplier_val.trace_add("write", update_calc)
tolerance_val.trace_add("write", update_calc)


def print_answers():
    print("Selected opt: {}".format(band1_val.get()))


submit_button = tk.Button(root, text='Submit', command=print_answers)
submit_button.pack()

root.mainloop()
