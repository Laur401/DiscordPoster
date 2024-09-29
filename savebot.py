import json
import time
from ruamel.yaml import YAML
from http.client import HTTPSConnection
yaml=YAML()

class UserInfo:
    def __init__(self,user_id,user_token):
        self.user_id=user_id
        self.user_token=user_token
    def to_dict(self):
        return dict(user_id=self.user_id,user_token=self.user_token)

class ChannelInfo:
    def __init__(self,channel_url,channel_name):
        self.channel_url=channel_url
        self.channel_name=channel_name
    def to_dict(self):
        return dict(channel_url=self.channel_url,channel_name=self.channel_name)

class MessageInfo:
    def __init__(self,message):
        self.message=message
    def to_dict(self):
        return dict(message=self.message)

class ScheduleMaker:
    def __init__(self,user_id,user_token,channel_url,channel_name,message):
        self.user_id=user_id
        self.user_token=user_token
        self.channel_url=channel_url
        self.channel_name=channel_name
        self.message=message
    def to_dict(self):
        return dict(user_id=self.user_id,user_token=self.user_token,channel_url=self.channel_url,channel_name=self.channel_name,message=self.message)

class FileManager:
    def __init__(self,file):
        self.file=file

    def create_file(self):
        open(f"{self.file}.yaml", "a").close()

    def write_file(self, content):
        try:
            with open(f"{self.file}.yaml", "r") as f:
                data=yaml.load(f)
            if data is None:
                data=[]
            data.append(content)
            with open(f"{self.file}.yaml", "w") as f:
                yaml.dump(data,f)
        except FileNotFoundError:
            self.create_file()
            self.write_file(content)

    def read_file(self):
        with (open(f"{self.file}.yaml", "r")) as f:
            data=yaml.load(f)
            return [d for d in data]

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

def send_message(queue):
    api_version = 6
    if isinstance(queue,dict):
        queue=[queue]
    for i in queue:
        header_data = {
            "content-type":"application/json",
            "user-id":i['user_id'],
            "authorization":i["user_token"],
            "host":"discordapp.com",
            "referrer":i["channel_url"]
        }
        channel_id=i["channel_url"].split('/')[-1]
        message=i["message"].replace(r"\n","\n")
        message_data = json.dumps({"content":message})
        conn=HTTPSConnection("discordapp.com",443)
        conn.request("POST",f"/api/v{api_version}/channels/{channel_id}/messages", message_data, header_data)
        print(conn.getresponse())
        time.sleep(8)

def message_handler(users,channels,messages):
    users_key = KeyWorker(users)
    channels_key = KeyWorker(channels)
    messages_key = KeyWorker(messages)
    users_key.key_lister("user_id")
    user_nr = int(input("Which user to use?: "))
    channels_key.key_lister("channel_name")
    channel_nr = int(input("Which channel to use?: "))
    messages_key.key_lister("message")
    message_nr = int(input("Which message to send?: "))

    user_id = users_key.key_getter("user_id", user_nr)
    user_token = users_key.key_getter("user_token", user_nr)
    channel_url = channels_key.key_getter("channel_url", channel_nr)
    channel_name = channels_key.key_getter("channel_name", channel_nr)
    message = messages_key.key_getter("message", message_nr)

    i=input("Would you like to send or queue this message? (s/q):")
    if i=="s":
        message_package=dict(user_id=user_id,user_token=user_token,channel_url=channel_url,message=message)
        send_message(message_package)
    if i=="q":
        queue_entry(user_id,user_token,channel_url,channel_name,message)

def main():
    while True:
        user_input()

def user_input():
    i=input("Enter 1 to add a new user.\nEnter 2 to add a new channel.\nEnter 3 to add a new message.\nEnter 4 to post a message.\nEnter 5 to send the queue.: ")
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
        message_handler(users,channels,messages)
    if i=="5":
        queue_file=FileManager("queue")
        queue = queue_file.read_file()
        send_message(queue)

def channel_entry():
    writer=FileManager("channels")
    channel_url=input("Enter your Discord channel URL: ")
    channel_name=input("Enter your Discord channel name: ")
    info=ChannelInfo(channel_url,channel_name)
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

def queue_entry(user_id,user_token,channel_url,channel_name,message):
    writer=FileManager("queue")
    info=ScheduleMaker(user_id,user_token,channel_url,channel_name,message)
    writer.write_file(info.to_dict())

if __name__ == "__main__":
    main()