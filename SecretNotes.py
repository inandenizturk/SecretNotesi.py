import tkinter as tk
from tkinter import messagebox
import base64

def encode(key, clear):
    """Basit simetrik XOR + Base64 şifreleme"""
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()

def decode(key, enc):
    """Şifre çözme fonksiyonu"""
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)

def save_and_encrypt_notes():
    title = title_entry.get().strip()
    message = text_area.get("1.0", tk.END).strip()
    master_key = key_entry.get().strip()

    if not title or not message or not master_key:
        messagebox.showwarning("Eksik Bilgi", "Lütfen tüm alanları doldurun!")
        return

    # Şifrele
    encrypted_message = encode(master_key, message)

    try:
        with open("my_secret_notes.txt", "a", encoding="utf-8") as file:
            file.write(f"\n{title}\n{encrypted_message}\n")
        
        # Alanları temizle
        title_entry.delete(0, tk.END)
        text_area.delete("1.0", tk.END)
        key_entry.delete(0, tk.END)
        messagebox.showinfo("Başarılı", "Notunuz şifrelenerek kaydedildi!")
    except Exception as e:
        messagebox.showerror("Hata", f"Dosya kaydedilemedi: {e}")

def decrypt_notes():
    encrypted_message = text_area.get("1.0", tk.END).strip()
    master_key = key_entry.get().strip()

    if not encrypted_message or not master_key:
        messagebox.showwarning("Eksik Bilgi", "Lütfen şifreli metni ve anahtarı girin!")
        return

    try:
        decrypted_message = decode(master_key, encrypted_message)
        text_area.delete("1.0", tk.END)
        text_area.insert("1.0", decrypted_message)
    except Exception:
        messagebox.showerror("Hata", "Şifre çözülemedi! Anahtarı veya şifreli metni kontrol edin.")

# --- UI Kurulumu ---
root = tk.Tk()
root.title("Secret Notes")
root.config(padx=30, pady=30)

# Başlık
title_label = tk.Label(text="Enter your title", font=("Arial", 10, "bold"))
title_label.pack(pady=5)

title_entry = tk.Entry(width=35)
title_entry.pack(pady=5)

# Not Alanı
text_label = tk.Label(text="Enter your secret", font=("Arial", 10, "bold"))
text_label.pack(pady=5)

text_area = tk.Text(width=35, height=12)
text_area.pack(pady=5)

# Anahtar (Şifre) Alanı
key_label = tk.Label(text="Enter master key", font=("Arial", 10, "bold"))
key_label.pack(pady=5)

key_entry = tk.Entry(width=35, show="*")
key_entry.pack(pady=5)

# Butonlar
save_button = tk.Button(text="Save & Encrypt", command=save_and_encrypt_notes)
save_button.pack(pady=5)

decrypt_button = tk.Button(text="Decrypt", command=decrypt_notes)
decrypt_button.pack(pady=5)

root.mainloop()
