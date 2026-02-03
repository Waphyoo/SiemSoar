import requests
import json
import urllib3
from datetime import datetime
from typing import Dict, List, Optional

# ปิด SSL warning (ใช้สำหรับ testing เท่านั้น)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class WazuhAPI:
    """Class สำหรับจัดการ Wazuh API operations"""
    
    def __init__(self, host: str, username: str, password: str, port: int = 55000):
        """
        Initialize Wazuh API connection
        
        Args:
            host: Wazuh manager IP/hostname
            username: API username (default: wazuh)
            password: API password
            port: API port (default: 55000)
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.base_url = f"https://{host}:{port}"
        self.token = None
        self.headers = {}
        
    def authenticate(self) -> bool:
        """
        ทำการ authenticate กับ Wazuh API และเก็บ JWT token
        
        Returns:
            bool: True ถ้า authentication สำเร็จ
        """
        try:
            url = f"{self.base_url}/security/user/authenticate"
            response = requests.post(
                url,
                auth=(self.username, self.password),
                verify=False
            )
            
            if response.status_code == 200:
                self.token = response.json()['data']['token']
                self.headers = {
                    'Authorization': f'Bearer {self.token}',
                    'Content-Type': 'application/json'
                }
                print("[+] Authentication สำเร็จ!")
                return True
            else:
                print(f"[-] Authentication ล้มเหลว: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"[-] Error during authentication: {e}")
            return False
    
    def get_rules(self, limit: int = 1, search: str = None) -> Optional[Dict]:
        """
        ดึงข้อมูล rules

        Args:
            limit: จำนวน rules
            search: คำค้นหา (เช่น 'authentication')
        """
        print(f"\n[*] กำลังดึงข้อมูล rules...")
        params = {'limit': limit}
        if search:
            params['search'] = search

        response = requests.get(
            f"{self.base_url}/rules",
            headers=self.headers, params=params, verify=False
        )
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        return response.json()

    def get_rule_files(self, search: str = None) -> Optional[Dict]:
        """
        ดึงรายการไฟล์ rules ทั้งหมด

        Args:
            search: คำค้นหา (เช่น 'custom')
        """
        print(f"\n[*] กำลังดึงรายการไฟล์ rules...")
        params = {}
        if search:
            params['search'] = search

        response = requests.get(
            f"{self.base_url}/rules/files",
            headers=self.headers, params=params, verify=False
        )
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        return response.json()

    def get_rule_file_content(self, filename: str, raw: bool = False) -> Optional[Dict]:
        """
        ดึงเนื้อหาของไฟล์ rule ที่ระบุ

        Args:
            filename: ชื่อไฟล์ rule (เช่น 'custom_rules_example.xml')
            raw: ถ้า True จะดึง raw XML content
        """
        print(f"\n[*] กำลังดึงเนื้อหาไฟล์ rule: {filename}...")
        params = {}
        if raw:
            params['raw'] = 'true'
        else:
            params['raw'] = 'false'

        response = requests.get(
            f"{self.base_url}/rules/files/{filename}",
            headers=self.headers, params=params, verify=False
        )

        if raw:
            print(response.text)
            return response.text

        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        return response.json()

    def update_rule_file(self, filename: str, body: str, overwrite: bool = False, relative_dirname: str = "etc/rules") -> Optional[Dict]:
        """
        อัปเดตไฟล์ rule

        Args:
            filename: ชื่อไฟล์ rule (เช่น 'custom_rules_example.xml')
            body: เนื้อหา XML ของ rule
            overwrite: เขียนทับไฟล์เดิม (default: True)
            relative_dirname: path ของไฟล์ rule (default: 'etc/rules')
        """
        print(f"\n[*] กำลังอัปเดตไฟล์ rule: {filename}...")
        params = {
            'overwrite': overwrite,
            'relative_dirname': relative_dirname
        }
        headers2 = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/octet-stream'
        }

        response = requests.put(
            f"{self.base_url}/rules/files/{filename}",
            headers=headers2, params=params, data=body.encode('utf-8'), verify=False
        )
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        return response.json()

    def run_logtest(self, event: str, log_format: str = "syslog", location: str = "logtest") -> Optional[Dict]:
        """
        ทดสอบ log event กับ rules (logtest)

        Args:
            event: log event ที่ต้องการทดสอบ
            log_format: รูปแบบ log (default: 'syslog')
            location: ตำแหน่ง log (default: 'logtest')
        """
        print(f"\n[*] กำลังทดสอบ log event...")
        data = {
            'log_format': log_format,
            'location': location,
            'event': event
        }

        response = requests.put(
            f"{self.base_url}/logtest",
            headers=self.headers, json=data, verify=False
        )
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        return response.json()



def main():
 
    # Configuration - แก้ไขตามสภาพแวดล้อมของคุณ
    WAZUH_HOST = "10.10.184.114"  # IP/hostname ของ Wazuh manager
    WAZUH_USER = "apibot"           # Username
    WAZUH_PASS = "APIbot321!"           # Password
    WAZUH_PORT = 55000             # API port
    
    # สร้าง API instance
    api = WazuhAPI(
        host=WAZUH_HOST,
        username=WAZUH_USER,
        password=WAZUH_PASS,
        port=WAZUH_PORT
    )
    
    
    if not api.authenticate():
        print("[-] ไม่สามารถ authenticate ได้ กรุณาตรวจสอบ credentials")
        return
    

    api.get_rules(limit=1, search="authentication")

    api.get_rule_files(search="custom")

    api.get_rule_file_content("custom_rules_example.xml")
    api.get_rule_file_content("custom_rules_example.xml", raw=True)

    rule_xml = """<group name="custom_rules_example">
  <rule id="100013" level="0">
    <program_name>3example</program_name>
    <description>User logged - 3example program</description>
  </rule>

  <rule id="100012" level="0">
    <program_name>2example</program_name>
    <description>User logged - 2example program</description>
  </rule>

  <rule id="100010" level="0">
    <program_name>example</program_name>
    <description>User logged - example program</description>
  </rule>
</group> """
    api.update_rule_file("custom_rules_example.xml", body=rule_xml, overwrite=True)

 
    api.run_logtest(
        event="Dec 25 20:45:02 MyHost 2example[12345]: User 'admin' logged from '192.168.1.100'"
    )
    



if __name__ == "__main__":
    main()