[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# 💎 Etimo Diamonds 2

Diamonds adalah tantangan pemrograman. Anda diminta untuk membuat sebuah bot dan berkompetisi untuk mendapatkan skor tertinggi.

- [Spesifikasi Proyek](https://docs.google.com/document/d/13cbmMVXviyu8eKQ6heqgDzt4JNNMeAZO/edit)  
- [Panduan Memulai Diamonds](https://docs.google.com/document/d/1L92Axb89yIkom0b24D350Z1QAr8rujvHof7-kXRAp7c/edit)

---

## i. Penjelasan Singkat Algoritma Greedy yang Diimplementasikan

Bot ini menggunakan algoritma **Greedy** dengan pendekatan memilih diamond yang berada dalam radius terdekat dengan base dengan memprioritaskan diamonds dengan nilai tertinggi dan mempertimbangkan penggunaan teleporter untuk memaksimalkan perolehan skor secara keseluruhan. Bot mengevaluasi posisi berlian terdekat dan menghitung nilai tertinggi yang bisa didapatkan dalam langkah minimum, lalu bergerak ke arah tersebut.

---

## ii. Requirement Program dan Instalasi

### Requirement
- Python 3.8 atau lebih baru
- `pip` package manager

### Instalasi

1. Clone repository dan masuk ke direktori proyek:
    ```bash
    git clone https://github.com/haziqam/tubes1-IF2110-bot-starter-pack.git
    cd ./tubes1-IF2110-bot-starter-pack
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

---

## iii. Cara Menjalankan Program

### Menjalankan 1 Bot:
```bash
python main.py --logic Random --email=your_email@example.com --name=your_name --password=your_password --team etimo
```

### Menjalankan Beberapa Bot Sekaligus:

#### Untuk Windows:
```bash
./run-bots.bat
```

#### Untuk Linux / macOS:
```bash
chmod +x run-bots.sh
./run-bots.sh
```

> ⚠️ Pastikan setiap bot memiliki **email** dan **name** yang unik. Email hanya perlu sesuai format, name dan password bebas tanpa spasi.

---

## iv. Author (Identitas Pembuat)

- Annisa Al-Qoriah – 123140030  
- Muhammad Romadhon Santoso – 123140031  
- Stevanus Cahya Anggara – 123140038  
