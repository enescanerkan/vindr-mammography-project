import os
import pandas as pd

# CSV dosyasının yolu
csv_file_path = r"C:\Users\Monster\Desktop\mammo_dataset_output_PNG\vindr-mammo-a-large-scale-benchmark-dataset-for-computer-aided-detection-and-diagnosis-in-full-field-digital-mammography-1.0.0\finding_annotations.csv"

# Hedef klasörlerin ana yolu
target_base_directory = r"C:\Users\Monster\Desktop\organized_labels"

# CSV dosyasını yükle
data = pd.read_csv(csv_file_path)

# Eksik bounding box verilerini filtrele
data = data.dropna(subset=['xmin', 'ymin', 'xmax', 'ymax'])
"""
yolo ile eğitim yapacağımızdan yolo format şekli:

class_id x_center y_center width height

"""
# 'finding_categories' sütununu listeye çevir
data['finding_categories'] = data['finding_categories'].apply(eval)

# Kategori encode
category_to_id = {
    "Architectural Distortion": 0,
    "Asymmetry": 1,
    "Focal Asymmetry": 2,
    "Global Asymmetry": 3,
    "Mass": 4,
    "Nipple Retraction": 5,
    "No Finding": 6,
    "Skin Retraction": 7,
    "Skin Thickening": 8,
    "Suspicious Calcification": 9,
    "Suspicious Lymph Node": 10
}

# Hedef klasörleri oluştur
splits = data['split'].unique()
for split in splits:
    split_dir = os.path.join(target_base_directory, split)
    os.makedirs(split_dir, exist_ok=True)

# Etiket dosyalarını oluştur
def generate_yolo_labels(group):
    """
    Belirli bir image_id için YOLO formatında etiketleri döndürür.
    """
    image_height = group['height'].iloc[0]
    image_width = group['width'].iloc[0]
    labels = []

    for _, row in group.iterrows():
        for category in row['finding_categories']:
            if category in category_to_id:
                class_id = category_to_id[category]

                xmin, ymin, xmax, ymax = row['xmin'], row['ymin'], row['xmax'], row['ymax']

                # YOLO formatına dönüştürme
                x_center = ((xmin + xmax) / 2) / image_width
                y_center = ((ymin + ymax) / 2) / image_height
                bbox_width = (xmax - xmin) / image_width
                bbox_height = (ymax - ymin) / image_height

                # YOLO formatı: class_id x_center y_center width height , yukarda da yazdığım gibi
                labels.append(f"{class_id} {x_center:.6f} {y_center:.6f} {bbox_width:.6f} {bbox_height:.6f}")

    return labels

# Grupları işlemeye başla
grouped_data = data.groupby('image_id')
for image_id, group in grouped_data:
    split = group['split'].iloc[0]  # Split değerini al
    yolo_labels = generate_yolo_labels(group)

    if yolo_labels:  # Sadece etiket varsa dosya oluştur
        split_dir = os.path.join(target_base_directory, split)
        label_path = os.path.join(split_dir, f"{image_id}.txt")
        with open(label_path, 'w') as f:
            f.write("\n".join(yolo_labels))

# Kategori eşlemesini kaydet
category_mapping_path = os.path.join(target_base_directory, "category_mapping.txt")
with open(category_mapping_path, 'w') as f:
    for category, idx in category_to_id.items():
        f.write(f"{idx}: {category}\n")

print("Etiketleme ve dosya organizasyonu tamamlandı!")
