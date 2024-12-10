import cv2
import os
import numpy as np
from collections import defaultdict

# Veri dizinleri: Eğitim ve doğrulama setlerinin görüntü ve etiket dosyalarının konumları
train_image_dir = r"C:\Users\Monster\Desktop\dataset\images\train"
train_label_dir = r"C:\Users\Monster\Desktop\dataset\labels\train"
val_image_dir = r"C:\Users\Monster\Desktop\dataset\images\val"
val_label_dir = r"C:\Users\Monster\Desktop\dataset\labels\val"

# Çoğaltma yapılmayacak sınıflar ve özel çoğaltma yapılacak sınıf tanımları
exclude_classes = [4]  # Mass sınıfı için çoğaltma yapılmayacak
duplicate_class = 9  # Suspicious Calcification sınıfı için özel olarak bir kez çoğaltma yapılacak
class_counts = defaultdict(int)  # Her sınıf için veri sayısını izlemek

# Görüntü ve etiket dosyalarını eşleştiren yardımcı bir fonksiyon
def get_files(image_dir, label_dir):
    """
    Verilen görüntü ve etiket dizinlerindeki dosyaları eşleştirir.
    """
    image_files = sorted([os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith('.png')])
    label_files = sorted([os.path.join(label_dir, f) for f in os.listdir(label_dir) if f.endswith('.txt')])
    return list(zip(image_files, label_files))

# Eğitim ve doğrulama veri setlerini yükle
train_files = get_files(train_image_dir, train_label_dir)
val_files = get_files(val_image_dir, val_label_dir)

# Görüntü ve etiketler üzerinde veri artırımı uygulayan fonksiyon
def augment_image_and_labels(image_path, label_path, output_image_dir, output_label_dir, special_class_id=None):
    """
    Bir görüntü ve etiket seti üzerinde veri artırımı işlemleri uygular.
    Flip (yansıtma) dönüşümleri ile yeni veri oluşturur.
    """
    image = cv2.imread(image_path)
    if image is None:
        return []  # Görüntü yüklenemezse boş dön

    height, width, _ = image.shape
    with open(label_path, "r") as f:
        labels = f.readlines()

    augmented_files = []

    # Yatay, dikey ve her iki yönde yansıma işlemleri
    for flip_name, flip_code in {"horizontal": 1, "vertical": 0, "both": -1}.items():
        flipped_image = cv2.flip(image, flip_code)  # Görüntüyü yansıt
        augmented_labels = []
        for label in labels:
            class_id, x_center, y_center, box_width, box_height = label.strip().split()
            class_id = int(class_id)

            # Özel sınıf için sadece bu sınıf üzerinde işlem yap
            if special_class_id is not None and class_id != special_class_id:
                continue

            # Hariç tutulan sınıflar üzerinde işlem yapma
            if class_id in exclude_classes and special_class_id is None:
                continue

            x_center = float(x_center)
            y_center = float(y_center)
            box_width = float(box_width)
            box_height = float(box_height)

            # Yansıma işlemleri için koordinat dönüşümleri
            if flip_name == "horizontal":
                x_center = 1 - x_center
            elif flip_name == "vertical":
                y_center = 1 - y_center
            elif flip_name == "both":
                x_center = 1 - x_center
                y_center = 1 - y_center

            # Yeni etiketleri oluştur
            augmented_labels.append(f"{class_id} {x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}\n")

        if augmented_labels:  # Eğer dönüşüm sonrası geçerli etiketler varsa, dosyayı kaydet
            base_name = os.path.basename(image_path).replace(".png", f"_aug_flip_{flip_name}.png")
            label_name = os.path.basename(label_path).replace(".txt", f"_aug_flip_{flip_name}.txt")
            augmented_image_path = os.path.join(output_image_dir, base_name)
            augmented_label_path = os.path.join(output_label_dir, label_name)
            cv2.imwrite(augmented_image_path, flipped_image)
            with open(augmented_label_path, "w") as f:
                f.writelines(augmented_labels)
            augmented_files.append((augmented_image_path, augmented_label_path))

    return augmented_files

# Veri seti üzerinde veri artırımı işlemi
def process_dataset(files, output_image_dir, output_label_dir):
    """
    Belirtilen dosyalar üzerinde veri artırımı işlemini uygular.
    """
    os.makedirs(output_image_dir, exist_ok=True)
    os.makedirs(output_label_dir, exist_ok=True)

    for image_path, label_path in files:
        with open(label_path, "r") as f:
            labels = f.readlines()
        for label in labels:
            class_id = int(label.split()[0])
            class_counts[class_id] += 1  # Her sınıf için veri sayısını artır

        # Suspicious Calcification sınıfı için özel veri artırımı
        augment_image_and_labels(image_path, label_path, output_image_dir, output_label_dir,
                                 special_class_id=duplicate_class)

        # Diğer sınıflar için genel veri artırımı
        augment_image_and_labels(image_path, label_path, output_image_dir, output_label_dir)

# Veri artırımı için çıkış dizinleri
augmented_train_image_dir = r"C:\Users\Monster\Desktop\augmented_dataset\images\train"
augmented_train_label_dir = r"C:\Users\Monster\Desktop\augmented_dataset\labels\train"
augmented_val_image_dir = r"C:\Users\Monster\Desktop\augmented_dataset\images\val"
augmented_val_label_dir = r"C:\Users\Monster\Desktop\augmented_dataset\labels\val"

# Eğitim ve doğrulama setlerine veri artırımı işlemini uygula
process_dataset(train_files, augmented_train_image_dir, augmented_train_label_dir)
process_dataset(val_files, augmented_val_image_dir, augmented_val_label_dir)

# Sınıf dağılımını yazdır
print("Veri dağılımı:")
for class_id, count in sorted(class_counts.items()):
    print(f"Sınıf {class_id}: {count} veri")
