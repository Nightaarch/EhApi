import requests
import re
import gzip

import Config
from Config import config

URL_PATTERN = r"https://(ex|e-)hentai\.org/g/\d+/[\da-f]+/?(\?p=\d+)?"
payloads = {"f_search": None}

def GetSearchPage(Payloads,SaveName):
    payloads["f_search"] = Payloads
    SaveName = str(SaveName)
    response = requests.get(config.endpoint,params=payloads,headers=config.headers,cookies=config.cookie)
    with open('%s'%SaveName, 'w',encoding="utf-8") as f:
        f.write(response.text)


def GetEHTitle(PAGEFILE):
    page = open(PAGEFILE, "r", encoding ='utf-8')
    htmldata = page.read().splitlines()[3].lstrip()
    htmldata = htmldata.lstrip("<title>").rstrip(" - ExHentai.org</title>")
    page.close()
    return htmldata


def GetPageLink(HTMLFILE):
    HTMLFILE = str(HTMLFILE)
    resp = open(HTMLFILE,"r",encoding = 'utf-8')
    content = resp.read()
    URL = re.finditer(URL_PATTERN,content)
    resp.close()
    urllist = []
    for match in URL:
        urllist.append(match.group())
    return list(set(urllist))


def GetSearchResult(Payloads):
    GetSearchPage(str(Payloads),"sresp.txt")
    LinkList = GetPageLink("sresp.txt")
    Result = {}
    for Links in LinkList:
        resp = requests.get(Links,headers=config.headers,cookies=config.cookie,)
        with open('lresp.txt','w',encoding="utf-8") as f:
            f.write(resp.text)
        Title = GetEHTitle("lresp.txt")
        Result[Title] = Links
    return Result


def GetPageContent(URL,SaveName="resp.txt"):
    resp = requests.get(URL, headers=config.headers, cookies=config.cookie)
    with open(SaveName, 'w', encoding="utf-8") as f:
        f.write(resp.text)


if __name__ == "__main__":
    print(GetSearchResult("Ibuki to asobo"))
