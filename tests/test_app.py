import pytest

from app.app import HttpHtml 

#FIXME: add mocks for WEB resource. It is a bad thing to test something with uncotrollable resource like website.
def test_cdn_recognition():
  url = 'https://www.funnygames.at'

  #It seems that I cannot use Packaging in Python :( (we need moar apps)
  app_service = HttpHtml()

  cdns = app_service.recognize_cdns(url)

  expected = {
    'assets.funnygames.at': 'OptimiCDN',
    'www.funnygames.at': 'Cloudflare',
    'cdnjs.cloudflare.com': 'Cloudflare',
    's7.addthis.com': None
  }

  assert cdns == expected