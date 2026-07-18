import os 

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()

app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"],
)
#commands



@app.command("/testing")
def testing(ack,body,client):
    ack()

    client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type":"modal",
            "callback_id":"testdashboard",
            "title":{
                "type":"plain_text",
                "text":"testing_dashboard"
            },
            "submit":{
                "type":"plain_text",
                "text":"Submit"
            },
            "blocks": [
                {
                    "type":"actions",
                    "block_id":"interest",
                    "elements": [
                        {
                            "type":"checkboxes",
                            "action_id":"channel_checkboxes",
                            "options":[
                                {
                                    "text":{
                                        "type":"plain_text",
                                        "text":"Art"
                                    },
                                    "value":"Art"
                                },
                                {
                                    "text":{
                                        "type":"plain_text",
                                        "text":"robotics"
                                    },
                                    "value":"Robotics"
                                },
                                {
                                    "text":{
                                        "type":"plain_text",
                                        "text":"Software"
                                    },
                                    "value":"Software"
                                },
                                {
                                    "text":{
                                        "type":"plain_text",
                                        "text":"Hardware"
                                    },
                                    "value":"Hardware"
                                },
                                {
                                    "text":{
                                        "type":"plain_text",
                                        "text":"CAD"
                                    },
                                    "value":"CAD"
                                }
                            ],
                            "initial_options": [
                                {
                                    "text":{
                                        "type":"plain_text",
                                        "text":"Software"
                                    },
                                    "value":"Software"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    )

channel = {
    "Software":["code"],
    "Hardware":["hardware"],
    "Art":["art"],
    "CAD":["cad"]
}

@app.view("testdashboard")
def handle_view_submission_events(ack,body,logger):
    ack()

    logger.info(body)

    options = logger.info(body)

    length = len(options)
    print(length)

@app.command("/hellocleaner")
def hellocleaner(ack,say):
    ack()
    say("hello This is Cleaner, Let's clean your slack")

@app.command("/listchannel")
def channellist(ack , client , respond):
    ack()
    respond = client.conversations_list(
        types = "public_channel,private_channel,mpim,im",
    )
    for channel in respond['channels']:
        print(channel['name'])

if __name__ == "__main__" :
    SocketModeHandler(
        app,
        os.environ["SLACK_APP_TOKEN"]
    ).start()