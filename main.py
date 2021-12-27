from os import path
import json
from posixpath import join
import config
import pymongo
import tornado.ioloop
import tornado.web
import tornado.escape
from bson import ObjectId
from pymongo.mongo_client import MongoClient
from sshtunnel import SSHTunnelForwarder

#Settings for Mongo Server
MONGODB_SERVER = '119.45.163.114'
MONGO_USER = 'kent'
MONGO_PASSWORD = 'kent'
MONGODB_PORT = 27017
MONGODB_DB = 'TweetScraper'

server = SSHTunnelForwarder(
    MONGODB_SERVER,
    ssh_username=MONGO_USER,
    ssh_password=MONGO_PASSWORD,
    remote_bind_address=('127.0.0.1', MONGODB_PORT),
)

server.start()
connection = pymongo.MongoClient('127.0.0.1', server.local_bind_port)
db = connection[MONGODB_DB]


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        datetimes = []
        texts = []
        retweets = []
        favorites = []
        urls = []
        
        limit = 20
        i = 1
        for tweet in db["tweetday"].find():
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

    app = tornado.web.Application(
        [
            (r"/", MainHandler)
        ],
        db = db
    )
    return app

if __name__=="__main__":
    print(config.__version__)
    app = setUpApp()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()