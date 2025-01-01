# NodePay Auto Mining By RGYUGHI

Script untuk menjalankan auto mining NodePay dengan multi akun dan proxy support.

## Fitur
- Support multi akun (maksimal 2000 akun)
- Support proxy 
- Auto ping untuk mining
- Auto daily claim
- Batasan koneksi bersamaan (100 koneksi)

## Cara Install & Menjalankan

### Windows
1. Install Python 3.8+ dari [python.org](https://www.python.org/downloads/)
2. Download dan extract script ini
   ```bash
   git clone https://github.com/BabyCobra1/NODEPAY.git
   cd nodepay
   ```
3. Buka CMD di folder script (Shift + Klik Kanan -> Open PowerShell/Command Prompt here)
4. Install requirements dengan perintah:
   ```bash
   pip install -r requirements.txt
   ```
5. Edit file `token.txt` dan masukkan akun dengan format:
   ```
   eyJhbG......
   eyJhbG......
   eyJhbG......
   ```
6. (WAJIB!!!) Edit file `proxy.txt`
7. Jalankan script dengan perintah:
   ```bash
   python nodepay.py or python3 nodepay.py
   ```

### Linux/Ubuntu
1. Install Python dan pip:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```
2. Clone atau download script ini
3. Masuk ke folder script:
   ```bash
   git clone https://github.com/BabyCobra1/NODEPAY.git
   cd nodepay
   ```
4. Install requirements:
   ```bash
   pip3 install -r requirements.txt
   ```
5. Edit file token.txt menggunakan nano:
   ```bash
   nano token.txt
   ```
6. Edit file proxy.txt menggunakan nano:
   ```bash
   nano proxy.txt
   ```
7. Jalankan script:
   ```bash
   python nodepay.py or python3 nodepay.py
   ```

### Termux (Android)
1. Install Termux dari F-Droid
2. Update package dan install python:
   ```bash
   pkg update && pkg upgrade
   pkg install python git
   ```
3. Clone repository:
   ```bash
   git clone https://github.com/BabyCobra1/NODEPAY.git
   cd nodepay
   ```
4. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
5. Edit file token.txt menggunakan nano:
   ```bash
   nano token.txt
   ```
6. Edit file proxy.txt menggunakan nano:
   ```bash
   nano proxy.txt
   ```
   Tambahkan akun lalu tekan Ctrl + X, Y, dan Enter untuk menyimpan
7. Jalankan script:
   ```bash
   python nodepay.py or python3 nodepay.py
   ```

## Konfigurasi
- `token.txt`: List akun dengan format email:password
- `proxy.txt`: List proxy dengan format ip:port atau ip:port:username:password
- `config.json`: Pengaturan script seperti delay dan jumlah thread

## Troubleshooting
1. Jika ada error "pip not found":
   - Windows: Reinstall Python dan centang "Add Python to PATH"
   - Linux: Install pip dengan `sudo apt install python3-pip`
   - Termux: `pkg install python-pip`

2. Jika ada error module not found:
   Jalankan ulang perintah install requirements

3. Jika script crash/error:
   - Pastikan internet stabil
   - Cek format token.txt dan proxy.txt
   - Kurangi jumlah thread di config.json

## Catatan
- Gunakan proxy untuk menghindari IP ban
- Jangan gunakan terlalu banyak akun dalam satu IP
- Backup token.txt secara berkala
- Script ini gratis dan open source
