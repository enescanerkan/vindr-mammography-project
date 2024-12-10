import cv2
import matplotlib.pyplot as plt

# Görüntü ve etiket dosyasının yolları
# image_path = r"C:\Users\Monster\Desktop\0a6f0eac805822cd00f3c25ba99569e8.jpg"
# label_path = r"C:\Users\Monster\Desktop\0a6f0eac805822cd00f3c25ba99569e8.txt"
# image_path = r"C:\Users\Monster\Desktop\00be38a5c0566291168fe381ba0028e6.jpg"
# label_path = r"C:\Users\Monster\Desktop\00be38a5c0566291168fe381ba0028e6.txt"

image_path = r"C:\Users\Monster\Desktop\b6d0903ba96ff1157a6b055bd56181d3.jpg"
label_path = r"C:\Users\Monster\Desktop\b6d0903ba96ff1157a6b055bd56181d3.txt"
# "C:\Users\Monster\Desktop\b6d0903ba96ff1157a6b055bd56181d3.jpg"
# b6d0903ba96ff1157a6b055bd56181d3
# Görüntüyü yükle
image = cv2.imread(image_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Etiket dosyasını oku ve bounding box'ları çiz
image_height, image_width, _ = image.shape
with open(label_path, 'r') as f:
    for line in f.readlines():
        parts = line.strip().split()
        class_id = int(parts[0])
        x_center, y_center, width, height = map(float, parts[1:])

        # Bounding box koordinatlarını çöz
        xmin = int((x_center - width / 2) * image_width)
        ymin = int((y_center - height / 2) * image_height)
        xmax = int((x_center + width / 2) * image_width)
        ymax = int((y_center + height / 2) * image_height)

        # Bounding box'u çiz
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color=(255, 0, 0), thickness=2)

# Görüntüyü göster
plt.imshow(image)
plt.axis('off')
plt.show()
