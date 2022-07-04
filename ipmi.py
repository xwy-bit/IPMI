import requests
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
    def close(self):
        self.sess.close()


if __name__ == '__main__':
    i0 = ipmi('10.123.456.789','ADMIN','ADMIN')
    i0.establish()
    for _ in range(10):
        print(i0.get_power())
    i0.close()