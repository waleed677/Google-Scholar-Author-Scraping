# Google-Scholar-Author-Scraping

-> This respository scraped the google scholar author's data using Python Scrapy Framework. I have implemented anti scraping techniques ( 302 redirects , too many requests etc) which will allow you to scrap the data without blocking the IP address.
-> It scrape all the data of author like name,postition,citations,h-index,totaltitles etc.
-> In this scraping project, i have used the xpath selector.
-> A simple and readable code.

There is one file in this repository fields.txt which contains the fields related to research. This file is used to scrape the author data related to these files so you can put fields as much as you can in this file.
In setting.py file you can change the Download_Delay to any value , but i will recommend you to make it 3-5 sec so that your IP address never gets block.

Clone this repository
use scrapy crawl googleauthor -o output.csv command to start scraping the data. This command will save the result in csv file
If you want to save the data in other formates you can use read scrapy documentation

If you want to suggest or improve this code let me know at contact@waleedarshad.com , we will discuss this.
