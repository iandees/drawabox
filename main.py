#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

class UserBboxHandler(webapp.RequestHandler):
    def get(self):
        lat = self.request.get('lat')
        lon = self.request.get('lon')
        zoom = self.request.get('zoom')
        returnUrl = self.request.get('ret')

        template_values = {}

        if returnUrl:
            template_values['return_url'] = returnUrl

        if lat and lon and zoom:
            template_values['initial_loc'] = {
                'lat': lat,
                'lon': lon,
                'zoom': zoom
            }


        path = os.path.join(os.path.dirname(__file__), 'bboxmap.html')
        self.response.out.write(template.render(path, template_values))

class UserBboxSelected(webapp.RequestHandler):
    def post(self):
        bbox = self.request.get('bbox')
        returnUrl = self.request.get('return_url')

        if bbox and returnUrl:
            self.redirect("%s?bbox=%s" % (returnUrl, bbox))
        else:
            self.error(404)


def main():
    application = webapp.WSGIApplication([
                                          ('/userBbox', UserBboxHandler),
                                          ('/bboxSelected', UserBboxSelected),
                                         ],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
