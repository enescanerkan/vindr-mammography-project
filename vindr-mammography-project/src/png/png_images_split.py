import os
import shutil
import pandas as pd

# CSV dosyasının yolu
csv_file_path = r"C:\Users\Monster\Desktop\Tubitak İTÜ\src\finding_annotations.csv"

# Görüntülerin ana klasörünün yolu
images_directory = r"C:\Users\Monster\Desktop\mammo_dataset_output_PNG\vindr-mammo-a-large-scale-benchmark-dataset-for-computer-aided-detection-and-diagnosis-in-full-field-digital-mammography-1.0.0\images"

# Hedef klasörlerin ana yolu
target_base_directory = r"C:\Users\Monster\Desktop\organized_images_png"

# CSV dosyasını oku
data = pd.read_csv(csv_file_path)

# Training ve test klasörlerini oluştur
for split in ['training', 'test']:
    split_directory = os.path.join(target_base_directory, split)
    if not os.path.exists(split_directory):
        os.makedirs(split_directory)

# Görüntüleri taşı
for _, row in data.iterrows():
    folder_name = row['study_id']  # images ana klasöründeki alt klasör adı
    image_name = row['image_id']  # Alt klasör içindeki görüntü adı
    split = row['split']          # Training ya da test

    # Kaynak dosya yolu
    source_path = os.path.join(images_directory, folder_name, image_name + ".png")

    # Hedef dosya yolu
    target_path = os.path.join(target_base_directory, split, image_name + ".png")

    # Görüntü varsa taşı
    if os.path.exists(source_path):
        shutil.copy(source_path, target_path)
    else:
        print(f"Image not found: {source_path}")