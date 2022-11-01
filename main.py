import requests
import time

# your discord webhook
webhook = "https://discord.com/api/webhooks/0000000000000000000/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
# https://www.twitch.tv/xqc
streamers = ["xqc", "jakenbakelive"]
# check stream every 60 sec
delay = 60

def discord(msg):
    if(webhook == None):
        print("[discord] incorrect webhook")
        return
    data = {
            "content": msg
        }
    response = requests.post(webhook, json=data)
    print(f"[discord] {response.status_code}")

class User():
    def __init__(self, json):
        try:
            user = json["data"]["user"]
            self.login = user["login"]
            self.displayName = user["displayName"]
            self.stream = Stream(user["stream"])
        except (AttributeError, KeyError, TypeError):
            self.login = None
            self.displayName = None
            self.stream = Stream(None)

    def __eq__(self, __o: object) -> bool:
        if(__o == None):
            return self.login == None and self.displayName == None and self.stream == None
        return self.login == __o.login and self.displayName == __o.displayName and self.stream == __o.stream

class Stream():
    def __init__(self, stream):
        try:
            self.id = stream["id"]
            self.title = stream["title"]
            self.createAt = stream["createdAt"]
            self.gameName = stream["game"]["name"]
        except (AttributeError, KeyError, TypeError):
            self.id = None
            self.title = None
            self.createAt = None
            self.gameName = None
    
    def __eq__(self, __o: object) -> bool:
        if(__o == None):
            return self.id == None and self.title == None and self.createAt == None and self.gameName == None
        return self.id == __o.id and self.title == __o.title and self.createAt == __o.createAt and self.gameName == __o.gameName

def getUserData(displayName) -> User:
    headers = {
        "Client-ID": "kimne78kx3ncx6brgo4mv6wki5h1ko"
    }
    query = """
    query { 
        user(login: "__displayName__") { 
            login 
            displayName 
            stream { 
                id 
                createdAt 
                title 
                game { 
                    name 
                } 
            } 
        } 
    }
    """.replace("__displayName__", displayName)
    response = requests.post("https://gql.twitch.tv/gql", headers=headers, json={"query": query}, timeout=10)
    return User(response.json())

latest_users = []
def checkStreamer(streamer):
    user = getUserData(streamer)
    if(user == None):
        # user not exist
        return
    if(user.stream == None):
        # user is offline
        return
    if(user in latest_users):
        # already
        return
    discord(f"{user.displayName}\n{user.stream.title}\n{user.stream.gameName}")
    latest_users.append(user)

while True:
    for streamer in streamers:
        checkStreamer(streamer)
    time.sleep(delay)
