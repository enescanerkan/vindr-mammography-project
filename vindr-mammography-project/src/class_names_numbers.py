import os
from collections import Counter

# Etiketlerin encode edilmiş isimleri
label_names = {
    0: "Architectural Distortion",
    1: "Asymmetry",
    2: "Focal Asymmetry",
    3: "Global Asymmetry",
    4: "Mass",
    5: "Nipple Retraction",
    6: "No Finding",
    7: "Skin Retraction",
    8: "Skin Thickening",
    9: "Suspicious Calcification",
    10: "Suspicious Lymph Node",
}


# Verilen dizindeki TXT dosyalarını okuyup etiket sayısı çıkaran fonksiyon
def count_labels_in_directory(directory):
    label_counts = Counter()

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        # TXT dosyasını oku
        if filename.endswith(".txt"):
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    # Sınıf numarası satırın ilk elemanıdır
                    parts = line.strip().split()  # Satırı parçala
                    if parts:  # Boş satır kontrolü
                        label_id = int(parts[0])  # İlk elemanı sınıf numarası olarak al
                        if label_id in label_names:
                            label_counts[label_id] += 1

    # İsimlere göre sonuçları düzenle
    return {label_names[label]: count for label, count in label_counts.items()}


# Eğitim ve doğrulama yolları
train_dir = r"C:\Users\Monster\Desktop\vindr_data\train\labels"
val_dir = r"C:\Users\Monster\Desktop\vindr_data\val\labels"

# Eğitim ve doğrulama verilerindeki etiket sayıları
train_label_counts = count_labels_in_directory(train_dir)
val_label_counts = count_labels_in_directory(val_dir)

# Sonuçları yazdır
print("Eğitim Verileri:")
for label, count in train_label_counts.items():
    print(f"{label}: {count}")

print("\nDoğrulama Verileri:")
for label, count in val_label_counts.items():
    print(f"{label}: {count}")
