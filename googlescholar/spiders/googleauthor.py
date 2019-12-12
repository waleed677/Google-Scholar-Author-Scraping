# -*- coding: utf-8 -*-
import scrapy
import logging
from googlescholar.items import GooglescholarItem
import urllib, socket, time, random
from scrapy.http import Request
from scrapy.http.cookies import CookieJar
import csv

class GoogleauthorSpider(scrapy.Spider):
	name = 'googleauthor'
	
	allowed_domains = ['scholar.google.com']
	#start_urls = ['https://scholar.google.com/citations?view_op=search_authors&mauthors=machine+learning']
	#handle_httpstatus_list = [302]
	
	
	def __init__(self):
		self.timepointer = int(time.clock())
		self.cnt = 0
		self.years = []
		self.start_urls = []
		self.fields =[]
		filepath = 'fields.txt'
		with open(filepath) as fp:
			 for line in fp:
				 field = line.strip()
				 field = field.replace(' ','+')
				 url = 'https://scholar.google.com/citations?view_op=search_authors&mauthors=' + field
				 self.start_urls.append(url)
			
	# parse is function to extract and parsed data
	def parse(self,response):
		cookieJar = response.meta.setdefault('cookie_jar',CookieJar())
		cookieJar.extract_cookies(response, response.request)
		for author_sel in response.xpath('//div[@class="gsc_1usr"]'):
			#if total !=3:
				#total=total+1
			link = author_sel.xpath(".//h3[@class='gs_ai_name']/a/@href").extract_first()
			url = response.urljoin(link)
			yield scrapy.Request(url,callback=self.parse_url_to_crawl)
		
		if response.xpath("//button[@class='gs_btnPR gs_in_ib gs_btn_half gs_btn_lsb gs_btn_srt gsc_pgn_pnx']/@onclick").extract_first() != "":
			next_page_url= response.xpath("//button[@class='gs_btnPR gs_in_ib gs_btn_half gs_btn_lsb gs_btn_srt gsc_pgn_pnx']/@onclick").extract_first().replace("\\x3d","=").replace("\\x26","?")

		count=next_page_url.count('?')
		after_author = next_page_url.split("?")[count-1]
		start = next_page_url.split("?")[count]
		join_url = "&"+after_author+"&"+start
		#url = "https://scholar.google.com/citations?view_op=search_authors&mauthors=machine+learning"+join_url
		url = response.url+join_url
		logging.info("Url %s",url)
		if start is not None:
			yield scrapy.Request(url)
		
		

	def parse_url_to_crawl(self,response):
		url = response.url
		idx = url.find("user")
		user = url[idx+5:idx+17]
		yield scrapy.Request(url+'&cstart=0&pagesize=100',callback=self.parse_profile_content,meta={'offset':0,'user':user})


	# get_user_profile_data
	def parse_profile_content(self,response):
		items=[]
		#url = response.url
		#idx = url.find("user")

		
		total_articles = response.meta.get("total_articles", 0)
		tyear = response.meta.get("years", 0)
		self.years = response.meta.get("allyears",[])


		offset = response.meta['offset']
		user = response.meta['user']

		if response.xpath("//div[@id='gsc_prf_in']/text()").extract_first() !="":
			name = response.xpath("//div[@id='gsc_prf_in']/text()").extract_first()
		
		if response.xpath("//div[@id='gsc_prf_ivh']/text()").extract_first() != "":
			email = response.xpath("//div[@id='gsc_prf_ivh']/text()").extract_first()

		if response.xpath("//div[@class='gsc_prf_il']/text()[1]").extract_first() != "":
			position1 = response.xpath("//div[@class='gsc_prf_il']/text()[1]").extract_first()
			position2 = response.xpath("//div[@class='gsc_prf_il']/a/text()").extract_first()
			position3 = response.xpath("//div[@class='gsc_prf_il']/text()[2]").extract_first()
			positions = str(position1)+' '+str(position2)+' '+str(position3)
		
		if response.xpath("//div[@id='gsc_prf_int']/a/text()").extract() !="":
			tags= response.xpath("//div[@id='gsc_prf_int']/a/text()").extract()
		
		if response.xpath("//tr/td[@class='gsc_rsb_std']/text()").extract() != "":
			publication_data = response.xpath("//tr/td[@class='gsc_rsb_std']/text()").extract()
			citation= publication_data[0]
			citation_2014= publication_data[1]
			hindex= publication_data[2]
			hindex_2014= publication_data[3]
			iindex= publication_data[4]
			iindex_2014= publication_data[5]
		else:
			publication_data =""


		tmp = response.xpath('//tbody[@id="gsc_a_b"]/tr[@class="gsc_a_tr"]/td[@class="gsc_a_t"]/a/text()').extract()
		year =  response.xpath("//span[@class='gsc_a_h gsc_a_hc gs_ibl']/text()").extract()

		total_articles += len(tmp)
		tyear += len(year)
		self.years.extend(year)
		
		item = GooglescholarItem()	
		
		
		if tmp:
			offset += 100
			yield scrapy.Request("https://scholar.google.com/citations?hl=en&user={user}&cstart={offset}&pagesize=100".format(offset=offset, user=user),callback=self.parse_profile_content, meta={'offset': offset, 'user': user,'total_articles': total_articles,'years':tyear,'allyears':self.years})

		else:
			item['name'] = name
			item['email'] = email
			item['position']=positions
			item['tags'] = tags
			item['citation']= int(citation)
			item['citation_2014']= int(citation_2014)
			item['hindex']= int(hindex)
			item['hindex_2014']= int(hindex_2014)
			item['iindex']= int(iindex)
			item['iindex_2014']= int(iindex_2014)
			item['totaltitle'] = int(total_articles)
			item['maxyear'] = max(self.years)
			item['minyear'] = min(self.years)
			items.append(item)
			self.years = []
			yield item
			

	
	
		
		