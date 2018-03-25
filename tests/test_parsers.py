import pytest

import app.parser.html as html_parser

@pytest.fixture
def html_doc():
  return """
  <html>  
    <head>
      <bla-bla>
      <script src="https://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js"></script>
      <link rel="stylesheet" type="text/css" href="theme.css">
      <script src="./add?ds=&lt;&quot; dsf"></script>
      <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
      <a href="/">ASad<img src="assets/any.image" alt="http://any.image.com"></a>
      <h1></h2><image></image>
      <img src="http://lorempixel.com/400/200/cats/" >
      <img alt="broken Image" />
    </body>
  </html>
  """

def test_script_src_parser(html_doc):
  parser = html_parser.ScriptSrc()

  for char in html_doc:
    parser.feed(char)


  results = [
    #Regular URL
    'https://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js',
    #Html entity like: &quot;
    './add?ds=<" dsf'
  ]

  assert parser.results() == results


def test_link_rel(html_doc):
  parser = html_parser.CssLink()

  for char in html_doc:
    parser.feed(char)

  results = [
    'theme.css',
    'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css'
  ]

  assert parser.results() == results


def test_img_src(html_doc):
  parser = html_parser.ImgSrc()

  for char in html_doc:
    parser.feed(char)

  results = [
    'assets/any.image',
    'http://lorempixel.com/400/200/cats/'
  ]

  assert parser.results() == results
