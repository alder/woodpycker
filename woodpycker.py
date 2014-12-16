#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import argparse
import json
from urlparse import urlparse
from selenium import webdriver
from browsermobproxy import Server
from colorama import init, Fore, Style


def show_status_codes(har,allowed_domain):
	for entry in har['log']['entries']:
		domain = urlparse(entry['request']['url'])
		domain = domain.netloc
		if domain.find(allowed_domain) != -1:
			status = Style.BRIGHT + str(entry['response']['status']) + " - " + entry['response']['statusText'] + Style.RESET_ALL
			if entry['response']['status'] >= 200 and entry['response']['status'] < 300:
				status = Fore.GREEN + str(entry['response']['status']) + " - " + entry['response']['statusText'] + Fore.RESET
			if entry['response']['status'] >= 400 and entry['response']['status'] < 500:
				status = Fore.YELLOW + str(entry['response']['status']) + " - " + entry['response']['statusText'] + Fore.RESET
			if entry['response']['status'] >= 500 and entry['response']['status'] < 600:
				status = Fore.RED + str(entry['response']['status']) + " - " + entry['response']['statusText'] + Fore.RESET
			print "-- %s [%s]" % (entry['request']['url'],status)


def main(argv):
	init()

	parser = argparse.ArgumentParser()
	parser.add_argument('-u', action='store', dest='start_url', help='Set page URL', required=True)
	parser.add_argument('-c', action='store', dest='cookies_file', help='JSON file with cookies', required=False)
	parser.add_argument('-w', action='store', dest='webdriver_type', help='Set WebDriver type (firefox or phantomjs, firebox by default)', default="firefox", required=False)
	results = parser.parse_args()
	
	start_url = results.start_url
	cookies_file = results.cookies_file
	webdriver_type = results.webdriver_type

	allowed_domain = urlparse(start_url).netloc

	browsermobproxy_path = "/usr/local/opt/browsermobproxy/bin/browsermob-proxy"

	options = {
		'port': 9090,
	}

	server = Server(browsermobproxy_path,options)
	server.start()
	proxy = server.create_proxy()

	if webdriver_type ==  "firefox":
		profile  = webdriver.FirefoxProfile()
		profile.set_proxy(proxy.selenium_proxy())
		driver = webdriver.Firefox(firefox_profile=profile)
	elif webdriver_type == "phantomjs":
		service_args = ['--proxy=localhost:9091','--proxy-type=http',]
		driver = webdriver.PhantomJS(service_args=service_args)
		driver.set_window_size(1440, 1024)
	else:
		profile  = webdriver.FirefoxProfile()
		profile.set_proxy(proxy.selenium_proxy())
		driver = webdriver.Firefox(firefox_profile=profile)

	driver.get(start_url)

	if not cookies_file is None:
		with open(cookies_file, 'rb') as fp:
		    cookies = json.load(fp)
		for cookie in cookies:
			driver.add_cookie(cookie)
		driver.refresh()

	links = driver.find_elements_by_tag_name('a')
	lenl = len(links)
	for i in range(0,lenl):
		if links[i].is_displayed():
			url = links[i].get_attribute('href')
			text = links[i].get_attribute('text')
			if url.find(allowed_domain) != -1:
				proxy.new_har('demo')
				links[i].click()
				print "%s Clicked on the link '%s' with HREF '%s'" % (Fore.BLUE+"*"+Fore.RESET,Style.BRIGHT+text+Style.RESET_ALL,Style.BRIGHT+url+Style.RESET_ALL)
				show_status_codes(proxy.har,allowed_domain)
			driver.back()
			driver.refresh()
			links = driver.find_elements_by_tag_name('a')

	driver.quit()
	server.stop()

if __name__ == '__main__':
	main(sys.argv[1:])
