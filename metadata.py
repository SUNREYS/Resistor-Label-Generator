# front.py or calc.py

RESISTOR_METADATA = {
    # Digit colors (for bands 1–3)
    "bands": {
        "Black": 0, "Brown": 1, "Red": 2, "Orange": 3, "Yellow": 4,
        "Green": 5, "Blue": 6, "Violet": 7, "Grey": 8, "White": 9
    },

    # Multipliers (band 3 or 4 depending on 4/5/6 band resistor)
    "multipliers": {
        "Black": 1,
        "Brown": 10,
        "Red": 100,
        "Orange": 1_000,
        "Yellow": 10_000,
        "Green": 100_000,
        "Blue": 1_000_000,
        "Violet": 10_000_000,
        "Grey": 100_000_000,
        "White": 1_000_000_000,
        "Gold": 0.1,
        "Silver": 0.01
    },

    # Tolerance bands
    "tolerances": {
        "Brown": "1%",
        "Red": "2%",
        "Green": "0.5%",
        "Blue": "0.25%",
        "Violet": "0.1%",
        "Grey": "0.05%",
        "Gold": "5%",
        "Silver": "10%"
    },

    # PPM (for 6-band resistors)
    "ppms": {
        "Black": "250ppm",
        "Brown": "100ppm",
        "Red": "50ppm",
        "Orange": "15ppm",
        "Yellow": "25ppm",
        "Blue": "10ppm",
        "Violet": "5ppm",
        "Grey": "1ppm"
    },

    # Optional: hex colors for UI / OptionMenu coloring
    "colors": {
        "Black": "#000000",
        "Brown": "#8B4513",
        "Red": "#FF0000",
        "Orange": "#FFA500",
        "Yellow": "#FFFF00",
        "Green": "#008000",
        "Blue": "#0000FF",
        "Violet": "#8A2BE2",
        "Grey": "#808080",
        "White": "#FFFFFF",
        "Gold": "#FFD700",
        "Silver": "#C0C0C0"
    }
}
