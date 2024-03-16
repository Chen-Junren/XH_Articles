#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import os

import bs4
import requests
from rich.progress import track


# In[1]:


# In[2]:

def GET():
    def get_data(data_url='', header=None, info="", attr=None):
        response = requests.get(url=data_url, headers=header)
        analysis = bs4.BeautifulSoup(response.text, 'html.parser')
        print(response)
        # print(analysis)
        return analysis.find_all(info, attrs=attr)

    # In[5]:

    # In[3]:

    header = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.109 '
                      'Safari/537.36 CrKey/1.54.248666 Edg/122.0.0.0'}

    # In[25]:

    li = []

    for x in track(range(1, 44), description='Downloading data...'):
        try:
            responsed = requests.get(f"https://xhsc.sipedu.org/xyxw/jsxw_{x}/", headers=header)
            anal = bs4.BeautifulSoup(responsed.text, 'html.parser')
            # print(analysis)
            get = anal.find_all('li')

            for i in get:
                temp = i.find('a', {'target': "_blank"})
                dat1 = i.find('span', {'class': 'date'})
                if (temp is not None and dat1 is not None) and ("融合课程" not in temp and "网站地图" not in temp):
                    url = temp.get('href')
                    li.append([dat1.string, temp.string, f'https://xhsc.sipedu.org{url}'])
        except Exception as e:
            # print(get,repr(e))
            with open('error.txt', 'w', encoding='utf-8') as l:
                l.write(f"{repr(e)}\n{repr(anal)}")
                print("exit with code -1")
            break

    # In[26]:

    # In[27]:

    li = [[x[0], x[1].strip('\r\n'), x[2]] for x in li]
    li = [[x[0], x[1].strip('        '), x[2]] for x in li]
    li = [[x[0], x[1].strip('\r\n'), x[2]] for x in li]
    li = [[x[0], x[1].strip('\u3000'), x[2]] for x in li]
    li = [[x[0], x[1].replace('\u3000', ' '), x[2]] for x in li]
    li_1 = {li.index(x): {'date': x[0], 'title': x[1], 'url': x[2]} for x in li}

    # In[29]:

    with open('./articles_xhsc.json', mode='w+', encoding='utf-8') as t:
        t.write(json.dumps(li_1, indent=4, ensure_ascii=False))


# ### Below: Get each post

# In[30]:
def URL():
    header = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.109 '
                      'Safari/537.36 CrKey/1.54.248666 Edg/122.0.0.0'}

    with open('.//articles_xhsc.json', 'r', encoding='utf-8') as d:
        js = json.loads(d.read())

    # In[31]:

    if not os.path.exists("./article_xhsc"):
        os.mkdir('./article_xhsc')

    # In[31]:

    # In[32]:

    def get_article(json_li, headers):
        try:
            for x in track(json_li, description="Processing url..."):
                date = js.get(x).get("date")
                if not os.path.exists(f"./article_xhsc/{date}.html"):
                    res = requests.get(js.get(x).get("url"), headers=headers)
                    ana = bs4.BeautifulSoup(res.text, 'html.parser')
                    text = ana.find_all('div', attrs={'class': 'conTxt'})[0]
                    img_li = text.find_all('img')
                    text = str(text)
                    for r in img_li:
                        text = text.replace(f"{r['src']}", f"https://xhsc.sipedu.org{r['src']}")

                    with open(f"./article_xhsc/{date}.html", "w+", encoding='utf-8') as f:
                        f.write(str(text))
                else:
                    continue
        except Exception as e:
            print(f'Error:{repr(e)}\n\nData acquired: {ana}')

    get_article(js, header)

if __name__ == '__main__':
    GET()
    URL()