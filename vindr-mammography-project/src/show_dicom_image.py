import pydicom
import matplotlib.pyplot as plt
import numpy as np

# DICOM dosyasının yolu
dicom_file_path = r"C:\Users\Monster\Desktop\2ce50597d3a7711d30b9ec3a0aa25623.dicom"  # DICOM dosyasının tam yolu

# DICOM dosyasını okuyun
ds = pydicom.dcmread(dicom_file_path)

# DICOM'daki piksel verilerini al
pixel_array = ds.pixel_array

print(pixel_array.shape)

# Görüntüyü göster
plt.imshow(pixel_array, cmap="gray")
plt.title("DICOM Görüntüsü")
plt.axis("off")  # Ekseni kapat
plt.show()
