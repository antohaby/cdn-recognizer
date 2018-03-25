from urllib.parse import urlparse

from app.transport import http
from app.parser import html
from app import engine

import json

class HttpHtml(object):
  def __init__(self, **kwargs):

    if 'transport' not in kwargs:
      self.transport = http.Client()
    else:
      self.transport = kwargs['transport']

    if 'parsers' not in kwargs:
      self.parsers = [
        html.CssLink(),
        html.ScriptSrc(),
        html.ImgSrc()
      ]
    else:
      self.parsers = kwargs['parsers']

    if 'engines' not in kwargs:
      
      with open('config/domains.json') as cfg_f:
        domains_cfg = json.load(cfg_f)

      with open('config/headers.json') as cfg_f:
        headers_cfg = json.load(cfg_f)

      self.engines = [
        engine.DomainName(domains_cfg),
        engine.DomainLookup(domains_cfg),
        engine.Header(headers_cfg)
      ]
    else:
      self.engines = kwargs['engines']

  #FIXME: move it out and implement Strategy Pattern
  def _parse_resources(self, rsrc_iter):
    #Feed all parsers with the same data
    for buf in rsrc_iter:
      for parser in self.parsers:
        parser.feed(buf)

    #Now collect all results
    res = []
    for parser in self.parsers:
      res.extend(parser.results())

    return res

  def _get_domain_by_url(self, url):
    res = urlparse(url)
    try:
      domain = res.hostname
    except ValueError:
      return None

    if domain == '':
      return None

    return domain

  #FIXME: move it out and implement Strategy Pattern
  def _process_urls_with_waterfall(self, urls):
    res = {}

    for url in urls:
      domain = self._get_domain_by_url(url)
      #Cache by Domain
      if domain == None:
        continue

      if domain in res:
        continue

      for engine in self.engines:
        cdn = engine.recognize(url)
        if cdn:
          break

      res[domain] = cdn

    return res


  def recognize_cdns(self, url):
    resource_iterator = self.transport.get_iterator(url)    
    
    #Add main URL to the loop as well
    urls = [url]
    urls.extend(self._parse_resources(resource_iterator))

    cdns = self._process_urls_with_waterfall(urls)

    return cdns
