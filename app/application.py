from flask import Flask
from flask import request
import time
import random
import sqlite3
import re

# What we can build a shortened url from
string_choices = '012345689abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
app = Flask(__name__)

'''In real scenario would create better hash function, but for this case
we will just use random. Small use case, very unlikely we will get a repeat but
not as scaleable'''
def UrlHasher(orig):
    # Randomly choose a character from our options above 7 times to build
    hashed = ''.join((random.choice(string_choices) for i in range(7)))
    return hashed

'''Route for shortening a URL. Will take in a URL, check if short form exists
and generate a new one if none exists.'''
@app.route('/ShortenUrl', methods=["POST"])
def Shorten():
    #if our request has a  url
    if(request.json):
        # Save original URL and 
        url = request.json        
        # Connect to DB
        with sqlite3.connect('urls.db') as connection:
            cursor = connection.cursor()
            # Check if our long URL has an entry
            query = 'SELECT * FROM entries WHERE long_url=?'
            res = cursor.execute(query, (url,))
            result = res.fetchall()
            # If we already created a shortened URL for this, then return it
            if(result):
                print("Returning")
                return {"data" : "https://dannyurl/"+result[0][1]}
            else:
                # Hash our url. In real situation would implement a check
                # on if the current hash already exists. If it does, we re-hash until we get a unique one.
                hashed_url = UrlHasher(url)
                cursor.execute("INSERT INTO entries VALUES (?, ?, ?)", (url, hashed_url, time.time()))
                return {"data" : "https://dannyurl/" + hashed_url}
            
    # Return nothing on default
    return {"data" : ""}

'''Route for getting the longer version of a shortened url. Will return N/a if none exists'''
@app.route('/GetUrl', methods=["POST"])
def GetLongUrl():
    # If our request has a payload
    print(request.json)
    if(request.json):
        url = request.json
        # Strip out the last part of the url (if not empty of course)
        stripped = url.split('dannyurl/')
        if(stripped):
            # Last element should be what we need (definitely prone to error here)
            stripped = stripped[-1]    
            # Connect to DB
            with sqlite3.connect('urls.db') as connection:
                cursor = connection.cursor()
                # Check if our long URL has an entry
                query = 'SELECT * FROM entries WHERE short_url=?'
                res = cursor.execute(query, (stripped,))
                result = res.fetchall()
                print(result)
                # If it exists, return it
                if(result):
                    return {"data" : result[0][0]}
                # Otherwise return N/a
                else:
                    return {"data" : "N/a"}
    return {"data" : "N/a"}
if __name__ == "__main__":
    app.run(debug=True)
