# vindr-mammography-project
Bu projede VinDr-Mammo veri seti kullanarak , mamografi görüntülerinde kitle tespiti yapmak amacıyla YOLOv11 modellerini kullanarak derin öğrenme tabanlı bir çözüm geliştirmektedir.(This project develops a deep learning-based solution using the YOLOv11 models for mass detection in mammography images.)
```bash
vindr-mammography-project/
├── notebooks/
│   ├── category_mapping
│   ├── config.yaml
│   ├── Fine_Tuning.ipynb
│   ├── main.ipynb
│   └── YOLOv11_Training.ipynb
├── results/
│   ├── only_mass_YOLOv11-Medium(png)/
│   │   ├── onlymass_test1.png
│   │   ├── onlymass_test2.png
│   │   ├── train_batch0.jpg
│   │   ├── train_batch1.jpg
│   │   ├── train_batch2.jpg
│   │   ├── train_batch7840.jpg
│   │   ├── train_batch7841.jpg
│   │   ├── train_batch7842.jpg
│   │   ├── val_batch0_labels.jpg
│   │   ├── val_batch0_pred.jpg
│   │   ├── val_batch1_labels.jpg
│   │   ├── val_batch1_pred.jpg
│   │   ├── val_batch2_labels.jpg
│   │   └── val_batch2_pred.png
│   ├── YOLOv11-Large(Fine_Tuning)/
│   ├── YOLOv11-Large(jpg)/
│   └── YOLOv11-Medium(png)/
├── src/
│   ├── augment_images_labels.py
│   ├── class_names_labels.py
│   ├── dicom_to_jpg.py
│   ├── images_labels_matching.py
│   ├── images_split.py
│   ├── labels_split.py
│   ├── model_test.py
│   ├── show_dicom_image.py
│   ├── show_labels_on_images.py
│   └── png/
│       ├── dicom_to_png.py
│       └── png_images_split.py

```
## Proje Yapısı

Proje, aşağıdaki klasör yapısına sahiptir:

### 1. **notebooks** 
  - **category_mapping**: Kategorileri eşlemek için kullanılan dosya.
  - **config.yaml**: Proje ayarları ve hiperparametrelerin bulunduğu yapılandırma dosyası.(YOLO eğitimi için gereklidir.)
  - **Fine_Tuning.ipynb**: İnce ayar (fine-tuning) süreciyle ilgili notebook.(Yarım kalan eğitimi yeniden başlattığım ayarlar.)
  - **main.ipynb**: Ana işlemlerin bulunduğu notebook.(Baştan sona projenin özeti yer almaktadır.)
  - **YOLOv11_Training.ipynb**: YOLOv11 modelinin eğitim süreci.(Colab üzerinden yapılan eğitim defteridir.)

### 2. **results**
Eğitim ve test sonuçlarının saklandığı klasör.
  - **only_mass_YOLOv11-Medium(png)**: Yalnızca Mass sınıfı ve png görüntülerden oluşan veri seti üzerinde eğitilen modelin çıktıları.
  - **YOLOv11-Large(jpg)**: YOLOv11 modelinin large versiyonu ile  jpg  görüntülerden oluşan veri setiyle colab erişim sınırı yüzünden erken biten eğitimin sonuçları.
  - **YOLOv11-Large(Fine_Tuning)**: YOLOv11 modelinin large versiyonu ile  jpg  görüntülerden oluşan veri setiyle , eğitime devam edildikten sonraki sonuçlar.
  - **YOLOv11-Medium(png)**: YOLOv11  medium modeliyle  png görüntülerden oluşan veri setiyle yapılan eğitimin  sonuçları.

### 3. **src**
Projenin Python scriptlerinin yer aldığı klasör.
  - **augment_images_labels.py**: Görüntü ve etiket artırımı.
  - **class_names_labels.py**: Sınıf isimlerini ve etiketlerini yöneten dosya.
  - **dicom_to_jpg.py**: DICOM formatından JPG formatına dönüştürme.
  - **images_labels_matching.py**: Görüntülerle etiketleri eşleştirme işlemi.
  - **images_split.py**: Görüntüleri eğitim ve test için bölen dosya.
  - **labels_split.py**: Etiketleri eğitim ve test için bölen dosya.
  - **model_test.py**: Model test etme işlemleri.
  - **show_dicom_image.py**: DICOM görüntülerini gösterme.
  - **show_labels_on_images.py**: Görüntüler üzerinde etiketlerin gösterilmesi.

### 4. **png** (Alt Klasör)
  - **dicom_to_png.py**: DICOM formatından PNG formatına dönüştürme.
  - **png_images_split.py**: PNG formatındaki görüntüleri eğitim ve test setlerine ayırma.

## SONUÇ GÖRSELLERİ(Tüm Sınıfların Olduğu Ve Çoğaltılmış Veri Seti Olan):

<div style="display: flex; justify-content: space-around;">
    <img src="https://github.com/user-attachments/assets/5e217c31-b3ba-4adc-9307-7ce6a0512faa" width="45%" />
    <img src="https://github.com/user-attachments/assets/f536f77e-35b7-4ab4-a2b1-c33b63f3c372" width="45%" />
</div>
<div style="display: flex; justify-content: space-around;">
    <img src="https://github.com/user-attachments/assets/89eb6eb4-a0c0-4fee-b22d-e89e2378e640" width="45%" />
    <img src="https://github.com/user-attachments/assets/9d1d6d8e-ac24-4a19-9072-05a0c16994fe" width="45%" />
</div>



## Kullanılan Teknolojiler ve Kütüphaneler

Proje, aşağıdaki kütüphaneleri ve teknolojileri kullanmaktadır:
- **Python 3.12**
- **OpenCV 4.10.0.84**
- **Ultralytics 8.3.13**
- **Pandas 2.2.2**
- **NumPy 1.26.4**
- **pydicom 2.4.4**
- **pillow 10.3.0**
- **matplotlib 3.9.0**
- **TensorFlow / PyTorch** (Eğitimde kullanılan derin öğrenme framework'leri)

## Kurulum

Bu projeyi çalıştırmak için aşağıdaki adımları takip edebilirsiniz:

1. Bu projeyi bilgisayarınıza klonlayın:
   ```bash
   git clone https://github.com/enescanerkan/vindr-mammography-project.git
