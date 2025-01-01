# Create By RGYUGHI
import asyncio
import json
import os
import random
import sys
import time
import uuid
from urllib.parse import urlparse
import schedule
import cloudscraper
import requests
from curl_cffi import requests
from loguru import logger
from pyfiglet import figlet_format
from termcolor import colored
from daily import run_daily_claim
from fake_useragent import UserAgent
import concurrent.futures

# Create By RGYUGHI
# Konfigurasi global
SHOW_REQUEST_ERROR_LOG = False

PING_INTERVAL = 60
RETRIES = 60
MAX_CONCURRENT = 100 # Batasan jumlah koneksi bersamaan

# Create By RGYUGHI
DOMAIN_API = {
    "SESSION": "http://api.nodepay.ai/api/auth/session", 
    "PING": ["https://nw.nodepay.org/api/network/ping"],
    "DAILY_CLAIM": "https://api.nodepay.org/api/mission/complete-mission",
}

# Create By RGYUGHI
CONNECTION_STATES = {
    "CONNECTED": 1,
    "DISCONNECTED": 2, 
    "NONE_CONNECTION": 3
}

status_connect = CONNECTION_STATES
account_info = {}
last_ping_time = {}
token_status = {}
browser_id = None

# Create By RGYUGHI
# Setup logger
logger.remove()
logger.add(
    sink=sys.stdout,
    format="<r>[Nodepay]</r> | <white>TANGGAL: {time:YYYY-MM-DD}</white> | <white>WAKTU: {time:HH:mm:ss}</white> | "
           "<level>{level: ^7}</level> | <cyan>{line: <3}</cyan> | {message}",
    colorize=True
)
logger = logger.opt(colors=True)

# Create By RGYUGHI
def truncate_token(token):
    return f"{token[:4]}--{token[-4:]}"

def load_proxies():
    try:
        with open('proxy.txt', 'r') as file:
            proxies = file.read().splitlines()
            if proxies:
                logger.info(f"<green>Berhasil memuat {len(proxies)} proxy dari proxy.txt</green>")
                return proxies
            else:
                logger.warning("<yellow>File proxy.txt kosong</yellow>")
                return []
    except FileNotFoundError:
        logger.error("<red>File proxy.txt tidak ditemukan</red>")
        return []

# Create By RGYUGHI
def load_tokens():
    try:
        with open('token.txt', 'r') as file:
            tokens = file.read().splitlines()
            if tokens:
                # Batasi maksimal 2000 token
                tokens = tokens[:2000]
                logger.info(f"<green>Berhasil memuat {len(tokens)} token dari token.txt</green>")
                return tokens
            else:
                logger.warning("<yellow>File token.txt kosong</yellow>")
                return []
    except FileNotFoundError:
        logger.error("<red>File token.txt tidak ditemukan</red>")
        return []

# Create By RGYUGHI
def assign_proxies_to_tokens(tokens, proxies):
    if not proxies:
        return [(token, None) for token in tokens]
    paired = []
    for i, token in enumerate(tokens):
        proxy = proxies[i % len(proxies)]
        paired.append((token, proxy))
    return paired

def extract_proxy_ip(proxy_url):
    try:
        return urlparse(proxy_url).hostname
    except Exception:
        return "Unknown"

# Create By RGYUGHI
def get_ip_address(proxy=None):
    try:
        url = "https://api.ipify.org?format=json"
        response = cloudscraper.create_scraper().get(url, proxies={"http": proxy, "https": proxy} if proxy else None)
        return response.json().get("ip", "Unknown") if response.status_code == 200 else "Unknown"
    except Exception as e:
        logger.error(f"<red>Gagal mendapatkan alamat IP: {e}</red>")
    return "Unknown"

# Create By RGYUGHI
def log_user_data(users_data):
    if not users_data:
        logger.error("<red>Data pengguna tidak tersedia.</red>")
        return

    try:
        for user_data in users_data:
            name = user_data.get("name", "Unknown")
            balance = user_data.get("balance", {})
            logger.info(f"Pengguna: <green>{name}</green>, "
                       f"Saldo Saat Ini: <green>{balance.get('current_amount', 0)}</green>, "
                       f"Total Terkumpul: <green>{balance.get('total_collected', 0)}</green>")
    except Exception as e:
        if SHOW_REQUEST_ERROR_LOG:
            logger.error(f"Error logging: {e}")

# Create By RGYUGHI
async def call_api(url, data, token, proxy=None, timeout=60):
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": UserAgent().random,
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://app.nodepay.ai/",
        "Accept": "application/json, text/plain, */*",
        "Origin": "chrome-extension://lgmpfmgeabnnlemejacfljbmonaomfmm"
    }

    for attempt in range(3):
        try:
            response = requests.post(
                url,
                json=data,
                headers=headers,
                impersonate="chrome110", 
                proxies={"http": proxy, "https": proxy} if proxy else None,
                timeout=timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.warning(f"<yellow>Percobaan ke-{attempt + 1} gagal: {e}</yellow>")
            await asyncio.sleep(random.uniform(5, 10))
    
    logger.error("<red>Semua percobaan gagal</red>")
    return None

# Create By RGYUGHI
async def process_account(token, proxy=None):
    browser_id = str(uuid.uuid4())
    
    try:
        # Cek info akun
        account_info = await call_api(DOMAIN_API["SESSION"], {}, token, proxy)
        if not account_info or account_info.get("code") != 0:
            logger.error(f"<red>Gagal mendapatkan info akun untuk token: {truncate_token(token)}</red>")
            return

        name = account_info["data"].get("name", "Unknown")
        logger.info(f"<green>Berhasil login sebagai: {name}</green>")

        # Mulai ping dengan jeda random
        while True:
            ping_data = {
                "id": account_info["data"].get("uid"),
                "browser_id": browser_id,
                "timestamp": int(time.time()),
                "version": "2.2.7"
            }

            ping_response = await call_api(DOMAIN_API["PING"][0], ping_data, token, proxy)
            if ping_response and ping_response.get("code") == 0:
                ip = extract_proxy_ip(proxy) if proxy else get_ip_address()
                logger.info(f"<green>PING BERHASIL</green> | IP: <cyan>{ip}</cyan> | TOKEN: {truncate_token(token)}")
            else:
                logger.warning(f"<yellow>PING GAGAL untuk token: {truncate_token(token)}</yellow>")

            # Jeda random antara ping untuk menghindari deteksi
            await asyncio.sleep(random.uniform(PING_INTERVAL-10, PING_INTERVAL+10))

    except Exception as e:
        logger.error(f"<red>Error pada akun {truncate_token(token)}: {e}</red>")

# Create By RGYUGHI
async def process_batch(token_proxy_pairs):
    tasks = []
    for token, proxy in token_proxy_pairs:
        tasks.append(asyncio.create_task(process_account(token, proxy)))
        await asyncio.sleep(0.5) # Delay kecil antar akun dalam batch
    await asyncio.gather(*tasks)

# Create By RGYUGHI
async def main():
    print(colored(figlet_format("RGYUGHI", font="slant"), "cyan"))
    print(colored("create by RGYUGHI", "cyan", attrs=["dark"]))
    logger.info("<green>Starting Nodepay Multi Account...</green>")

    tokens = load_tokens()
    proxies = load_proxies()

    if not tokens:
        logger.error("<red>Tidak ada token yang dimuat. Program berhenti.</red>")
        return

    token_proxy_pairs = assign_proxies_to_tokens(tokens, proxies)
    
    # Bagi token menjadi batch-batch kecil
    batch_size = MAX_CONCURRENT
    batches = [token_proxy_pairs[i:i + batch_size] for i in range(0, len(token_proxy_pairs), batch_size)]
    
    try:
        # Proses batch secara berurutan
        for i, batch in enumerate(batches):
            logger.info(f"<cyan>Memproses batch {i+1}/{len(batches)} ({len(batch)} akun)</cyan>")
            await process_batch(batch)
            await asyncio.sleep(2) # Delay antar batch
            
    except KeyboardInterrupt:
        logger.info("<yellow>Program dihentikan oleh pengguna.</yellow>")
    except Exception as e:
        logger.error(f"<red>Error: {e}</red>")

# Create By RGYUGHI
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram dihentikan. Keluar dengan aman...")
    finally:
        print("Membersihkan resources sebelum keluar.")
