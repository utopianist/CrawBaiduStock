import traceback
import requests
import re
from bs4 import BeautifulSoup

def getHTML(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def getStockURL(nameurl, urllist):
    html = getHTML(nameurl)
    name = re.findall('[s][hz]\d{6}', html)
    for item in name:
        urllist.append("https://gupiao.baidu.com/stock/%s.html" %item)

def getStockInfo(urllist, fpath):
    count = 0
    for i in range(len(urllist)):
        html = getHTML(urllist[i])
        soup = BeautifulSoup(html, "html.parser")
        try:
            info = {}
            title = soup.find_all('a', attrs={'class':'bets-name'})[0]
            info.update({'股票名称': title.text.split()[0]}) #初始化股票名称
            keylist = soup.find_all('dt')
            valuelist = soup.find_all('dd')
            lenth = len(keylist)
            for i in range(lenth):
                key = keylist[i].text
                value = valuelist[i].text
                info[key] = value

            with open(fpath, 'a', encoding='utf-8') as f:
                f.write(str(info) + '\n')
                count = count + 1
                print("\r当前进度: {:.2f}%".format(count * 100 / len(urllist)), end="")

        except:
            count = count + 1
            print("\r当前进度: {:.2f}%".format(count * 100 / len(urllist)), end="")
            continue


def main():
    urllist = []
    nameurl = "http://quote.eastmoney.com/stocklist.html"
    output_file = 'D:/BaiduStockInfo.txt'
    getStockURL(nameurl, urllist)
    getStockInfo(urllist, output_file)

main()