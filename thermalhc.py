import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def interpolation(value, color_stops):
    for i in range(1, len(color_stops)):
        if value <= color_stops[i][0]:
            x1, c1 = color_stops[i-1]
            x2, c2 = color_stops[i]
            t = (value - x1) / (x2 - x1)
            return (1 - t) * np.array(c1) + t * np.array(c2)

    return color_stops[-1][1]

def flirtorgb(image_path, output_path):
    thermal_image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)


    # faktor skala konversi kelvin, offset ke celcius
    scale_factor = 0.04 
    offset = -273.15 
    temperature_data = thermal_image * scale_factor + offset
    
    # norm min-max
    min_temp = np.min(temperature_data)
    max_temp = np.max(temperature_data)
    normalized_temp = (temperature_data - min_temp) / (max_temp - min_temp)

    # colormap
    color_stops = [
        (0.0, [0, 0, 0]),       # Black
        (0.125, [148, 0, 211]), # Violet
        (0.25, [0, 0, 255]),    # Blue
        (0.375, [0, 255, 255]), # Cyan
        (0.50, [0, 100, 0]),    # Dark Green
        (0.625, [255, 255, 0]), # Yellow
        (0.75, [128, 0, 0]),    # Maroon
        (0.875, [255, 0, 0]),   # Red
        (1.0, [255, 255, 255])  # White
    ]
    rgb_image = np.zeros((thermal_image.shape[0], thermal_image.shape[1], 3), dtype=np.uint8)
    
    for i in range(thermal_image.shape[0]):
        for j in range(thermal_image.shape[1]):
            value = normalized_temp[i, j]
            color = interpolation(value, color_stops)
            rgb_image[i, j] = np.clip(color, 0, 255).astype(np.uint8)

    colors = ['black', 'blue', 'cyan', 'lime', 'yellow', 'red', 'white']
    thermal_colormap = LinearSegmentedColormap.from_list("black_blue_cyan_lime_yellow_red_white", colors)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.imshow(rgb_image)
    ax.axis('off')

    # colorbar
    sm = plt.cm.ScalarMappable(cmap=thermal_colormap, norm=plt.Normalize(vmin=min_temp, vmax=max_temp))
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, orientation='vertical', fraction=0.02, pad=0.04)
    cbar.set_label('Temperature (°C)')

    # save
    plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0.1)
    plt.show()


image_path = 'FLIR_08863.tiff'  # ganti jadi tiff
output_path = '1hc.png'  # output
flirtorgb(image_path, output_path)
