from bs4 import BeautifulSoup
from urlparse import urljoin
import argparse
import requests
from time import sleep
import os

def crawl(depth,s_url):
	i = 1
	file_num = 0
	s_url = s_url.strip()
	print 'URL to start crawling:',s_url
	print 'Maximum depth:',depth
	urls = [s_url]
	while i<=depth:
		deeper_links = list()
		for url in urls:
			if url not in checked_urls:
				try:
					# Request the link from the Internet and set a timeout to prevent
					# hanging
					request = requests.get(url,stream=True,timeout=1)
					# Will only parse html files, skips any other format
					if( 'text/html' not in request.headers['Content-Type'] ):
						print 'Skipping ',url
						continue
					print 'Crawling ',url,
				except :
					continue
				# Check if link is valid or not
				if(request.status_code==200):
					checked_urls.add(url)
					print ' URL OK'
				else:
					print ' URL NOT OK'
					continue
				file_num +=1 
				with open(path+'/'+str(file_num)+'.html','w') as file:
					file.write(request.text.encode('utf-8'))
					file.close()
				soup = BeautifulSoup(request.text,'html.parser')
				# Retrieve the links in the html file
				links = soup.find_all('a')
				for link in links:
					new_link = link.get('href')
					if  new_link :
						new_link = new_link.strip()
						# Make link absolute if needed
						new_link = urljoin(url,new_link)
						# If link not crawled yet add to pending links
						if new_link not in checked_urls:
							deeper_links.append(new_link)
			# Wait 5 seconds before downloading the next html file
			sleep(5)
		print len(deeper_links),'links for next depth'
		urls = deeper_links
		print 'Finished depth ',i
		i=i+1

# Set the command line arguments 
parser = argparse.ArgumentParser('Crawler Parser')
parser.add_argument('--url','-u',help='The url to start crawling from [default= http://www.cs.odu.edu/~mln/ ',default='http://www.cs.odu.edu/~mln/')
parser.add_argument('--depth','-d',help='The crawl depth [default= 5]',default=5,type=int)
parser.add_argument('--path','-p',help='The path where the crawl directory will be created to put the downloaded files [default= current directory]',default='.')
args = parser.parse_args();
depth = args.depth
s_url = args.url
path = os.path.abspath(args.path)+'/crawl'
if not os.path.exists(path):
    os.makedirs(path)
print 'Files will be downloaded at',path
# A set of all previously met links 
checked_urls = set()
crawl(depth,s_url)
print 'Crawler finished, you can find the downloaded files at',path