#-*- coding=utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from flask import Flask, render_template, redirect
from flask import request
from flask.ext.bootstrap import Bootstrap
from bs4 import BeautifulSoup
from urlparse import urlparse
#import urllib2
import featch_source
app = Flask(__name__)
bootstrap = Bootstrap(app)

last_url_domain = ''

def url_subs(base,html):
    soup = BeautifulSoup(html, "lxml")
    o = urlparse(base)
    base = o.netloc
    base = o.scheme + "://" + base
    if base == 'https://' or base == 'http://':
        base = 'https://www.google.com'
    base = base[:-1] if base.endswith('/') else base
    print 'url_sub base',base
    last_url_domain = base
    
    for a in soup.findAll('a'):
        #print a
        if a.has_attr('href'):
            if a['href'].startswith('/'):
                a['href'] = base + a['href']

    for img in soup.find_all('img'):
        #print img
        if img.has_attr('src'):
            if img['src'].startswith('/'):
                img['src'] = base + img['src']
        
    return str(soup)

def url_decorates(html):
    soup = BeautifulSoup(html, "lxml")
    for a in soup.findAll('a'):
        #print a
        if a.has_attr('href'):
            a['href'] = decorate_url(a['href'])
                
    return str(soup)


@app.route('/')
def index():
    searchword = request.args.get('url', '')
    print 'this request url',request.url
    print 'search word raw=',searchword
    searchword = searchword.replace('<!>','&')
    print 'request URL param=',searchword
    base2 = 'https://www.google.com/search?newwindow=1&q=sample'
    #base = 'https://www.google.com?lang=en'
    
    if searchword != '':
        base2 = searchword
    title,source = featch_source.get(base2)
    source = url_subs(base2,source)
    source = url_decorates(source)
    #response = urllib2.urlopen(base2)
    #source = response.read()
    #source = url_subs(base,source)
    #source = source.encode('utf-8')
    return source
    
@app.route('/<url>')
def user(url):
    #title,source = featch_source.get(url)
    original_url = request.url
    base_url = request.base_url
    original_url = original_url.replace(base_url,'')
    print 'orignal url',original_url
    if original_url.startswith('http'):
        print 'direct http'
        return redirect("?url="+original_url)
    else:
        while original_url.startswith('/'):
            original_url = original_url[1:].strip()
        while original_url.startswith('?'):
            original_url = original_url[1:].strip()
        while original_url.startswith('/'):
            original_url = original_url[1:].strip()

        prev_url = request.referrer
        o = urlparse(prev_url)
        print 'o=',o
        if o.params == '':
            last_url_domain = 'https://www.google.com/search?'
        else:
            print 'o params:',o.params
        full = last_url_domain  +  original_url.strip()
        full = full.replace('//','/')
        full = full.replace('&','<!>')
        return redirect("?url="+full)
    #return redirect("?url="+url, code=302)
    #return render_template('user.html',name=name)

def decorate_url(url):
    if url.startswith('http'):
        full = url
        full = full.replace('//','/')
        full = full.replace('&','<!>')
        #base_url = request.base_url
        #full = base_url + '/' + full
        if full.find('https://') > 0 or full.find('http://') > 0:
            decorated = "?url=" + full
        else:
            full = full.replace('http:/','http://')
            full = full.replace('https:/','https://')
            decorated = "?url=" + full
        return decorated
    else:
        return url
    
    
if __name__ == '__main__':
    app.run(debug=True,port=5053)   