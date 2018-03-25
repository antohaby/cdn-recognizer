import falcon
from app.app import HttpHtml
import json

class MainResource(object):

    def on_get(self, req, resp):
        resp.body = '<h1>To Be Done</h1>'
        resp.content_type = falcon.MEDIA_HTML
        resp.status  = falcon.HTTP_200

    def on_post(self, req, resp):        

        url = req.media['url']

        app_service = HttpHtml()
        cdns = app_service.recognize_cdns(url)

        resp.body = json.dumps(cdns)
        resp.status = falcon.HTTP_200


# Configure your WSGI server to load "things.app" (app is a WSGI callable)
api = falcon.API()

api.add_route('/recognize/cdns', MainResource())