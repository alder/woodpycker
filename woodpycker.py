#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys,os
from urlparse import urlparse
from selenium import webdriver
from browsermobproxy import Server
from colorama import init, Fore, Style


def show_status_codes(har,allowed_domain):
	for entry in har['log']['entries']:
		domain = urlparse(entry['request']['url'])
		domain = domain.netloc
		if domain.find(allowed_domain) != -1:
			if entry['response']['status'] >= 200 and entry['response']['status'] < 300:
				status = Fore.GREEN + str(entry['response']['status']) + " - " + entry['response']['statusText'] + Fore.RESET
			if entry['response']['status'] >= 400 and entry['response']['status'] < 500:
				status = Fore.YELLOW + str(entry['response']['status']) + " - " + entry['response']['statusText'] + Fore.RESET
			if entry['response']['status'] >= 500 and entry['response']['status'] < 600:
				status = Fore.RED + str(entry['response']['status']) + " - " + entry['response']['statusText'] + Fore.RESET
			print "-- %s [%s]" % (entry['request']['url'],status)


def main():
	init()
	if len(sys.argv) >= 2:
	    start_url = sys.argv[1]
	else:
	    print "You must specify page URL!"
	    sys.exit()

	allowed_domain = urlparse(start_url).netloc

	browsermobproxy_path = "/usr/local/opt/browsermobproxy/bin/browsermob-proxy"

	options = {
		'port': 9090,

	}

	server = Server(browsermobproxy_path,options)
	server.start()
	proxy = server.create_proxy()

	profile  = webdriver.FirefoxProfile()
	profile.set_proxy(proxy.selenium_proxy())
	driver = webdriver.Firefox(firefox_profile=profile)

	driver.get(start_url)

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
	main()
