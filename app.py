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
	"type": "modal",
    "callback_id": "submission",
	"title": {
		"type": "plain_text",
		"text": "My App",
		"emoji": True
	},
	"submit": {
		"type": "plain_text",
		"text": "Submit",
		"emoji": True
	},
	"close": {
		"type": "plain_text",
		"text": "Cancel",
		"emoji": True
	},
	"blocks":[
		{
			"type": "actions",
			"elements": [
				{
					"type": "checkboxes",
					"options": [
						{
							"text": {
								"type": "plain_text",
								"text": "Software",
								"emoji": True
							},
							"value": "value-0"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "Hardware",
								"emoji": True
							},
							"value": "value-1"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "CAD",
								"emoji": True
							},
							"value": "value-2"
						}
					],
					"action_id": "channel_checkboxes"
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

@app.action("channel_checkboxes")
def handle_channels(ack,body,logger):
    ack()
    logger.info(body)

@app.view("submission")
def handle_view_submission(ack, body, logger):
    ack()  
    logger.info(body)
    optiontable = body['view']['state']['values']['P5FdQ']['channel_checkboxes']['selected_options']
    options= []
    for x in range(0,len(optiontable)):
        options.append(optiontable[x]['text']['text'])
    print(options)


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