from selenium.webdriver.common.proxy import *
from selenium import webdriver

# myProxyUrl = "http://149.215.113.110:70"
# myProxy = Proxy({
#     'httpProxy': myProxyUrl,
#     'ftpProxy': myProxyUrl,
#     'sslProxy': myProxyUrl,
#     'noProxy': ''
# })

browser = webdriver.PhantomJS()
browser.get('http://kuailv.meituan.com/wxmall/api/goods/list?cat1Id=1000875&cat2Id=1001397&pageNo=1&cityId=110100&_=1530006506987')
print(browser.page_source)

proxy = webdriver.Proxy()
proxy.proxy_type = ProxyType.MANUAL
proxy.http_proxy = "47.106.135.10:443"

proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
browser.start_session(webdriver.DesiredCapabilities.PHANTOMJS)
browser.get('http://kuailv.meituan.com/wxmall/api/goods/list?cat1Id=1000875&cat2Id=1001397&pageNo=1&cityId=110100&_=1530006506987')
print(browser.page_source)


# # 还原为系统代理
# proxy=webdriver.Proxy()
# proxy.proxy_type=ProxyType.DIRECT
# proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
# browser.start_session(webdriver.DesiredCapabilities.PHANTOMJS)
# browser.get('http://1212.ip138.com/ic.asp')