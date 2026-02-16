def prefix_conversion(val):
    if val >= 1000000000:
        return f"{val/1000000000:g}G"
    if val >= 1000000:
        return f"{val/1000000:g}M"
    elif val >= 1000:
        return f"{val/1000:g}K"
    else:
        return f"{val:g}"

resist_multi_col_dict = ["black", "brown", "red", "orange", "yellow", "green", "blue", "violet", "grey", "white", "gold", "silver"]
tol_col_dict = ["brown", "red", "green", "blue", "violet", "grey", "gold", "silver"]

