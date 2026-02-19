# Base Color Values for drawing
resist_multi_col_dict = ["black", "brown", "red", "orange", "yellow", "green", "blue", "violet", "grey", "white", "gold", "silver"]
tol_col_dict = ["brown", "red", "green", "blue", "violet", "grey", "gold", "silver"]
ppm_col_dict = ["brown", "red", "orange", "yellow", "blue", "violet", "grey"]

# Value Lookups for text generation
TOLS =  { "Brown": "1%", "Red": "2%", "Green": "0.5%", "Blue": "0.25%", "Violet": "0.1%", "Grey": "0.05%", "Gold": "5%", "Silver": "10%" }
PPMS =  { "Black": "250ppm", "Brown": "100ppm", "Red": "50ppm", "Orange": "15ppm", "Yellow": "25ppm", "Blue": "10ppm", "Violet": "5ppm", "Grey": "1ppm" }

# GUI Configuration Lists
num_bands_list = [4, 5, 6]
body_col_list = ["Carbon Film (Beige)", "Metal Film (Blue)"]
watt_list = ["0.03125", "0.05", "0.0625", "0.1", "0.125", "0.25", "0.5", "1.0", "2.0", "3.0", "5.0", "10.0", "20.0", "25.0", "50.0", "100.0"]

color_label_format = ["0: Black", "1: Brown", "2: Red", "3: Orange", "4: Yellow", "5: Green", "6: Blue", "7: Violet", "8: Grey", "9: White"]
multiplier_label = ["0: Black ×1 Ω", "1: Brown ×10 Ω", "2: Red ×100 Ω", "3: Orange ×1 kΩ", "4: Yellow ×10 kΩ", "5: Green ×100 kΩ", "6: Blue ×1 MΩ", "7: Violet ×10 MΩ", "8: Grey ×100 MΩ", "9: White ×1 GΩ", "10: Gold ×0.1 Ω", "11: Silver ×0.01 Ω"]
tolerance_label = ["0: Brown ± 1%", "1: Red ± 2%", "2: Green ± 0.5%", "3: Blue ± 0.25%", "4: Violet ± 0.1%", "5: Grey ± 0.05%", "6: Gold ± 5%", "7: Silver ± 10%"]
ppm_label = ["0: 100ppm", "1: 50ppm", "2: 15ppm", "3: 25ppm", "4: 0.5ppm", "5: 0.25ppm", "6: 0.1ppm"]