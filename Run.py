from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import *
import requests
import threading
import time

i = 0

mainThread = None
toURL = ""
toProxy = []
toChat = ""
toPause = 0
toScreen = 0
toThreads = 10
threads = []


def run2(proxyList):
	global status_now, toURL, toPause, toScreen
	if toURL.startswith("http://") or toURL.startswith("https://"):
		pass
	else:
		toURL = "http://" + toURL
	for proxy in proxyList:
		print("Proxy: " + proxy)
		proxyIP = proxy.split(":")[0]
		proxyPort = int(proxy.split(":")[1])
		getScreenshot(url = toURL, proxyIP = proxyIP, proxyPort = proxyPort, pause = toPause, toScreen = toScreen)

def run():
	global status_now, toURL, toPause, toProxy, toScreen, toThreads, threads
	def divide(lst,n):
		return [lst[i::n] for i in range(n)]
	proxies = divide(toProxy, toThreads)
	for proxyList in proxies:
		threads.append(threading.Thread(target = run2, args = (proxyList,)).start())

def getScreenshot(url, proxyIP = None, proxyPort = None, pause = 15, toScreen = False):
	global i
	opts = webdriver.FirefoxOptions()
	opts.add_argument("--headless")
	profile = webdriver.FirefoxProfile()
	if proxyIP != None:
		profile.set_preference("network.proxy.type", 1)
		profile.set_preference("network.proxy.socks", proxyIP)
		profile.set_preference("network.proxy.socks_port", proxyPort)
		profile.set_preference("network.proxy.socks_version", 5)
	profile.update_preferences()
	try:
		driver = webdriver.Firefox(firefox_profile=profile, firefox_options=opts)
	except Exception as e:
		print("Не удалось инициализировать браузер")
		return
	driver.implicitly_wait(pause) # seconds
	print("Жду загрузки. " + str(pause) + " сек.")
	try:
		driver.get(url)
	except Exception as e:
		print("Ошибка открытия страницы. ")
		try:
			driver.close()
			driver.quit()
		except Exception as e:
			return
		finally:
			return
	time.sleep(pause)
	try:
		driver.close()
	except Exception as e:
		pass

	try:
		driver.quit()
	except Exception as e:
		pass

	i = i + 1
	print("Сделано. Всего:" + str(i))

if __name__ == '__main__':
	mainThread = None
	toURL = input("Введите ссылку: ")
	toPause = int(input("Введите сколько секунд ждать: "))
	toThreads = int(input("Сколько потоков (10 - оптимально): "))
	prox = [line.replace("\r","").strip('\n') for line in open('proxy.txt')]
	errorsProxy = 0
	for each in prox:
		x = each
		x = x.replace("1", "N").replace("2", "N").replace("3", "N")
		x = x.replace("4", "N").replace("5", "N").replace("6", "N")
		x = x.replace("7", "N").replace("8", "N").replace("9", "N")
		x = x.replace("0", "N").replace("NN", "N").replace("NN", "N").replace("NN", "N")
		if x == "N.N.N.N:N" and each != "N.N.N.N:N":
			toProxy.append(each)
		else:
			errorsProxy = errorsProxy + 1
	print("Загружено прокси: " + str(len(toProxy)) +". Ошибки в прокси: "+ str(errorsProxy))
	run()
