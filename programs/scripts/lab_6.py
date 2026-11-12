#testowe załadowanie gotowego rgb rastra

import matplotlib.pyplot as plt
import numpy as np
import rasterio

path_to_file = "bydgoszcz.tif"

with rasterio.open(path_to_file) as src:
    raster = src.read()

if raster.shape[0] < 3:
    raise ValueError(f"Expected an RGB raster with at least 3 bands, got {raster.shape[0]}.")

rgb = np.moveaxis(raster[:3], 0, -1)
low, high = np.percentile(rgb, [2, 98], axis=(0, 1))
rgb = np.clip((rgb - low) / (high - low), 0, 1)

plt.figure(figsize=(10, 8))
plt.imshow(rgb)
plt.axis("off")
plt.tight_layout()
plt.show()

# Zadanie 1: Wyświetl raster w kolorach możliwie odzwierciedlających rzeczywistość
red_path = "sentinel-2-l2a_2026-10-23_S2A_MSIL2A_20261023T100041_R122_T33UYU_20261023T163256_B04.tif"
green_path = "sentinel-2-l2a_2026-10-23_S2A_MSIL2A_20261023T100041_R122_T33UYU_20261023T163256_B03.tif"
blue_path = "sentinel-2-l2a_2026-10-23_S2A_MSIL2A_20261023T100041_R122_T33UYU_20261023T163256_B02.tif"

with rasterio.open(red_path) as src:
    red = src.read(1).astype(np.float32)
    profile = src.profile
with rasterio.open(green_path) as src:
    green = src.read(1).astype(np.float32)
with rasterio.open(blue_path) as src:
    blue = src.read(1).astype(np.float32)

 
rgb_stacked = np.stack([red, green, blue], axis=-1).astype(float)
rgb_norm = np.zeros_like(rgb_stacked)

for i in range(3):
  low = np.percentile(rgb_stacked[:, :, i], 2)
  high = np.percentile(rgb_stacked[:, :, i], 98)
  rgb_norm[:, :, i] = np.clip(
      (rgb_stacked[:, :, i] - low) / (high - low), 0, 1
  )

plt.figure(figsize=(7, 7))
plt.imshow(rgb_norm)
plt.title("Kompozycja RGB")
plt.axis("off")
plt.show()


# Zadanie 2: Przedstaw i krótko opisz histogram wartości dla każdego kanału

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
channels = [("Czerwony (Red - B04)", red, "red"), 
            ("Zielony (Green - B03)", green, "green"), 
            ("Niebieski (Blue - B02)", blue, "blue")]

for ax, (title, data, color) in zip(axes, channels):
  ax.hist(data.flatten(), bins=50, color=color, alpha=0.7)
  ax.set_title(title)
  ax.set_xlabel("Wartość reflektancji")
  ax.set_ylabel("Częstotliwość")

plt.tight_layout()
plt.show()


# Zadanie 3: Podziel wartości rastra na 9 równych części (3 x 3), a następnie podaj współrzędne w układzie odniesienia rastra środka każdej z tych części
with rasterio.open(red_path) as src:
  transform = src.transform

height, width = red.shape
h_step = height // 3
w_step = width // 3

print("Współrzędne geograficzne/terenowe środków 9 części")
center_coords = []

for row in range(3):
  for col in range(3):
    # Indekse piksela w środku każdego z 9 okien
    px = col * w_step + w_step // 2
    py = row * h_step + h_step // 2

    # Przeliczenie indeksów wiersz/kolumna na współrzędne w układzie rastra za pomocą transformacji
    x_coord, y_coord = rasterio.transform.xy(transform, py, px)
    center_coords.append((x_coord, y_coord))
    print(
        f"Część [{row+1}, {col+1}] -> Indeksy (px: {px}, py: {py}) -> Współrzędne"
        f" terenowe: X = {x_coord:.2f}, Y = {y_coord:.2f}"
    )

# Zadanie 4: Zapisz raster do 1 pliku RGB złożonego z zaciągniętych 3 kanałów

rgb_to_save = np.moveaxis(rgb_norm, -1, 0)

rgb_to_save_uint8 = (rgb_to_save * 255).astype(np.uint8)

# Aktualizacja profilu dla pliku trzykanałowego
profile.update(count=3, dtype="uint8")

output_path = "sentinel_rgb_output.tif"
with rasterio.open(output_path, "w", **profile) as dst:
  dst.write(rgb_to_save_uint8)

print(f"\nZapisano plik RGB do: {output_path}")