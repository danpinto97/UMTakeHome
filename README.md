# UMTakeHome

Took ~3.5-4 hours to finish

Created utilizing Python3 with Flask for backend and React for frontend

My node version is v18.0.0 (npm versionb 8.6.0)
Steps to run:
1. Install python requirements
  pip install -r requirements.txt
2. Install node modules
  npm install (from UMClient directory)
3. Run server
  python3 application.py
4. Run client (from UMClient directory)
  npm start

When the app launches you can use the left-hand text input to input either a URL to shorten OR a shortened URL to get the long form of. The button you press below will distinguish between which of the two you are doing. There are some assumptions made (you can see some code comments) such as  the shortened version of the url will be returned in a "tinyurl" fashion. It is also expected that when getting a full URL, the input URL will be in the dannyurl format.
