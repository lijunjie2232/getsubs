#!/usr/bin python3
# coding: utf-8

import requests
import re
import base64


def decode(sub: str):
    return base64.b64decode(sub).decode('utf-8').split('\n')


def encode(subs: list):
    str = ""
    for i in subs:
        if str:
            str += '\n'
        str += i
    return base64.b64encode(str.encode()).decode('utf-8')


def html_filter(url: str, rule: str = None):
    resp = requests.get(url)
    resp.encoding = "utf-8"
    if rule == None:
        try:
            return resp.text
        except Exception as e:
            print(e)
    try:
        text = requests.get(url).text
        # print(text)
        pattern = re.compile(rule)
        result = pattern.findall(text)
        return result
    except Exception as e:
        print(e)


def text_filter(text: str, rule: str):
    try:
        pattern = re.compile(rule)
        result = pattern.findall(text)
        return result
    except Exception as e:
        print(e)


vsub_data = [
    [
        "https://raw.githubusercontent.com/FiFier/v2rayShare/main/README.md",
        ('h', r"v2ray订阅链接[\s\S]*?(http.*?)\n", 0),
        ('h', None, -1),
        1
    ],
    [
        "https://raw.githubusercontent.com/mksshare/mksshare.github.io/main/README.md",
        ('h', r"```[\s]*?([\s\S]*)[\s]*?```" , 0),
        ('t', r"\n(.*?)\n", -1),
        0
    ],

]
csub_data = [
    
]

if __name__ == '__main__':
    try:
        ### v2ray sub
        nodeList = set()
        
        result = None
        for data in vsub_data:
            result = data[0]
            for action in data[1:-1]:
                if action[0] == 'h':
                    if action[-1] == -1:
                        result = html_filter(result, action[1])
                    else:
                        result = html_filter(result, action[1])[action[-1]]
                elif action[0] == "t":
                    if action[-1] == -1:
                        result = text_filter(result, action[1])
                    else:
                        result = text_filter(result, action[1])[action[-1]]
                # print(result)
            if result:
                if data[-1]:
                    nodes = set(decode(result))
                else:
                    nodes = set(result)
            
                if '' in nodes:
                    nodes.remove('')
                nodeList = nodeList.union(nodes)
                # print(data[0], '\nnums: ' , len(nodes))
            else:
                pass

        # form sub and write into file
        nodes_sub = str(encode(nodeList))
        files_v = [
            "./Free-servers",
            "./Free-servers.txt"
        ]
        for f in files_v:
            with open(f, "w", encoding='utf-8') as f:
                f.write(nodes_sub)
            
        ### clash sub
        clash_url = html_filter(
            "https://raw.githubusercontent.com/FiFier/v2rayShare/main/README.md", r"clash订阅链接[\s\S]*?(http.*?)\n")
        # print(clash_url)
        clash = html_filter(clash_url[0])
        # print(clash)

        # write into file
        files_c = [
            "clash.yaml"
        ]
        for f in files_c:
            with open(f, "w", encoding='utf-8') as f:
                f.write(clash)

    except Exception as e:
        print(repr(e))
