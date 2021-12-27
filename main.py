import os
from posixpath import join
import pymongo
import tornado.ioloop
import tornado.web
import tornado.escape
from bson import ObjectId
from pymongo.mongo_client import MongoClient
from sshtunnel import SSHTunnelForwarder

client = MongoClient("mongodb://kent:viygF&$^&VFJF@119.45.163.114:27017/TweetScraper")
db = client["TweetScraper"]


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        datetimes = []
        texts = []
        retweets = []
        favorites = []
        urls = []
        
        limit = 20
        i = 1
        for tweet in db["tweetday"].find( { "is_labeled" : { "$in": [0, 'false', 'N/A', None]}}):
            datetimes.append(tweet['created_at'])
            texts.append(tweet['text'])
            retweets.append(tweet['retweet_cou'])
            favorites.append(tweet['like_count'])
            urls.append(tweet['url'])
            if i == limit:
                break
            else:
                i += 1
        self.render("index.html", datetimes = datetimes, texts = texts, retweets = retweets, favorites = favorites, urls = urls)


def setUpApp(): 

    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static")
    }
    app = tornado.web.Application(
        [
            (r"/", MainHandler)
        ],
        **settings,
        db = db
    )
    return app

if __name__=="__main__":
    app = setUpApp()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()