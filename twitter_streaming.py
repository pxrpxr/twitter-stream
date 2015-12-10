#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import ConfigParser
from os.path import expanduser
import pprint
#Variables that contains the user credentials to access Twitter API

class Configer:
    def __init__(self, filename):
        self.filename = filename
        self.config = ConfigParser.ConfigParser()
        self.config.read(filename)
    def ConfigSectionMap(self, section):
        dict1 = {}
        options = self.config.options(section)
        for option in options:
            try:
                dict1[option] = self.config.get(section, option)
                if dict1[option] == -1:
                    print ("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':
    #This handles Twitter authetification and the connection to Twitter Streaming API
    home = expanduser("~")
    filename            = "%s/.twitter_streaming" % home
    config              = Configer(filename)
    section_map = config.ConfigSectionMap('access')
    consumer_key        = section_map['consumer_key']
    consumer_secret     = section_map['consumer_secret']
    access_token        = section_map['access_token']
    access_token_secret = section_map['access_token_secret']

    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    #
    # #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['python', 'javascript', 'ruby'])
