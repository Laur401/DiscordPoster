import json
from http.client import HTTPSConnection

def send_message():
    api_version=6
    user_id=***REMOVED***
    token="***REMOVED***"
    channel_url="***REMOVED***"
    channel_id=***REMOVED***
    header_data={
        "content-type":"application/json",
        "user-id":user_id,
        "authorization":token,
        "host":"discordapp.com",
        "referrer":channel_url
    }
    message_data=json.dumps({"content":"Hello, world"})
    conn=HTTPSConnection("discordapp.com",443)
    conn.request("POST",f"/api/v{api_version}/channels/{channel_id}/messages", message_data, header_data)
    #conn.request("POST",f"/api/v6/channels/***REMOVED***/messages", message_data, header_data)
    print(conn.getresponse())

def main():
    send_message()

if __name__ == "__main__":
    main()