woodpycker
==========

A small utility for clicking on links of the Web page and display HTTP response statuses.

Requirements:

 * Python 2.6.x and above
 * selenium 2.44.0 (Python bindings for Selenium)
 * [BrowserMob Proxy](http://bmp.lightbody.net/)
 * [browsermob-proxy-py](https://github.com/AutomatedTester/browsermob-proxy-py)
 * colorama 0.3.2 and above
 * [PhantomJS](http://phantomjs.org/)

How to run:
```bash
# python woodpycker.py -u <page_url>
```
or run
```bash
# python woodpycker.py -h
```
for list of all parameters.

*Note:* I've installed BrowserMob Proxy to /usr/local/opt/browsermobproxy/. You can install it to this location or change browsermobproxy_path in code.

Example:

![woodpycker demo screenshot](https://cloud.githubusercontent.com/assets/199887/5436457/2a6142bc-846f-11e4-81b0-0e6a9c41bb06.png "woodpycker demo screenshot")
