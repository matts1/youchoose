import re
import urllib2
import xml.etree.ElementTree as ET
from . import render
from functions.users import require_login

@require_login
def add(response, user):
    url = response.get_field("url")
    if url != None:
        get = re.findall(r".*?youtube\.com[^/]*?/watch\?(?:.+?=.+?&)*v=([^&]+)(?:&.+?=.+?)*", url)[0]
        query_url = "https://gdata.youtube.com/feeds/api/videos/%s?v=2" % get
        data = urllib2.urlopen(query_url).read()
        root = ET.fromstring(data)

        find = lambda key, attrib: [x for x in root.iter(key)][0].attrib[attrib]

        published = root.find("{http://www.w3.org/2005/Atom}published").text
        title = root.find("{http://www.w3.org/2005/Atom}title").text
        duration = int(find("{http://gdata.youtube.com/schemas/2007}duration", "seconds"))
        views = int(find("{http://gdata.youtube.com/schemas/2007}statistics", "viewCount"))
        author = [x for x in root.iter("{http://www.w3.org/2005/Atom}name")][0].text

        values = {
            "url": url,
            "title": title,
            "published": published,
            "duration": duration,
            "views": views,
            "author": author
        }
        for key in values:
            print key, values[key]

    render("add.html", response, {"url": url})
