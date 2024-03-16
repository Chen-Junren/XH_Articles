#!/usr/bin/env python
# coding: utf-8

# In[2]:


import json
import os

import bs4
import requests
from rich.progress import track


# In[1]:


# In[8]:
def Get() -> None:
    def get_data(data_url='', header=None, info="", attr=None):
        response = requests.get(url=data_url, headers=header)
        analysis = bs4.BeautifulSoup(response.text, 'html.parser')
        #print(response)
        # print(analysis)
        return analysis.find_all(info, attrs=attr)

    # In[5]:

    # In[9]:

    header = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.109 '
                      'Safari/537.36 CrKey/1.54.248666 Edg/122.0.0.0'}
    # In[10]:

    li = []

    for x in track(range(1, 42), description='Downloading data...'):
        responsed = requests.get(f"https://xhsy.sipedu.org/xyxw/jsxw_{x}/", headers=header)
        anal = bs4.BeautifulSoup(responsed.text, 'html.parser')
        # print(analysis)
        get = anal.find_all('li')

        for i in get:
            temp = i.find('a', {'target': "_blank"})
            dat1 = i.find('span', {'class': 'date'})
            if (temp is not None) and ("融合课程" not in temp and "网站地图" not in temp):
                url = temp.get('href')
                try:
                    li.append([dat1.string, temp.string, f'https://xhsy.sipedu.org{url}'])
                except Exception:
                    print(i)
                    break

    # In[11]:

    li = [[x[0], x[1].strip('\r\n'), x[2]] for x in li]
    li = [[x[0], x[1].strip('        '), x[2]] for x in li]
    li = [[x[0], x[1].strip('\r\n'), x[2]] for x in li]
    li = [[x[0], x[1].strip('\u3000'), x[2]] for x in li]
    li = [[x[0], x[1].replace('\u3000', ' '), x[2]] for x in li]
    li_1 = {li.index(x): {'date': x[0], 'title': x[1], 'url': x[2]} for x in li}

    # In[13]:

    with open('./articles_xhsy.json', mode='w+', encoding='utf-8') as t:
        t.write(json.dumps(li_1, indent=4, ensure_ascii=False))


# ### Below: Get each post

# In[15]:

def URL() -> None:
    with open('.//articles_xhsy.json', 'r', encoding='utf-8') as d:
        js = json.loads(d.read())

    # In[16]:

    if not os.path.exists("./article_xhsy"):
        os.mkdir('./article_xhsy')

    # In[16]:

    header = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.109 '
                      'Safari/537.36 CrKey/1.54.248666 Edg/122.0.0.0'}

    # In[22]:

    def get_article(json_li, headers):
        try:
            for x in track(json_li, description="Processing url..."):
                date = js.get(x).get("date")
                if not os.path.exists(f"./article_xhsy/{date}.html"):
                    res = requests.get(js.get(x).get("url"), headers=headers)
                    ana = bs4.BeautifulSoup(res.text, 'html.parser')
                    text = ana.find_all('div', attrs={'class': 'conTxt'})[0]
                    img_li = text.find_all('img')
                    text = str(text)
                    for r in img_li:
                        text = text.replace(f"{r['src']}", f"https://xhsy.sipedu.org{r['src']}")

                    with open(f"./article_xhsy/{date}.html", "w+", encoding='utf-8') as f:
                        f.write(str(text))
                else:
                    continue
        except Exception as e:
            print(f'Error:{repr(e)}\n\nData acquired: {ana}')

    get_article(js, header)

    # #### After 2024.3.14 22:55
    # - Put the title into the html files

    # In[ ]:

    # In[ ]:

if __name__ == '__main__':
    Get()
    URL()
