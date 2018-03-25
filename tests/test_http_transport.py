import pytest

from app.transport import http

def test_transport_should_offer_iterable():
  client = http.Client()

  getattr(client, 'get_iterator')