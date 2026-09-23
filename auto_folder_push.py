import os
import json
import base64
import requests

# ==================== VMOS CLOUD कॉन्फ़िगरेशन ====================
# स्क्रीनशॉट के अनुसार क्रेडेंशियल्स सेट किए गए हैं
HOST = "https://api.vmoscloud.com"
ACCESS_KEY = "GXCUvC2GyDu0qQtCBFlxSwNA9x"
SECRET_KEY = "fafImINSIemr3m9PhqITpbdR"
PAD_CODE   = "APP636640QA50FX4"

# लोकल फ़ोल्डर जहाँ आपकी फाइलें रखी हैं
LOCAL_FOLDER = "files_to_send"

# क्लाउड फोन का फोल्डर पाथ
REMOTE_FOLDER = "/sdcard/Download"
# ================================================================

def push_file_vmos(local_path, file_name, remote_dest_folder):
    """VMOS Cloud API के ज़रिए फ़ाइल पुश करना"""
    endpoint = f"{HOST}/vcpcloud/api/padApi/pushFile"
    remote_file_path = f"{remote_dest_folder.rstrip('/')}/{file_name}"

    with open(local_path, "rb") as f:
        file_bytes = f.read()
        b64_content = base64.b64encode(file_bytes).decode("utf-8")

    payload = {
        "accessKeyId": ACCESS_KEY,
        "secretAccessKey": SECRET_KEY,
        "padCode": PAD_CODE,
        "filePath": remote_file_path,
        "fileContent": b64_content
    }

    headers = {
        "Content-Type": "application/json"
    }

    print(f"[*] भेज रहे हैं: {file_name} -> {remote_file_path}")

    try:
        response = requests.post(endpoint, json=payload, headers=headers, timeout=40)
        
        if response.status_code == 200:
            res_data = response.json()
            if res_data.get("code") == 200 or res_data.get("success") is True:
                print(f"[✔] सफ़ल: {file_name}\n")
            else:
                print(f"[✘] सर्वर रिस्पॉन्स ({file_name}): {res_data}\n")
        else:
            print(f"[✘] HTTP एरर {response.status_code} ({file_name}): {response.text}\n")
            
    except requests.exceptions.RequestException as e:
        print(f"[!] नेटवर्क एरर: {e}\n")

def main():
    print("==================================================")
    print("      VMOS Cloud Auto Folder Push Tool            ")
    print("==================================================")
    print(f"टारगेट डिवाइस (PAD CODE): {PAD_CODE}")
    print(f"टारगेट क्लाउड फ़ोल्डर: {REMOTE_FOLDER}\n")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    source_folder = os.path.join(script_dir, LOCAL_FOLDER) if not os.path.isabs(LOCAL_FOLDER) else LOCAL_FOLDER

    if not os.path.exists(source_folder):
        print(f"[✘] लोकल फ़ोल्डर नहीं मिला: {source_folder}")
        return

    items = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]

    if not items:
        print(f"[!] '{source_folder}' फ़ोल्डर खाली है।")
        return

    print(f"[*] कुल {len(items)} फ़ाइलें मिलीं। अपलोडिंग शुरू...\n")

    for item in items:
        full_local_path = os.path.join(source_folder, item)
        push_file_vmos(full_local_path, item, REMOTE_FOLDER)

    print("[✔] प्रोसेस पूरा हुआ।")

if __name__ == "__main__":
    main()
