import json
import yaml
from http.client import HTTPSConnection

class UserInfo:
    def __init__(self,user_id,user_token):
        self.user_id=user_id
        self.user_token=user_token
    def to_dict(self):
        return {
            'user_id':self.user_id,
            'user_token':self.user_token
        }

class ChannelInfo:
    def __init__(self,channel_url,channel_id):
        self.channel_url=channel_url
        self.channel_id=channel_id
    def to_dict(self):
        return {
            'channel_url':self.channel_url,
            'channel_id':self.channel_id
        }

class MessageInfo:
    def __init__(self,message):
        self.message=message
    def to_dict(self):
        return {
            'message':self.message
        }

class FileManager:
    def __init__(self,file):
        self.file=file

    def create_file(self):
        open(f"{self.file}.yaml", "a").close()

    def write_file(self, content):
        f = open(f"{self.file}.yaml", "a")
        yaml.dump(content,f)
        f.close()

    def read_file(self):
        f = open(f"{self.file}.yaml", "r")
        return yaml.safe_load_all(f)


def send_message(users,channels,messages):
    api_version=6
    user_nr=int(input("Which user to use?: "))
    channel_nr=int(input("Which channel to use?: "))
    message_nr=int(input("Which message to send?: "))
    user_id=users[user_nr].user_id
    user_token=users[user_nr].user_token
    channel_url=channels[channel_nr].channel_url
    channel_id=channels[channel_nr].channel_id
    header_data={
        "content-type":"application/json",
        "user-id":user_id,
        "authorization":user_token,
        "host":"discordapp.com",
        "referrer":channel_url
    }
    message_data=json.dumps({"content":messages[message_nr].message})
    conn=HTTPSConnection("discordapp.com",443)
    conn.request("POST",f"/api/v{api_version}/channels/{channel_id}/messages", message_data, header_data)
    print(conn.getresponse())

def main():
    users=[]
    channels=[]
    messages=[]
    while True:
        user_input(users,channels,messages)

def user_input(users,channels,messages):
    i=input("Enter 1 to add a new user.\nEnter 2 to add a new channel.\nEnter 3 to add a new message.\nEnter 4 to post a message.: ")
    if i=="1":
        user_entry(users)
    if i=="2":
        channel_entry(channels)
    if i=="3":
        message_entry(messages)
    if i=="4":
        send_message(users,channels,messages)

def channel_entry(channels):
    channel_url=input("Enter your Discord channel URL: ")
    channel_id=input("Enter your Discord channel ID: ")
    channels.append(ChannelInfo(channel_url,channel_id))

def user_entry(users):
    user_id = input("Enter your Discord user ID: ")
    user_token = input("Enter your Discord user token: ")
    users.append(UserInfo(user_id,user_token))

def message_entry(messages):
    message=input("Enter your message: ")
    messages.append(MessageInfo(message))

if __name__ == "__main__":
    main()