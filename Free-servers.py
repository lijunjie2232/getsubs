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
        ("https://raw.githubusercontent.com/FiFier/v2rayShare/main/README.md",
         r"v2ray订阅链接[\s\S]*?(http.*?)\n"),
        (None)
    ],

    [
        ("https://raw.githubusercontent.com/mksshare/mksshare.github.io/main/README.md",
         r"```[\s]*?([\s\S]*)[\s]*?```"),
        (r"\n(.*?)\n")
    ],

]

if __name__ == '__main__':
    try:
        ### v2ray sub
        nodeList = set()

        # get sub url
        result = html_filter(
            "https://raw.githubusercontent.com/FiFier/v2rayShare/main/README.md", r"v2ray订阅链接[\s\S]*?(http.*?)\n")

        # get sub
        sub = html_filter(result[0])

        # node aggr
        nodes = set(decode(sub))
        nodes.remove('')
        nodeList = nodeList.union(nodes)

        result = html_filter(
            "https://raw.githubusercontent.com/mksshare/mksshare.github.io/main/README.md", r"```[\s]*?([\s\S]*)[\s]*?```")[0]
        result = text_filter(result, r"\n(.*?)\n")
        nodes = set(result)
        nodes.remove('')
        nodeList = nodeList.union(nodes)

        # form sub and write into file
        nodes_sub = str(encode(nodeList))
        files_v = [
            "./Free-servers",
            "./Free-servers.txt"
        ]
        for f in files_v:
            with open(f, "w") as f:
                f.write(nodes_sub)


        ### clash sub
        clash_url = html_filter(
            "https://raw.githubusercontent.com/FiFier/v2rayShare/main/README.md", r"clash订阅链接[\s\S]*?(http.*?)\n")
        # print(clash_url)
        clash = html_filter(clash_url[0])

        # write into file
        files_c = [
            "clash.yaml"
        ]
        for f in files_c:
            with open(f, "w") as f:
                f.write(clash)

    except Exception as e:
        print(e)
