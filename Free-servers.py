#!/usr/bin python3
# coding: utf-8

import requests
import re
import base64

def decode(sub:str):
    return base64.b64decode(sub).decode('utf-8').split('\n')

def encode(subs:list):
    str = ""
    for i in subs:
        if str:
            str += '\n'
        str += i
    return base64.b64encode(str.encode()).decode('utf-8')


if __name__ == '__main__':
    try:
        nodeList = set()

        # get sub url
        resp = requests.get("https://raw.githubusercontent.com/FiFier/v2rayShare/main/README.md")
        text = resp.text
        pattern = re.compile(r"v2ray订阅链接[\s\S]*?(http.*?)\n")
        result = pattern.findall(text)

        # get sub
        resp = requests.get(result[0])
        sub = resp.text

        # node aggr
        nodes = set(decode(sub))
        nodes.remove('')
        nodeList = nodeList.union(nodes)
        len(nodeList)

        # form sub
        sub1 = str(encode(nodeList))
        with open("./Free-servers", "w") as f:
            f.write(sub1)
            f.close()

    except Exception as e:
        print(e)
