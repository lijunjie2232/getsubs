#!/usr/bin python3
# coding: utf-8

import requests
import re

resp = requests.get("https://raw.githubusercontent.com/Pawdroid/Free-servers/main/README.md")
html = resp.text
pattern = re.compile(r"<h5>本次节点订阅地址：(.*?)</h5>")
result = pattern.findall(html)

resp = requests.get(result[0])
sub = resp.text

f = open("./Free-servers", "w")
f.write(sub)
f.close()

