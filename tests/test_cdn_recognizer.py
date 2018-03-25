import pytest
import json
import requests
from unittest.mock import patch


from app import engine

@pytest.fixture
def domains_cfg():
  with open('config/domains.json') as cfp:
    cfg = json.load(cfp)
  return cfg

@pytest.fixture
def headers_cfg():
  with open('config/headers.json') as cfp:
    cfg = json.load(cfp)
  return cfg


def test_recognize_by_domain_name(domains_cfg):
  cases = [
    ("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css", "Cloudflare"),
    ("//viar-4538.kxcdn.com/", "KeyCDN"),    
    ("http://unknown-cdn.com/", None),
    ("http://assets.funnygames.at/", None),
  ]

  eng = engine.DomainName(domains_cfg)

  for (url, cdn) in cases:
    assert eng.recognize(url) == cdn

def test_recognize_by_domain_lookup(domains_cfg):
  cases = [
    ("http://assets.funnygames.at/", "OptimiCDN")
  ]

  eng = engine.DomainLookup(domains_cfg)

  for (url, cdn) in cases:
    assert eng.recognize(url) == cdn  


def fake_get_headers(self, url):
  url_map = {
    "http://www.funnygames.at": {
      'Date': 'Sun, 25 Mar 2018 20:22:51 GMT', 'Content-Type': 'text/html', 'Connection': 'keep-alive',
      'Set-Cookie': '__cfduid=d2bbf2dd0d3a0f1468c5cab8b9623d1791522009371; expires=Mon, 25-Mar-19 20:22:51 GMT; path=/; domain=.funnygames.at; HttpOnly', 
      'Last-Modified': 'Sun, 25 Mar 2018 14:30:08 GMT', 'Vary': 'Accept-Encoding', 
      'P3P': 'CP="IDC DSP DEVa TAIa PSAa PSDa IVAa IVDa OUR BUS UNI NAV INT PRE", CP="NOI DSP COR NID PSA ADM OUR IND NAV COM"', 
      'Server': 'cloudflare', 'CF-RAY': '4014178c948a7277-AMS', 
      'Content-Encoding': 'gzip'},
    "http://assets.funnygames.at/": {
      'Date': 'Tue, 06 Mar 2018 22:24:16 GMT', 'Content-Type': 'image/jpeg', 
      'Content-Length': '6225', 'Connection': 'keep-alive', 'Cache-Control': 'max-age=2592000', 
      'ETag': '"1851-562fc9c606166"', 'Expires': 'Thu, 05 Apr 2018 22:25:54 GMT', 
      'Last-Modified': 'Wed, 17 Jan 2018 17:59:38 GMT', 'Server': 'Footprint Distributor V4.11', 
      'Access-Control-Allow-Origin': '*', 'Age': '1634536', 
      'Accept-Ranges': 'bytes'},
    "https://static.telegraph.co.uk/": {
      'Content-Type': 'application/javascript', 'Connection': 'keep-alive', 
      'Date': 'Mon, 19 Mar 2018 15:48:28 GMT', 'Last-Modified': 'Mon, 19 Mar 2018 15:44:44 GMT', 
      'x-amz-server-side-encryption': 'AES256', 'x-amz-meta-access-control-request-method': '*', 
      'x-amz-meta-origin': '*', 'x-amz-meta-access-control-request-headers': '*', 'Cache-Control': 'max-age=3600', 
      'Server': 'AmazonS3', 'Content-Encoding': 'gzip', 'Vary': 'Accept-Encoding', 
      'Age': '3314', 'X-Cache': 'Hit from cloudfront', 'Via': '1.1 d942ee6a387b745954972448a42def1c.cloudfront.net (CloudFront)', 
      'X-Amz-Cf-Id': 'IWyeprMMygbe8lJvN8lCbTq4nso247YRQw2OqJ7w2Frco_KsiNV93w=='}
  }

  return url_map[url]

@patch.object(engine.Header, '_get_headers', fake_get_headers)
def test_recognize_by_headers(headers_cfg):
  cases = [
    ("http://www.funnygames.at","Cloudflare"),
    ("http://assets.funnygames.at/", None),
    ("https://static.telegraph.co.uk/", "Amazon CloudFront")
  ]


  eng = engine.Header(headers_cfg)

  for (url, cdn) in cases:
    assert eng.recognize(url) == cdn