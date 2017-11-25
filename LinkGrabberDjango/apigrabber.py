import base64
import hashlib
import json
import time
import requests
from django.utils import timezone
from LinkGrabberDjango.models import Setting, Post
from pyimei import ImeiSupport
from Crypto import Random
from Crypto.Cipher import AES
import sys
reload(sys)
import re
from django.db.models import Q

sys.setdefaultencoding("utf8")

key = "darth19@1234bhgdrasew@1094561234"
bs = 32
currenttimems = str(int(round(time.time() * 1000)))[0:10]
baseurl = "http://appmoviehd.info/admin/index.php/apiandroid2/"

def encrypt(raw, key=key):
    raw = _pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))


def decrypt(enc, key=key):
    enc = base64.b64decode(enc)
    iv = enc[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return _unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')


def _pad(s):
    return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)


def _unpad(s):
    return s[:-ord(s[len(s) - 1:])]


def getToken():
    version = Setting.objects.get(Status="Current").AppVersion
    token = "ttteam@android@122334" + currenttimems
    token = hashlib.md5(token.encode('utf-8')).hexdigest().upper()
    params = {'os': 'android', 'version': version, 'token': token, 'tokengoogle': '', 'time': currenttimems, 'ads': '0','deviceid': ImeiSupport.generateNew() }
    return params

def apirequest(suffix, apiparams):
    params = getToken().copy()
    params.update(apiparams)
    response = requests.get(baseurl + suffix,params=params)
    r = response.text
    testtext = decrypt(r)
    text = testtext[testtext.index("{"):][:-1]
    jsonResponse = json.loads(text)
    return jsonResponse

def getpopular(type):
    params = {'type': 'updated', 'page': '1', 'count':'10'}
    suffix = type
    videos2 = apirequest(suffix,params)

    return videos2["films"]

def createmainlisting(name):
    params = {'type': 'search', 'keyword': name, 'page':'1','count':'10'}
    suffix = "movies"
    videos2 = apirequest(suffix,params)

    return videos2["films"]


def createdetails(id):

    params = {'id': id, 'page':'1','count':'-1'}
    suffix = "detail"
    videos2 = apirequest(suffix,params)

    return {"posts": videos2["chapters"],
            "desc": videos2["desc"],
            "rating": videos2['rating'],
            "startyear": videos2['startyear'],
            "title": videos2['title'],
            "poster": videos2['poster'],
            "state": videos2['state'],
            "genre": videos2['genre'],
            }


def getstreams(id):
    streamurl = baseurl + "stream?chapterid=" + id + "&page=1&count=-1&"
    r = requests.get(streamurl, params=getToken()).text
    test3 = decrypt(r)
    text3 = test3[test3.index("{"):][:-1]
    videos3 = json.loads('{"bar":[' + text3 + "}")
    print test3
    return videos3["bar"]




def getToplist(type, page, sort):
    allvids = []
    notlast = "yes"
    currentpage = 1

    while notlast == "yes":
        params = {'type': sort, 'page': str(currentpage), 'count': '5000'}
        suffix = type
        videos2 = apirequest(suffix, params)
        allvids += videos2["films"]
        notlast = videos2["more"]
        currentpage += 1

    return allvids

def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""

def testtime():
    start_time = time.time()
    print getToplist("movies",1,"popular")
    print("---- %s seconds ----" % (time.time() - start_time))

def loadListToDB():
    hits= 0
    for i in range(6000,20000):
        params = {'id': i, 'page': '1', 'count': '-1'}
        suffix = "detail"
        videos2 = apirequest(suffix, params)
        if videos2["id"] is not None:
            if videos2["poster"]:
                obj, created = Post.objects.update_or_create(
                    id=int(videos2["id"]),
                    defaults={'id': int(videos2["id"]),
                              "title": videos2["title"],
                              "rating":float(videos2["rating"]),
                              "poster": videos2["poster"],
                              "year": int(videos2["startyear"]),
                              },
                )
                print "added" + videos2["id"]
            else:
                hits= hits +1
                print videos2["id"]
                print "skipped"

    return hits


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

         normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query
