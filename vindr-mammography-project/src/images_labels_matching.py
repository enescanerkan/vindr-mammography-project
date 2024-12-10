import os
import shutil

# Klasör yolları
label_dirs = {
    "test": r"C:\Users\Monster\Desktop\organized_labels\test",
    "training": r"C:\Users\Monster\Desktop\organized_labels\training"
}

image_dirs = {
    "test": r"C:\Users\Monster\Desktop\organized_images_png\test",
    "training": r"C:\Users\Monster\Desktop\organized_images_png\training"
}

# Hedef klasörler (organize edilmiş dosyalar buraya kopyalanacak)
output_dirs = {
    "test": r"C:\Users\Monster\Desktop\images\test",
    "training": r"C:\Users\Monster\Desktop\images\training"
}

# İşlem
for category in label_dirs:
    label_path = label_dirs[category]
    image_path = image_dirs[category]
    output_path = output_dirs[category]

    # Klasörler varsa işlem yap
    if os.path.exists(label_path) and os.path.exists(image_path):
        # Etiket dosyalarını al
        label_files = {os.path.splitext(f)[0] for f in os.listdir(label_path) if f.endswith('.txt')}

        # Görüntü dosyalarını kontrol et
        for image_file in os.listdir(image_path):
            image_name, image_ext = os.path.splitext(image_file)
            if image_ext.lower() == ".png" and image_name in label_files:
                # Dosya eşleşirse hedef klasöre taşı veya kopyala
                src_image = os.path.join(image_path, image_file)
                dst_image = os.path.join(output_path, image_file)

                # Kopyalama işlemi
                shutil.copy(src_image, dst_image)
                print(f"Kopyalandı: {src_image} -> {dst_image}")
    else:
        print(f"{category} klasörlerinden biri eksik, işlem atlandı.")
