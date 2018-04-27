import requests
import re
from lxml import etree
import os
import time

def get_Imageurl(url,headers):
    res = requests.get(url,headers=headers)
    pattern = '<a href="(.*?)" target="_blank">'
    image_urls = re.findall(pattern,res.text)
    return image_urls

def get_Image(url_list):

    for each in set(url_list):
        time.sleep(2)
        print('正在爬取{0}'.format(each))
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'}
        html = requests.get(each,headers=headers).text
        data = etree.HTML(html)
        page_num = data.xpath('//div[@class="pagenavi"]/a[last()-1]/span/text()')[0]
        title = data.xpath('//h2[@class="main-title"]/text()')[0]
        #这个地方有待完善。
        os.mkdir(title)
        for image_num in range(1,int(page_num)+1):
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'}
            if image_num == 1:
                headers.update({'Referer': url})
                res = requests.get(each,headers=headers)
                pattern = '<img src="(.*?)" alt="(.*?)" />'
                result = re.findall(pattern, res.text)
                for image_url, image_name in result:
                    #有待完善
                    path = 'E:\Python\SpiderItems\Spider\Spider_Mzitu'+'\\'+image_name
                    print(path)
                    res = requests.get(image_url, headers=headers)
                    with open(path+'\\'+str(image_num)+'.jpg', 'wb') as f:
                        f.write(res.content)
                        f.close()
            elif image_num == 2:
                collection_url = each+"/"+str(image_num)
                headers.update({'Referer': url})
                res = requests.get(collection_url,headers=headers)
                pattern = '<img src="(.*?)" alt="(.*?)" />'
                result = re.findall(pattern, res.text)
                for image_url, image_name in result:
                    path = 'E:\Python\SpiderItems\Spider\Spider_Mzitu' + '\\' + image_name
                    res = requests.get(image_url, headers=headers)
                    with open(path+'\\'+str(image_num)+'.jpg', 'wb') as f:
                        f.write(res.content)
                        f.close()
            else:
                collection_url = each+"/"+str(image_num)
                referer = each +"/"+str(image_num-1)
                headers.update({'Referer':referer})
                res = requests.get(collection_url,headers=headers)
                pattern = '<img src="(.*?)" alt="(.*?)" />'
                result = re.findall(pattern, res.text)
                for image_url, image_name in result:
                    path = 'E:\Python\SpiderItems\Spider\Spider_Mzitu' + '\\' + image_name
                    res = requests.get(image_url, headers=headers)
                    with open(path+'\\'+str(image_num)+'.jpg', 'wb') as f:
                        f.write(res.content)


if __name__ == '__main__':
    for i in range(1,2):
        headers = {
            'Host': 'www.mzitu.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
        }
        if i == 1:
            url = 'http://www.mzitu.com/mm/'
            url_list = get_Imageurl(url,headers)
            get_Image(url_list)
        elif i == 2:
            url = 'http://www.mzitu.com/mm/page/2/'
            headers.update({'Referer':'http://www.mzitu.com/mm/'})
            get_Imageurl(url,headers)
        else:
            url = 'http://www.mzitu.com/mm/page/{0}/'.format(i)
            referer = 'http://www.mzitu.com/mm/page/{0}/'.format(i-1)
            headers.update({'Referer':referer})
            get_Imageurl(url,headers)
