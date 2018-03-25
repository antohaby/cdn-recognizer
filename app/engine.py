from urllib.parse import urlparse
import requests
import dns.resolver
from dns.exception import DNSException

class DomainName(object):

  def __init__(self,cfg):
    #TODO: validate cfg
    #TODO: increase performance of cfg by using full text key indexing.
    self.rules = cfg

  def recognize(self, url):
    res = urlparse(url)
    try:
      domain = res.hostname
    except ValueError:
      return None

    if domain == '':
      return None

    #TODO: Add caching for already known domains

    for (rule, cdn) in self.rules:    
      if rule in domain:
        #TODO: Remember which rule has matched so next time we will able to reindex 
        # and check most popular rules first increasing performance.
        return cdn

    return None

#FIXME: combine Domain engines together (if possible)
class DomainLookup(object):
  def __init__(self,cfg):
    #TODO: validate cfg
    #TODO: increase performance of cfg by using full text key indexing.
    self.rules = cfg

  def recognize(self, url):

    res = urlparse(url)
    try:
      domain = res.hostname
    except ValueError:
      return None

    if domain == '':
      return None

    domains = []
    try:
      #Find cannonical domain
      q_res = dns.resolver.query(domain, 'CNAME')
      domains = [r.to_text() for r in q_res]
    except DNSException:
      #TODO: add logger
      return None

    #TODO: Add caching for already known domains
    for domain in domains:    
      for (rule, cdn) in self.rules:    
        if rule in domain:
          #TODO: Remember which rule has matched so next time we will able to reindex 
          # and check most popular rules first increasing performance.
          return cdn    
    
    return None
            

class Header(object):
  def __init__(self,cfg):    
    #Prepare rules to be in following format:
    #{ headerName: [ (value1, Cdn1), (Value2, Cdn2), .... ], .... }
    rules = {}
    for ( header, value, cdn ) in cfg:
      header = header.lower()

      if header not in rules:
        rules[header] = []

      rules[header].append( [value, cdn] )

    self.rules = rules

  def _get_headers(self,url):
    #If url has following format: //domain
    #try to add http in front of it
    if url[:2] == '//':
      url = 'http:' + url

    #TODO: Add try expect and response code checker.
    try:
      r = requests.head(url)
      return r.headers
    except requests.RequestException:
      #Log errors
      print("Cannot parse for URL: " + url)
      return {}


  def recognize(self, url):
    #Suppose validation already done for URL
    headers = self._get_headers(url)

    for (header, value) in headers.items():
      header = header.lower()

      if header in self.rules:
        for (rule, cdn) in self.rules[header]:
          if rule in value:
            return cdn

    return None