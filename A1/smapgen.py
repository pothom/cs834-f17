import os	
import time
import sys
import argparse

parser = argparse.ArgumentParser('smapgen')
parser.add_argument('path',help='Path to the directory that will be used to generate sitemap')
parser.add_argument('--path_to_gen','-p',help='Path where the generated sitemap.xml will be put [default= Current directory]',default='./')
args = parser.parse_args();
p_to_gen = args.path_to_gen+'sitemap.xml';
root_dir = args.path

out=''
out+='<?xml version="1.0" encoding="UTF-8"?>\n'
out+='<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for root,dirs,files in os.walk(root_dir):
	for f in files:
		loc = root+'/'+f
		url = root.replace(root_dir,"http://www.example.com")
		out+='  <url>\n'
		out+= '    <loc>'+url+'/'+f+'</loc>\n'
		out+= '    <lastmod>'+time.strftime("%Y-%m-%d",time.localtime(os.path.getmtime(loc)))+'</lastmod>\n'
		out+= '  </url>\n'
out+= '</urlset>'

with open(p_to_gen,'w') as f:
	f.write(out)
	f.close()