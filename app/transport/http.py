import requests

class Client(object):
  """A wrapper for requests module to get html by given url"""

  def __init__(self, chunk_size=128):
      self.chunk_size = chunk_size

  def get_iterator(self, url):
    #TODO: Add try expect and response code checker.
    return requests.get(url, stream=True).iter_content(chunk_size=self.chunk_size, decode_unicode=True)
