#!/usr/bin/python
import urllib2,os,re,time,sys
from bs4 import BeautifulSoup

req_header = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6)Gecko/20091201 Firefox/3.5.6',
              'Referer':None
}

queue = []
popped = []
seeds = ['http://www.ccs.neu.edu']
output = []
robots_me=[]

def init():
       global queue
       queue = seeds
       global robots_me
       #read robots.txt
       robot_url='http://www.ccs.neu.edu/robots.txt'
       req=urllib2.Request(robot_url,None,req_header)
       robots=urllib2.urlopen(req).readlines()
       for i in range(0,len(robots)):
              if robots[i]=='User-agent: *\n':
	             robots_me=robots[i+1:]
       robots_me=map(lambda x:x[10:-1],robots_me)
       print 'I will not crawl:'
       for line in robots_me:
              print line
       
def grab_url():
       global popped
       if len(queue) > 0:
              print 'url: ',queue[0]
              popped.append(queue[0])
              print 'popped length: ',len(popped)
              return queue.pop(0)
       else:
              print 'queue empty!'
              return 0

def respect_robots(url):
       for line in robots_me:
              if url.find(line[:-1]) != -1:
                     return 0
       return 1

def record(url):
       global output
       output.append(url)
       print 'output length: ',len(output)
       
       
def getsite(url):
       #print 'queue length: ',len(queue)
       if url == 0:
              print 'terminating program...'
              sys.exit()
              
       if respect_robots(url) == 0:
              return 0
       
       try:
              req = urllib2.Request(url,None,req_header)
              site = urllib2.urlopen(req)
       except:
	      return 0
       if 'application/pdf'==site.headers.getheaders('Content-Type')[0] or 'text/html' in site.headers.getheaders('Content-Type')[0]:
              record(url)
       return site.read()

def check_added(url,L):
       if url in L:
              return 1
       else:
              return 0
       
def parse(content):
       if content != 0:
              soup = BeautifulSoup(content)
              #time.sleep(5)
              urls=soup.find_all('a')
              for url in urls:
                     try:
			    url=url['href']
		     except:
			    continue
                     if not check_added(url,queue) and\
                        not check_added(url,popped):
                            queue.append(url)
              print 'queue length: ',len(queue)

def generate_file():
       f=open('output.txt','a')
       for out in output:
              f.write(out+'\n')
       f.close()
                     
if __name__ == "__main__":
       init()
       while len(output) < 100:
              parse(getsite(grab_url()))
              time.sleep(5)
       generate_file()
       print 'done.'
       
