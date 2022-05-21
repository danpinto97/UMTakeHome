from flask import Flask
from flask import request
from URLReq import URLReq

app = Flask(__name__)

'''Route for shortening a URL. Will take in a URL, check if short form exists
and generate a new one if none exists.'''
@app.route('/ShortenUrl', methods=["POST"])
def Shorten():
    #if our request has a  url
    if(request.json):
        # Save original URL and 
        url = request.json
        url_req = URLReq()
        url_req.initLongUrl(url)
        return url_req.ShortenUrl()
            
    # Return nothing on default
    return {"data" : ""}

'''Route for getting the longer version of a shortened url. Will return N/a if none exists'''
@app.route('/GetUrl', methods=["POST"])
def GetLongUrl():
    # If our request has a payload
    if(request.json):
        url = request.json
        # Strip out the last part of the url (if not empty of course)
        stripped = url.split('dannyurl/')
        
        if(stripped):
            url_req = URLReq()
            # Last element should be what we need (definitely prone to error here)
            url_req.initShortUrl(stripped[-1])
            return url_req.FindLongUrl()
            
    # Return N/a on default
    return {"data" : "N/a"}
if __name__ == "__main__":
    app.run(debug=True)
