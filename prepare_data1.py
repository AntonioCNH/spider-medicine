from ast import parse
import urllib.request
import urllib.parse
from lxml import etree
import pymongo
import re
import json

class XYWY_spider:
    def __init__(self):
        self.conn = pymongo.MongoClient()
        self.db = self.conn['medical_new_1']
        self.col = self.db['data']
    
    def get_html(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/51.0.2704.63 Safari/537.36'}
        req = urllib.request.Request(url=url, headers=headers)
        res = urllib.request.urlopen(req)
        html = res.read().decode('gbk')
        return html

    def spider_main(self):
        init_location = 'http://jib.xywy.com/html/neike.html'
        init_html = self.get_html(init_location)
       # print(init_html)
        parse_html = etree.HTML(init_html)
       # print(parse_html)
        name_xpath = '//ul[@class="jbk-sed-menu bor pa none f12"]//a/text()'
        name_list = parse_html.xpath(name_xpath)
        speical = [4,6,10,11,13,16,17]
      #  print(len(name_list))

        #pa_html = etree.HTML(name_html)
        location_xpath = '//ul[@class="jbk-sed-menu bor pa none f12"]//a/@href'
        location_list = parse_html.xpath(location_xpath)
        print(len(location_list))
        head = 'http://jib.xywy.com'
        i = 0
        for item in location_list:
            url = head + item
            self.info_spider(url, i, name_list)
            i = i + 1

        for k in speical:
            add1 = '//div[@class="jblist-nav fl"]/ul/li[%s]/a/@href'%k
            add2 = '//div[@class="jblist-nav fl"]/ul/li[%s]/a/text()'%k
            url = parse_html.xpath(add1)
            name = parse_html.xpath(add2)
            self.info_spider('http://jib.xywy.com' + url[0], 0, name)

        return

    def info_spider(self, url, i, name_list):
        html = self.get_html(url)
        parse_html = etree.HTML(html)
       # medical_name_xpath = '//ul[@class="ks-ill-list clearfix mt10"]//a/text()'
       # medical_name_list = parse_html.xpath(medical_name_xpath)
       # print(len(medical_name_list))
        location_xpath = '//ul[@class="ks-ill-list clearfix mt10"]//a/@href'
        location_list = parse_html.xpath(location_xpath)
        print(len(location_list))
        for item in location_list:
            try:
                #print(item)
                head = 'http://jib.xywy.com'
                medical_url = head + item
                print(medical_url)
                medical_html = self.get_html(medical_url)
                medical_parse_html = etree.HTML(medical_html)
                basicinfo_xpath = '//ul[@class="dep-nav f14 clearfix"]/li[2]/a/@href'
                basicinfo = medical_parse_html.xpath(basicinfo_xpath)
            # basicinfo_url = head + basicinfo
              #  print(basicinfo)
                symptom_xpath = '//div[@class="jib-navbar fl bor pr"]/div[2]/ul/li/a/@href'
                symptom = medical_parse_html.xpath(symptom_xpath)
              #  print(symptom)
                name_xpath = '//div[@class="jb-name fYaHei gre"]/text()'
                name = medical_parse_html.xpath(name_xpath)
                data = {}
                data['cure_department'] = name_list[i]
                print(data['cure_department'])
                data['url'] = medical_url
                data['name'] = name
                print(data['name'])
                data['symptoms'] = self.symptom_spider(head + symptom[0])
                data['basicinfo'] = self.basicinfo_spider(head + basicinfo[0])
                self.col.insert_one(data)
            except Exception as e:
                print(e, item)
        return

    def symptom_spider(self, url):
        print('symptom_spider:',url)
        html = self.get_html(url)
        parse_html = etree.HTML(html, parser=etree.HTMLParser(encoding='utf-8'))
        xpath = '//div[@class="jib-articl fr f14 jib-lh-articl"]//p/text()'
        return parse_html.xpath(xpath)

    def basicinfo_spider(self, url):
        print('basicinfo_spider:',url)
        html = self.get_html(url)
        parse_html = etree.HTML(html)
        basic_xpath = '//div[@class="jib-articl-con jib-lh-articl"]//p/text()'
        data = {}
        data['basic_data'] = parse_html.xpath(basic_xpath)
        get_prob_xpath = '//div[@class="jib-articl fr f14 "]/div[2]/p[2]/span[2]/text()'
        data['get_prob'] = parse_html.xpath(get_prob_xpath)
        #print(data['get_prob'])
        return data

class HDF_spider:
    def __init__(self):
        self.conn = pymongo.MongoClient()
        self.db = self.conn['medical_new_2']
        self.col = self.db['data']

    def get_html(self, url):
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/51.0.2704.63 Safari/537.36'}
        req = urllib.request.Request(url=url, headers=headers)
        res = urllib.request.urlopen(req)
        html = res.read().decode('gbk')
        return html

    def spider_main(self):
        init_location = 'https://www.haodf.com/citiao/list-jibing-xinshengerke.html?from=zhishi'
        init_html = self.get_html(init_location)
        parse_html = etree.HTML(init_html)
        name_xpath = '//div[@id="el_result_content"]/div/div[2]/div[4]//a/text()'
        name_list = parse_html.xpath(name_xpath)
        location_xpath = '//div[@id="el_result_content"]/div/div[2]/div[4]//a/@href'
        location_list = parse_html.xpath(location_xpath)
        head = 'https://www.haodf.com'
        i = 0
        for item in location_list:
            data = {}
            data['cure_department'] = '新生儿科'
            data['name'] = name_list[i]
            url = head + item
            head_html = self.get_html(url)
            head_parse_html = etree.HTML(head_html)
            info_xpath = '//div[@class="top-banner-container"]/section[2]/a/@href'
            info_path = head_parse_html.xpath(info_xpath)
            info_url = head + info_path[0]
            data_html = self.get_html(info_url)
            data_parse_html = etree.HTML(data_html)
            data_xpath = '//div[@class="l-content js-1003"]/div//li/text()'
            symptom_data = data_parse_html.xpath(data_xpath)
            print(symptom_data)
            data['symptoms'] = symptom_data
            self.col.insert_one(data)
            i = i + 1
        return
            
class Symptom_spider:
    def __init__(self):
        self.conn = pymongo.MongoClient()
        self.db = self.conn['symptom']
        self.col = self.db['data']

    def get_html(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/51.0.2704.63 Safari/537.36'}
        req = urllib.request.Request(url=url, headers=headers)
        res = urllib.request.urlopen(req)
        html = res.read().decode('gbk')
        return html
    def spider_main(self):
        init_url = 'http://zzk.xywy.com/p/a.html'
        init_html = self.get_html(init_url)
        parse_html = etree.HTML(init_html)
        xpath = '//div[@class="fr jblist-con-zm fYaHei"]//a/@href'
        path_list = parse_html.xpath(xpath)
        for item in path_list:
            head = 'http://zzk.xywy.com'
            url = head + item
            html = self.get_html(url)
            pars_html = etree.HTML(html)
            xpath = '//div[@class="jblist-con-ear fl"]//a/@href'
            item_list = pars_html.xpath(xpath)
            for i in item_list:
                data = {}
                item_url = head + i
                item_html = self.get_html(item_url)
                item_parse_html = etree.HTML(item_html)
                item_name_xpath = '//div[@class="blood-item panel"]//a/text()'
                item_name_list = item_parse_html.xpath(item_name_xpath)
                symptom_xpath = '//div[@class="jb-name fYaHei gre"]/text()'
                symptom = item_parse_html.xpath(symptom_xpath)
                data['symptom'] = symptom
                data['name'] = item_name_list
                print(data['symptom'], data['name'])
                self.col.insert_one(data)

class Data_handle:
    def __init__(self):
        self.conn = pymongo.MongoClient()
        self.db1 = self.conn['medical_new_1']
        self.con1 = self.db1['data']
        self.db2 = self.conn['symptom']
        self.con2 = self.db2['data']
        self.db = self.conn['medical_fin']
        self.col = self.db['data']
        return 

    def data_main(self):
        pre_list = []
        list = []
        #myquery = {"cure_department" : "传染科"}
        #mydoc = self.con1.find(myquery)
        #for y in mydoc:
        #    print(y)
        i = 0
        for x in self.con2.find():
           # print(x)
         #   print(type(x['symptom']))
          #  data[x['symptom'][0]] = x['name']
            for item in x['name']:
                myquery = {"name" : item}
                mydoc = self.con1.find(myquery)
                if mydoc is None:
                    print('not find:', item)
                    continue
                for y in mydoc:
                    flag = 0
                    for z in list:
                        if z['name'] == y['name']:
                           # print(list)
                            z['symptom'].append(x['symptom'][0])
                           # print(z)
                            #print(list)
                            flag = 1
                    if flag == 0:
                        item_data = {}
                        item_data['name'] = y['name']
                        item_data['cure_department'] = y['cure_department']
                        item_data['get_prob'] = y['basicinfo']['get_prob']
                        item_data['symptom'] = ['null']
                        item_data['symptom'][0] = x['symptom'][0]
                        list.append(item_data)
                        # print('new', item_data)
                        print('new', i)
                        i = i+1
                    
                 #   if item_data in pre_list:
                 #       index = pre_list.index(item_data)
                      #  print(list[index])
                 #       list[index]['symptom'] += (x['symptom'][0])
                      #  print(list[index])
                  #  else:
                   #     pre_list.append(item_data)
                    #    print(item_data)
                     #   print(pre_list)
                     #   print(x)
                     #   data = item_data
                     #   data['symptom'] = ['null']
                     #   data['symptom'][0] = x['symptom'][0]
                     #   list.append(data)
                     #   print(pre_list)
                     #   print(list)
      
        preserve = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '%', '-', '.']
        k = 0
        for item in list:
            get_prob = item['get_prob']
            if get_prob != []:
                if '%' not in get_prob[0]:
                    print(k, item['get_prob'])
                    k = k + 1
                    item['get_prob'] = 'null'
                else:
                    i_list = []
                    for i in get_prob[0]:
                        if i not in preserve:
                            i_list.append(i)
                    for i in i_list:
                        get_prob[0] = get_prob[0].replace(i, '')
                #print(get_prob[0])
                    item['get_prob'] = get_prob[0]
                    if (len(get_prob[0].split('%'))-1) > 2:
                        tem = []
                        tem = get_prob[0].split('%')
                        item['get_prob'] = tem[0] + tem[1]
                    print(k, item['get_prob'])  
                    k = k + 1                 
        item_data = {}
        item_data['name'] = '新生儿黄疸'
        item_data['symptom'] = ['面、颈部皮肤呈浅黄色']
        item_data['cure_department'] = ['新生儿科']
        item_data['get_prob'] = 'null'
        list.append(item_data)
        item_data = {}
        item_data['name'] = '新生儿溶血'
        item_data['symptom'] = ['巩膜（眼白部分）变黄', '肤色泛黄', '贫血']
        item_data['cure_department'] = ['新生儿科']
        item_data['get_prob'] = 'null'
        list.append(item_data)
        self.col.insert_many(list)

        print(list)
        for item in self.con.find():
            print(item)
handler = XYWY_spider()
handler.spider_main()
handler = Symptom_spider()
handler.spider_main()
handle = Data_handle()
handle.data_main()

