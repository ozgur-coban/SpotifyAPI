import requests
import urllib.parse
from datetime import datetime 
from flask import Flask , redirect , request , jsonify ,session 



app=Flask(__name__)
app.secret_key='123456'

CLIENT_ID='888df5bddb1748eb9f00d4decd7cc353'
CLIENT_SECRET='3c2c365906854355859d681ef7ea2a6e'
REDIRECT_URI='http://192.168.1.2:5000/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL='https://accounts.spotify.com/api/token' #refresh
API_BASE_URL='https://api.spotify.com/v1/'


@app.route('/')#route of the flask app
def index():
    return " <a href='/login'>Login with Spotify</a>" #returns html link


@app.route('/login') #login endpoint
def login():
    scope='playlist-modify-public playlist-modify-private user-read-currently-playing'  #scope for permissions
    
    params={ #pass to spotify 
        'client_id':CLIENT_ID,
        'response_type':'code',
        'scope':scope,
        'redirect_uri': REDIRECT_URI,
        
    }
    
    auth_url=f"{AUTH_URL}?{urllib.parse.urlencode(params)}"#encoding params
    
    return redirect(auth_url)

@app.route('/callback') #callback endpoint , once user logs in
def callback():
    if 'error' in request.args: #spotify sends the request once user logs in
        return jsonify({"error":request.args['error']})
    
    
    if 'code' in request.args:
        req_body={ #another thing to send to spotify to get the auth token 
            'code':request.args['code'],
            'grant_type':'authorization_code',
            'redirect_uri':REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret':CLIENT_SECRET
        }
        
        response=requests.post(TOKEN_URL,data=req_body) #sending req body to spotify
        token_info=response.json() #spotify gives back token as json 
        
        session['access_token']=token_info['access_token'] #session for storing the data from flask
        session['refresh_token']=token_info['refresh_token']
        session['expires_at']=datetime.now().timestamp()+token_info['expires_in']
        
        return redirect('/AddCurrentSongToThePlaylist') #redirecting to endpoint which will be using this access token
    
    
    
@app.route('/AddCurrentSongToThePlaylist')




def AddToPlaylist():
    
    
    

        if'access_token' not in session: #check if access token is in the session
            return redirect('/login')
        
        if datetime.now().timestamp()>session['expires_at']:
            return redirect('/refresh-token')
        
        
        
        headers1={
            'Authorization':f"Bearer {session ['access_token']}"
        }
        
        response1=requests.get(API_BASE_URL+'me/player/currently-playing',headers=headers1) 
        CurrentSong=response1.json()
        CurrentSong_Uri=(CurrentSong.get("item")).get("uri")
        song_uri=CurrentSong_Uri
            
        
        #start of the request to do what you want 
        
        headers={#contains authorization token
            'Authorization':f"Bearer {session ['access_token']}" , 
            'Content-Type': 'application/json'
            
        }
        
        
        data={
            'uris':[song_uri]
            
            
            
        }
        
        
        response=requests.post(url=API_BASE_URL+'playlists/"playlistUrl"/tracks',headers=headers , params=data ) #stores the result of making the request 
        AddToPlaylist=response.json()
        

        return jsonify(AddToPlaylist)
        



@app.route('/refresh-token') #redirecting user to refresh token if token is expired , refreshing the token here , redirecting back to main route
def refresh_token():#using the refresh token
    if'refresh_token' not in session:
        return redirect('/login')
    
    
    
    if datetime.now().timestamp()>session['expires_at']:
        req_body={
            'grant_type':'refresh_token',
            'refresh_token':session['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret':CLIENT_SECRET
        }
    
        response=requests.post(TOKEN_URL,data=req_body) #send spotify the req body , spotify gives back new token info as json , save that to response
        new_token_info=response.json()
        session['access_token']=new_token_info['access_token'] #updating variables
        session['expires_at']=datetime.now().timestamp()+new_token_info['expires_in']
        
        return redirect('/AddCurrentSongToThePlaylist')
    
if __name__=='__main__':
    app.run(host='0.0.0.0' , debug=True)
    
    
    
    
    
    