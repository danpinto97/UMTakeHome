import sqlite3
import random
import time

# What we can build a shortened url from
string_choices = '012345689abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

'''
URL Request Class
Contains short URL version and long URL version
With capabilities to connect to the DB and return each
'''
class URLReq:
    def __init__(self):
        self.long_url = ""
        self.short_url = ""
    
    def initShortUrl(self, shortUrl):
        self.short_url = shortUrl
        self.long_url = ""

    def initLongUrl(self, longUrl):
        self.long_url = longUrl
        self.short_url = ""

    '''In real scenario would create better hash function, but for this case
    we will just use random. Small use case, very unlikely we will get a repeat but
    not as scaleable'''
    def UrlHasher(self, orig):
        # Randomly choose a character from our options above 7 times to build
        self.short_url = ''.join((random.choice(string_choices) for i in range(7)))

    '''
    Method to Shorten a longUrl. First we connect to the db and check if we have already hashed the
    long url. If so, no need to hash again - just return the entry we found. If no hashed url exists
    for this long url, we want to hash it and insert it into the DB before returning. In a real situation,
    we'd want to check that the hash we create doesn't already exist in the DB but since this use case is 
    so small I did not implement it since it's very unlikely.
    '''
    def ShortenUrl(self):
        # Connect to DB
        with sqlite3.connect('urls.db') as connection:
            cursor = connection.cursor()
            # Check if our long URL has an entry
            query = 'SELECT * FROM entries WHERE long_url=?'
            res = cursor.execute(query, (self.long_url,))
            result = res.fetchall()
            # If we already created a shortened URL for this, then return it
            if(result):
                print("Returning")
                return {"data" : "https://dannyurl/"+result[0][1]}
            else:
                # Hash our url. In real situation would implement a check
                # on if the current hash already exists. If it does, we re-hash until we get a unique one.
                self.UrlHasher(self.long_url)
                cursor.execute("INSERT INTO entries VALUES (?, ?, ?)", (self.long_url, self.short_url, time.time()))
                return {"data" : "https://dannyurl/" + self.short_url}
        # Default nothing
        return {"data": ""}

    '''
    Method to connect to the db and find the LongUrl from a shortened URL.
    We strip out the /xxxxxxx portion from a dannyurl/xxxxxxx and look it up.
    If no corresponding entry exists, we return N/a.
    '''
    def FindLongUrl(self):
        # Connect to DB
        with sqlite3.connect('urls.db') as connection:
            cursor = connection.cursor()
            # Check if our long URL has an entry
            query = 'SELECT * FROM entries WHERE short_url=?'
            res = cursor.execute(query, (self.short_url,))
            result = res.fetchall()
            # If it exists, return it
            if(result):
                return {"data" : result[0][0]}
            # Otherwise return N/a
            else:
                return {"data" : "N/a"}
        return {"data" : "N/a"}