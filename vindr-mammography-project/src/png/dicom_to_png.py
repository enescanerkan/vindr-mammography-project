import os
import zipfile
import numpy as np
import pydicom
from PIL import Image
import cv2


def ensure_dir(directory):
    """Klasör varsa geç, yoksa oluştur."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def apply_windowing(pixel_array, window_center, window_width):
    """
    Window level ve width'e göre piksel değerlerini ölçekler.
    """
    lower_bound = window_center - (window_width / 2)
    upper_bound = window_center + (window_width / 2)

    # Piksel değerlerini pencereleme aralığına indirgeme
    pixel_array = np.clip(pixel_array, lower_bound, upper_bound)

    # Normalizasyon (0-255)
    normalized_array = ((pixel_array - lower_bound) / (upper_bound - lower_bound)) * 255
    return np.uint8(normalized_array)


def get_safe_dicom_value(value):
    """
    DICOM değerlerini işlemek için güvenli bir yöntem.
    MultiValue, DSfloat gibi özel durumları ele alır.
    """
    try:
        if isinstance(value, pydicom.multival.MultiValue):
            return float(value[0])  # İlk değeri kullan
        elif isinstance(value, (pydicom.valuerep.DSfloat, pydicom.valuerep.DSdecimal)):
            return float(value)
        return float(value)
    except Exception:
        return None  # Eğer değer okunamıyorsa None döndür


def dicom_to_png(dicom_file, output_path):
    """
    DICOM dosyasını PNG formatına dönüştürür.
    """
    try:
        # DICOM dosyasını oku
        ds = pydicom.dcmread(dicom_file)
        pixel_array = ds.pixel_array

        # Pencereleme merkezi ve genişliğini belirle
        window_center = get_safe_dicom_value(ds.get("WindowCenter"))
        window_width = get_safe_dicom_value(ds.get("WindowWidth"))

        # Eğer pencereleme bilgisi eksikse otomatik hesapla
        if window_center is None:
            window_center = (pixel_array.max() + pixel_array.min()) / 2
        if window_width is None:
            window_width = (pixel_array.max() - pixel_array.min())

        # Pencereleme uygula
        pixel_array = apply_windowing(pixel_array, window_center, window_width)

        # Görüntüyü PNG formatına dönüştür ve kaydet
        image = Image.fromarray(pixel_array)
        image = image.convert("L")  # Gri tonlama
        image.save(output_path, "JPEG", quality=95)
        print(f"Başarılı: {output_path}")
    except Exception as e:
        print(f"Hata ({output_path}): {e}")


def process_zip(zip_path, output_folder):
    """
    ZIP içerisindeki tüm DICOM dosyalarını PNG formatına dönüştürür.
    - zip_path: ZIP dosyasının yolu.
    - output_folder: Çıktı dosyalarının kaydedileceği klasör.
    """
    with zipfile.ZipFile(zip_path, 'r') as z:
        for file_name in z.namelist():
            # Sadece DICOM dosyalarını işliyoruz
            if file_name.endswith(".dicom"):
                try:
                    # Çıktı dosyasının yolu
                    relative_path = os.path.splitext(file_name)[0]  # .dicom uzantısını çıkar
                    output_path = os.path.join(output_folder, relative_path + ".png")

                    # Çıktı klasör yapısını oluştur
                    ensure_dir(os.path.dirname(output_path))

                    # ZIP içerisindeki DICOM dosyasını okuyarak dönüştür
                    with z.open(file_name) as dicom_file:
                        dicom_to_png(dicom_file, output_path)
                except Exception as e:
                    print(f"Hata ({file_name}): {e}")
            else:
                # Diğer dosyaları olduğu gibi çıkart
                output_path = os.path.join(output_folder, file_name)
                ensure_dir(os.path.dirname(output_path))
                with z.open(file_name) as file:
                    with open(output_path, "wb") as out_file:
                        out_file.write(file.read())
                print(f"Diğer dosya taşındı: {output_path}")


# Ana çalışma fonksiyonu
if __name__ == "__main__":
    # Kullanıcı ayarları
    zip_file_path = r"C:\Users\Monster\Desktop\Tubitak İTÜ\src\mammo_dataset.zip" # ZIP dosyasının tam yolu
    output_directory = r"C:\Users\Monster\Desktop\mammo_dataset_output_PNG"  # Çıktıların kaydedileceği klasör

    # Çıktı klasörünü oluştur
    ensure_dir(output_directory)

    # ZIP dosyasını işle
    process_zip(zip_file_path, output_directory)

    print("İşlem tamamlandı!")
