from html.parser import HTMLParser

class ScriptSrc(HTMLParser):
  """Parses html script tags with src attribute"""

  def __init__(self):
    super(ScriptSrc, self).__init__()
    self.res_arr = []

  def handle_starttag(self, tag, attrs):
    if tag != 'script':
      return

    #attrs has following structure => [ ( 'attribute', 'value' ), .... ]
    src = list( filter(lambda x: x[0] == 'src', attrs) )
    if len(src) == 0:
      return

    self.res_arr.append( src[0][1] )      

  def results(self):
    return self.res_arr


class CssLink(HTMLParser):
  """Parses html link tag for stylsheet with href attribute"""

  def __init__(self):
    super(CssLink, self).__init__()
    self.res_arr = []

  def handle_starttag(self, tag, attrs):
    if tag != 'link':
      return

    #attrs has following structure => [ ( 'attribute', 'value' ), .... ]
    atr_map = { a[0]: a[1] for a in attrs }

    if 'href' not in atr_map:
      return

    self.res_arr.append( atr_map['href'] )

  def results(self):
    return self.res_arr    


class ImgSrc(HTMLParser):
  """Parses html script tags with src attribute"""

  def __init__(self):
    super(ImgSrc, self).__init__()
    self.res_arr = []

  def handle_starttag(self, tag, attrs):
    if tag != 'img':
      return

   #attrs has following structure => [ ( 'attribute', 'value' ), .... ]
    atr_map = { a[0]: a[1] for a in attrs }

    if 'src' not in atr_map:
      return

    self.res_arr.append( atr_map['src'] )  

  def results(self):
    return self.res_arr

