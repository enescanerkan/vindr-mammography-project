from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt

# Model ve görüntü yollarını tanımla
model_path = r"C:\Users\Monster\Desktop\Tubitak İTÜ\resume2\trained_data_resume2\weights\best.pt"
image_path = r"C:\Users\Monster\Desktop\4afca14421444ba0184608751cb4b3ef.png"
#"C:\Users\Monster\Desktop\mamografi-scaled.jpg"
# YOLO modelini yükle
model = YOLO(model_path)

# Görüntüyü yükle
img = cv2.imread(image_path)

# OpenCV BGR okur, RGB'ye dönüştürelim
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Model ile tahmin yap
results = model.predict(source=img_rgb, save=False, save_txt=False)

# Tahmin edilen sonuçları göster
annotated_frame = results[0].plot()  # Modelin anotasyonlu çıktısı

# RGB görüntüyü göster
plt.imshow(cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
