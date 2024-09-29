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
        return list(yaml.safe_load_all(f)) #don't want a generator for now

class KeyWorker:
    def __init__(self,dics):
        self.dics=dics

    def key_lister(self,target_key):
        i=1
        for dic in self.dics:
            for key, value in dic.items():
                if key == target_key:
                    print(f"{i}: {value}")
                    i+=1

    def key_getter(self,target_key,i):
        values=[]
        for dic in self.dics:
            for key, value in dic.items():
                if key == target_key:
                    values.append(value)
        if 1<=i<=len(values):
            return values[i-1]
        else:
            return None

def send_message(users,channels,messages):
    api_version=6
    users_key=KeyWorker(users)
    channels_key=KeyWorker(channels)
    messages_key=KeyWorker(messages)
    users_key.key_lister("user_id")
    user_nr=int(input("Which user to use?: "))
    channels_key.key_lister("channel_id")
    channel_nr=int(input("Which channel to use?: "))
    messages_key.key_lister("message")
    message_nr=int(input("Which message to send?: "))
    user_id=users_key.key_getter("user_id",user_nr)
    user_token=users_key.key_getter("user_token",user_nr)
    channel_url=channels_key.key_getter("channel_url",channel_nr)
    channel_id=channels_key.key_getter("channel_id",channel_nr)
    message=messages_key.key_getter("message",message_nr)
    header_data={
        "content-type":"application/json",
        "user-id":user_id,
        "authorization":user_token,
        "host":"discordapp.com",
        "referrer":channel_url
    }
    message_data=json.dumps({"content":message})
    conn=HTTPSConnection("discordapp.com",443)
    conn.request("POST",f"/api/v{api_version}/channels/{channel_id}/messages", message_data, header_data)
    print(conn.getresponse())

def main():
    while True:
        user_input()

def user_input():
    i=input("Enter 1 to add a new user.\nEnter 2 to add a new channel.\nEnter 3 to add a new message.\nEnter 4 to post a message.: ")
    if i=="1":
        user_entry()
    if i=="2":
        channel_entry()
    if i=="3":
        message_entry()
    if i=="4":
        users_file = FileManager("users")
        users = users_file.read_file()
        channels_file = FileManager("channels")
        channels = channels_file.read_file()
        messages_file = FileManager("messages")
        messages = messages_file.read_file()
        send_message(users,channels,messages)

def channel_entry():
    writer=FileManager("channels")
    channel_url=input("Enter your Discord channel URL: ")
    channel_id=input("Enter your Discord channel ID: ")
    info=ChannelInfo(channel_url,channel_id)
    writer.write_file(info.to_dict())

def user_entry():
    writer=FileManager("users")
    user_id = input("Enter your Discord user ID: ")
    user_token = input("Enter your Discord user token: ")
    info=UserInfo(user_id,user_token)
    writer.write_file(info.to_dict())

def message_entry():
    writer=FileManager("messages")
    message=input("Enter your message: ")
    info=MessageInfo(message)
    writer.write_file(info.to_dict())

if __name__ == "__main__":
    main()