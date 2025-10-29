# 🎯 Face Recognition + Absensi Otomatis

Aplikasi ini menggunakan **Convolutional Neural Network (CNN)** untuk mengenali wajah dan mencatat absensi otomatis ke file **CSV**, lengkap dengan tampilan GUI (Tombol Mulai, Lihat Data, dan Keluar).

---

## ⚙️ 1. Cara Menjalankan Program

### 🧩 Aktifkan Virtual Environment
venv\Scripts\activate

🧠 Install Library
pip install -r requirements.txt

🚀 Jalankan Aplikasi GUI
python face_recognition_gui.py

## 2. Menambahkan Data Training & Test
📸 Tambah Orang Baru

Buat folder baru di:

dataset/train/NamaTeman/
dataset/test/NamaTeman/


Isi masing-masing folder dengan beberapa foto wajah (3–10 foto).
Contoh:

dataset/train/Rafi/
├── 1.jpg
├── 2.jpg
├── 3.jpg

⚙️ Update label di face_recognition_gui.py


## 🧠 3. Latih Ulang Model

Setelah menambah data baru, jalankan ulang:

python face_train.py


Hasil model baru otomatis disimpan sebagai:

face_cnn_model.h5

## 🧾 4. Lihat Hasil Absensi

Data tersimpan otomatis di file:

absensi.csv

Edit baris ini:

class_names = ['Alif', 'Yusuf', 'Rafi']
