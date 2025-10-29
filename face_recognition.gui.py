import cv2
import tensorflow as tf
import numpy as np
import os
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# =====================================================
# 1️⃣ LOAD MODEL DAN LABEL
# =====================================================
print("[INFO] Memuat model CNN...")
model = tf.keras.models.load_model('face_cnn_model.h5')
class_names = ['Alif', 'Dito', 'Fadhil', 'Toni']  # Ganti sesuai folder dataset/train

# =====================================================
# 2️⃣ FILE ABSENSI OTOMATIS
# =====================================================
absen_file = 'absensi.csv'
if not os.path.exists(absen_file):
    df = pd.DataFrame(columns=['Nama', 'Waktu'])
    df.to_csv(absen_file, index=False)

def catat_absensi(nama):
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.read_csv(absen_file)
    if nama not in list(df['Nama']):
        new_data = pd.DataFrame([[nama, waktu]], columns=['Nama', 'Waktu'])
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(absen_file, index=False)
        print(f"[✔] {nama} tercatat pada {waktu}")

# =====================================================
# 3️⃣ DETEKSI KAMERA OTOMATIS
# =====================================================
def get_available_camera():
    for i in range(5):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"[INFO] Kamera index {i} digunakan.")
            return cap
    print("[ERROR] Tidak ada kamera terdeteksi.")
    return None

# =====================================================
# 4️⃣ FUNGSI UTAMA: MULAI ABSENSI
# =====================================================
def mulai_absensi():
    cap = get_available_camera()
    if cap is None:
        messagebox.showerror("Error", "Kamera tidak terdeteksi!")
        return

    cap.set(3, 640)
    cap.set(4, 480)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    messagebox.showinfo("Info", "Tekan 'q' untuk menghentikan absensi.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Kamera tidak aktif.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face_roi = frame[y:y+h, x:x+w]
            face_roi = cv2.resize(face_roi, (150, 150))
            face_roi = np.expand_dims(face_roi, axis=0) / 255.0

            predictions = model.predict(face_roi)
            class_index = np.argmax(predictions)
            confidence = np.max(predictions)

            if confidence > 0.8:
                nama = class_names[class_index]
                catat_absensi(nama)
                label = f"{nama} ({confidence*100:.1f}%)"
                color = (0, 255, 0)
            else:
                label = "Tidak Dikenal"
                color = (0, 0, 255)

            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        cv2.imshow('Face Recognition - Absensi Otomatis', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# =====================================================
# 5️⃣ LIHAT DATA ABSENSI
# =====================================================
def lihat_absensi():
    if not os.path.exists(absen_file):
        messagebox.showinfo("Info", "Belum ada data absensi.")
        return

    df = pd.read_csv(absen_file)
    if df.empty:
        messagebox.showinfo("Info", "Belum ada nama yang tercatat.")
        return

    top = tk.Toplevel(window)
    top.title("Data Absensi")
    top.geometry("400x300")

    tree = ttk.Treeview(top, columns=("Nama", "Waktu"), show='headings')
    tree.heading("Nama", text="Nama")
    tree.heading("Waktu", text="Waktu")
    tree.pack(fill=tk.BOTH, expand=True)

    for _, row in df.iterrows():
        tree.insert("", tk.END, values=(row["Nama"], row["Waktu"]))

# =====================================================
# 6️⃣ GUI UTAMA TKINTER
# =====================================================
window = tk.Tk()
window.title("Face Recognition - Absensi Otomatis")
window.geometry("400x350")
window.configure(bg="#1E1E1E")

title_label = tk.Label(window, text="📸 Absensi Wajah Otomatis", fg="white", bg="#1E1E1E", font=("Arial", 16, "bold"))
title_label.pack(pady=20)

btn_mulai = tk.Button(window, text="▶️  Mulai Absensi", bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), width=25, height=2, command=mulai_absensi)
btn_mulai.pack(pady=10)

btn_lihat = tk.Button(window, text="📋  Lihat Data Absensi", bg="#2196F3", fg="white", font=("Arial", 12, "bold"), width=25, height=2, command=lihat_absensi)
btn_lihat.pack(pady=10)

btn_keluar = tk.Button(window, text="❌  Keluar", bg="#F44336", fg="white", font=("Arial", 12, "bold"), width=25, height=2, command=window.destroy)
btn_keluar.pack(pady=10)

credit = tk.Label(window, text="Dibuat oleh: Kelompok 5", bg="#1E1E1E", fg="#AAAAAA", font=("Arial", 9))
credit.pack(side=tk.BOTTOM, pady=10)

window.mainloop()
