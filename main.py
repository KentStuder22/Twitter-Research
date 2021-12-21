import json
import pymongo
import tornado.ioloop
import tornado.web
import tornado.escape
from bson import ObjectId
from pymongo.mongo_client import MongoClient
from sshtunnel import SSHTunnelForwarder

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        tweets = self.settings["db"]["tweet"].find()
        self.render("index.html", tweets = tweets)

def setUpApp(): 
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

    app = tornado.web.Application(
        [
            (r"/", MainHandler)
        ],
        db = db
    )
    return app

if __name__=="__main__":
    app = setUpApp()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()