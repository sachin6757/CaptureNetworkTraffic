from browsermobproxy import Server
from selenium import webdriver
import json

def CaptureNetworkTraffic(url,server_ip,headers,file_path):
	''' 
	This function can be used to capture network traffic from the browser. Using this function we can capture header/cookies/http calls made from the browser
	url - Page url
	server_ip - remap host to for specific URL
	headers - this is a dictionary of the headers to be set
	file_path - File in which HAR gets stored
	'''
	port = {'port':9090}
	server = Server("G:\\browsermob\\bin\\browsermob-proxy",port) #Path to the BrowserMobProxy
	server.start()
	proxy = server.create_proxy()
	proxy.remap_hosts("www.example.com",server_ip)
	proxy.remap_hosts("www.example1.com",server_ip)
	proxy.remap_hosts("www.example2.com",server_ip)
	proxy.headers(headers)
	profile  = webdriver.FirefoxProfile()
	profile.set_proxy(proxy.selenium_proxy())
	driver = webdriver.Firefox(firefox_profile=profile)
	new = {'captureHeaders':'True','captureContent':'True'}
	proxy.new_har("google",new)
	driver.get(url)
	proxy.har # returns a HAR JSON blob
	server.stop()
	driver.quit()
	file1 = open(file_path,'w')
	json.dump(proxy.har,file1)
	file1.close()

    
def Parse_Request_Response(filename,url,response=False,request_header=False,request_cookies=False,response_header=False,response_cookies=False):
    resp ={}
    har_data = open(filename, 'rb').read()
    har = json.loads(har_data)
    for i in har['log']['entries']:
        if url in i['request']['url']:
            resp['request'] = i['request']['url']
            if response:
                resp['response'] = i['response']['content']
            if request_header:
                resp['request_header'] = i['request']['headers']
            if request_cookies:
                resp['request_cookies'] = i['request']['cookies']
            if response_header:
                resp['response_header'] = i['response']['headers']
            if response_cookies:
                resp['response_cookies'] = i['response']['cookies']
    return resp


if (__name__=="__main__"):
    headers = {"User-Agent":"Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3"}
    CaptureNetworkTraffic("http://www.google.com","192.168.1.1",headers,"g:\\har.txt")
    print Capture_Request_Response("g:\\har.txt","google.com",False,True,False,False,False)

