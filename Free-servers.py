#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
import re


# In[18]:


resp = requests.get("https://raw.githubusercontent.com/Pawdroid/Free-servers/main/README.md")
html = resp.text
html


# In[19]:


pattern = re.compile(r"<h5>本次节点订阅地址：(.*?)</h5>")
result = pattern.findall(html)
result


# In[20]:


resp = requests.get(result[0])
sub = resp.text
sub


# In[21]:


f = open("Free-servers", "w")
f.write(sub)
f.close()


# In[ ]:




