from statistics import mode
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
class ipmi:
    def __init__(self,ip,username,passwd) -> None:
        self.ip = ip
        self.username = username
        self.passwd = passwd
        self.ipmi_url = 'https://'+self.ip
        self.random_tag_url = self.ipmi_url+'/api/randomtag'
        self.login_url = self.ipmi_url+'/api/session'
        self.psu_url = self.ipmi_url+'/api/status/psu_info'
        self.fans_url = self.ipmi_url+'/api/status/fan_info'
        self.fans_control_url = self.ipmi_url+'/api/settings/fans-mode'
        self.set_fans_url = self.ipmi_url +'/api/settings/fan/'
    def establish(self):
        self.sess = requests.session()
        random_tag_res = self.sess.get(self.random_tag_url, verify=False)
        random_tag_info = random_tag_res.content.decode()
        self.random_tag = int(random_tag_info[random_tag_info.index(":")+1:random_tag_info.index(",")])
        self.post_data = {
            "encrypt_flag": 0,
            "username": self.username,
            "password": self.passwd,
            "login_tag": self.random_tag    
        }
        post_res = self.sess.post(self.login_url,data=self.post_data,verify=False)
        get_cookie = post_res.headers['Set-Cookie']
        cookie_str = get_cookie[get_cookie.index("=")+1:get_cookie.index(";")]
        post_info = post_res.content.decode()
        CSRFToken = post_info[post_info.index("CSRFToken")+13:post_info.index("\"",post_info.index("CSRFToken")+13)]
        self.send_header = {
            'User-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36",
            'Cookie' : 'lang=zh-cn; QSESSIONID='+ cookie_str + '; refresh_disable=1',
            'X-CSRFTOKEN':CSRFToken,
            'Connection':'keep-alive'            
        }
    def get_power(self):
        psu_res = self.sess.get(self.psu_url,headers = self.send_header,verify=False)
        psu_info = psu_res.content.decode()
        psu = int(psu_info[psu_info.index("\"present_power_reading\": ")+24:psu_info.index(",",psu_info.index("\"present_power_reading\": ")+24)])
        return psu
    def get_fans(self,get_type = 'power'):
        fans_rec = self.sess.get(self.fans_url,headers = self.send_header,verify=False)
        fan_info = fans_rec.content.decode()
        fan_info_json = json.loads(fan_info)
        if get_type == 'power':
            return fan_info_json['fans_power']
        elif get_type == 'pwm':
            pwm_list = []
            fans_info_detail = fan_info_json['fans']
            for fan_index in fans_info_detail:
                pwm_list.append(fan_index['speed_percent'])
            return pwm_list
        print(fan_info)
    def control_fans(self,mode = 'auto',pwd = 66):
        if mode == 'manual':
            manual_json = {"control_mode": "manual"}
            self.sess.put(self.fans_control_url,headers = self.send_header,json=manual_json)
            fans_num = len(self.get_fans('pwm'))
            set_fans_json = {"duty": pwd}
            for ii in range(fans_num):
                self.sess.put(self.set_fans_url+str(ii),headers = self.send_header,json = set_fans_json)
        else:
            auto_json = {"control_mode": "auto"}
            self.sess.put(self.fans_control_url,headers = self.send_header,json=auto_json)
    def close(self):
        self.sess.close()


if __name__ == '__main__':
    with open('login.json','r') as f:
        login2str = f.read()
        print(login2str)
        login2json = json.loads(login2str)
        ip_str = login2json['ip']
        usr_str = login2json['user']
        passwd_str = login2json['password']
    i0 = ipmi(ip_str,usr_str,passwd_str)
    i0.establish()
    print(i0.control_fans())
    i0.close()