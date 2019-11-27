# -*- coding: utf-8 -*-
import scrapy
import logging
from googlescholar.items import GooglescholarItem
import urllib, socket, time, random
from scrapy.http import Request
from scrapy.http.cookies import CookieJar

class GoogleauthorSpider(scrapy.Spider):
	name = 'googleauthor'
	
	allowed_domains = ['scholar.google.com']
	#start_urls = ['https://scholar.google.com/citations?&user=jplQac8AAAAJ']
	start_urls = ['https://scholar.google.com/citations?view_op=search_authors&mauthors=machine+learning']
	# custom_settings = {
	# 	'DEPTH_LIMIT': 1
	# }
	
	def __init__(self):
		self.timepointer = int(time.clock())
		self.cnt = 0
		self.n = 0
		self.totaltitle=0

	# parse is function to extract and parsed data
	def parse(self, response):
		total =0
		for author_sel in response.xpath('.//div[@class="gsc_1usr"]'):
			#if total !=2:
				#total=total+1
			link = author_sel.xpath(".//h3[@class='gs_ai_name']/a/@href").extract_first()
			url = response.urljoin(link)
			yield scrapy.Request(url,callback=self.parse_url_to_crawl)


	def parse_url_to_crawl(self,response):
		url = response.url
		yield scrapy.Request(url+'&cstart=0&pagesize=100',callback=self.parse_profile_content)

	# get_user_profile_data
	def parse_profile_content(self,response):
		
		url = response.url
		idx = url.find("user")
		_id = url[idx+5:idx+17]
		name = response.xpath("//div[@id='gsc_prf_in']/text()").extract()[0]
		tmp = response.xpath('//tbody[@id="gsc_a_b"]/tr[@class="gsc_a_tr"]/td[@class="gsc_a_t"]/a/text()').extract()
		item = GooglescholarItem()	
		n = len(tmp)
		titles=[]
		if tmp:
			#logging.info("N value %s",n)
			offset = 0; d = 0
			idx = url.find('cstart=')
			idx += 7
			val = int(url[idx])
			#logging.info("cstart val is = %s",val)
			while url[idx].isdigit():
				offset = offset*10 + int(url[idx])
				idx += 1
				d += 1
			self.n += len(tmp)
			titles.append(self.n)
			self.totaltitle = titles[-1]
			#logging.info('if k ander totaltitle = %s',self.n)
			logging.info('inside if URL is: %s',url[:idx-d] + str(offset+100) + '&pagesize=100')
			yield scrapy.Request(url[:idx-d] + str(offset+100) + '&pagesize=100', self.parse_profile_content)
		else:
			#logging.info('else k under start mai totaltile is:%s',self.totaltitle)
			item = GooglescholarItem()
			item['name'] = name
			item['totaltitle'] = self.totaltitle
			self.n=0
			self.totaltitle=0
			yield item
			
		# else:
		# 	item['name'] = name
		# 	yield item
		
			#logging.info('else k under last mai totaltile is:',self.totaltitle)
		#item['name'] = response.xpath("//div[@id='gsc_prf_in']/text()").extract_first()
		# item['email']= response.xpath("//div[@id='gsc_prf_ivh']/text()").extract_first()
		# if response.xpath("//div[@class='gsc_prf_il']/text()[1]").extract_first() != "":
		# 	position1 = response.xpath("//div[@class='gsc_prf_il']/text()[1]").extract_first()
		# 	position2 = response.xpath("//div[@class='gsc_prf_il']/a/text()").extract_first()
		# 	position3 = response.xpath("//div[@class='gsc_prf_il']/text()[2]").extract_first()
		# 	positions = str(position1)+' '+str(position2)+' '+str(position3)
		# item['position']=positions
		# item['tags']= response.xpath("//div[@id='gsc_prf_int']/a/text()").extract()
		# publication_data = response.xpath("//tr/td[@class='gsc_rsb_std']/text()").extract()
		# item['citation']= publication_data[0]
		# item['citation_2014']= publication_data[1]
		# item['hindex']= publication_data[2]
		# item['hindex_2014']= publication_data[3]
		# item['iindex']= publication_data[4]
		# item['iindex_2014']= publication_data[5]
			#yield item
		# request = scrapy.Request(response.url+'$start=0&pagesize=100',callback=self.parse_title_content)		
		# request.meta['name'] = name
		# yield request

	

	def parse_title_content(self,response):
		url = response.url
		logging.info('in title function')
		aname = response.meta.get('name')
		

	def serializeItem(self,response):

		logging.info('in serializeItem function')
		item = GooglescholarItem()
		item['name']=response.meta.get('aname')
		yield item
		
	
	def CrawlData(self, response):
		if response.status == 200:
			

			url = response.url
			idx = url.find("user")
			_id = url[idx+5:idx+17]

			item = GooglescholarItem()
	
			
			#item['name'] = response.xpath('//div[@id="gsc_prf_in"]/text()').extract()[0]
			tmp = response.xpath('//tbody[@id="gsc_a_b"]/tr[@class="gsc_a_tr"]/td[@class="gsc_a_t"]/a/text()').extract()
			item['pubs'] = []
			n = len(tmp)
			#if tmp:
	# 			logging.info('if call')
	# 			offset = 0; d = 0
	# 			idx = url.find('cstart=')
	# 			idx += 7
	# 			val = int(url[idx])
	# 			while url[idx].isdigit():
	# 				offset = offset*10 + int(url[idx])
	# 				idx += 1
	# 				d += 1
	# 			#cstart = url[:idx-d] + str(offset+100)+ '&pagesize=100'
	# 			#logging.info('cstart is = ',cstart)
	# 			self.n += len(tmp)
	# 			logging.info('if k ander totaltitle = ',self.n)
	# 			yield scrapy.Request(url[:idx-d] + str(offset+100) + '&pagesize=100', self.get_total_title)
			for i in range(1,n+1):
				pub = {}
				pub['title'] = \
					response.xpath('//tbody[@id="gsc_a_b"]/tr[@class="gsc_a_tr"][%d]/td[@class="gsc_a_t"]/a/text()' % i).extract()
				# pub['author'] = \
				# 	response.xpath('//tbody[@id="gsc_a_b"]/tr[@class="gsc_a_tr"][%d]/td[@class="gsc_a_t"]/div[1]/text()' % i).extract()
				# pub['venue'] = \
				# 	response.xpath('//tbody[@id="gsc_a_b"]/tr[@class="gsc_a_tr"][%d]/td[@class="gsc_a_t"]/div[2]/text()' % i).extract()
				# pub['citation'] = \
				# 	response.xpath('//tbody[@id="gsc_a_b"]/tr[@class="gsc_a_tr"][%d]/td[@class="gsc_a_c"]/a/text()' % i).extract()
				# pub['year'] = \
				# 	response.xpath('//tbody[@id="gsc_a_b"]/tr[@class="gsc_a_tr"][%d]/td[@class="gsc_a_y"]/span/text()' % i).extract()
				item['pubs'].append(pub)
				

			yield item
			
			if tmp:
				offset = 0; d = 0
				idx = url.find('cstart=')
				idx += 7
				while url[idx].isdigit():
					offset = offset*10 + int(url[idx])
					idx += 1
					d += 1
				yield Request(url[:idx-d] + str(offset+100) + '&pagesize=100', self.CrawlData)
	
	# def get_total_title(self,response):
	# 	if response.status == 200:
	# 		url = response.url
	# 		#item = GooglescholarItem()
	# 		tmp = response.xpath('//tbody[@id="gsc_a_b"]/tr[@class="gsc_a_tr"]/td[@class="gsc_a_t"]/a/text()').extract()
	# 		#self.n += len(tmp)
	# 		if tmp:
	# 			logging.info('if call')
	# 			offset = 0; d = 0
	# 			idx = url.find('cstart=')
	# 			idx += 7
	# 			val = int(url[idx])
	# 			while url[idx].isdigit():
	# 				offset = offset*10 + int(url[idx])
	# 				idx += 1
	# 				d += 1
	# 			#cstart = url[:idx-d] + str(offset+100)+ '&pagesize=100'
	# 			#logging.info('cstart is = ',cstart)
	# 			self.n += len(tmp)
	# 			logging.info('if k ander totaltitle = ',self.n)
	# 			yield scrapy.Request(url[:idx-d] + str(offset+100) + '&pagesize=100', self.get_total_title)
	# 			logging.info("final",url[:idx-d] + str(offset+100) + '&pagesize=100')
	# 		# request = Request(callback=self.get_profile_data)
	# 		# request.meta['total']=self.n
	# 		# return request
	
	
	# def get_profile_data(self,response):
	# 	totaltitle = response.meta.get('total')
	# 	logging.info('total',totaltitle)
		
			# for i in range(1,self.n):
			#  	logging.info('in loop')
			#  	pub = {}
			#  	#item['pubs'] = \
			#  		#response.xpath('//tbody[@id="gsc_a_b"]/tr[@class="gsc_a_tr"][%d]/td[@class="gsc_a_t"]/a/text()' % i).extract()
			#  	item['totaltitle']=self.n
			# yield item
			# while url[idx].isdigit():
			# 	offset = offset*10 + int(url[idx])
			# 	idx += 1
			# 	d += 1
			# logging.info('yeh chala')
			# cstart = url[:idx-d] + str(offset+100)
			# logging.info('cstart is = ',cstart)
			# yield scrapy.Request(url[:idx-d] + str(offset+100) + '&pagesize=100', self.parse_profile_content)

			#yield item
		
		
		