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



@app.command("/addme")
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

@app.action("channel_checkboxes")
def handle_channels(ack,body,logger):
    ack()
    logger.info(body)

@app.view("submission")
def handle_view_submission(ack, body, logger,client):
    ack()  
    logger.info(body)
    optiontable = body['view']['state']['values']['P5FdQ']['channel_checkboxes']['selected_options']
    user_id = body["user"]["id"]
    print(user_id)
    options = []
    for x in range(0,len(optiontable)):
        options.append(optiontable[x]['text']['text'])
    print(options)

    if options.__contains__("Hardware"):
        try:
            client.conversations_invite(
                channel='C6C026NHJ',
                users = user_id
            )
        except:
            client.chat_postMessage(
                channel = user_id,
                text = "Oooo you are already there in the Hardware channels !!! "
            )

    if options.__contains__("Software"):
        try:
            client.conversations_invite(
                channel='C0EA9S0A0',
                users = user_id
            )
        except:
            client.chat_postMessage(
                channel = user_id,
                text = "Oooo you are already there in the Software channels !!! "
            )
    if options.__contains__("CAD"):
        try:
            client.conversations_invite(
                channel='C06DMUYHE5S',
                users = user_id
            )
        except:
            client.chat_postMessage(
                channel = user_id,
                text = "Oooo you are already there in the CAD channels !!! "
            )

@app.command("/helloclensie")
def hellocleaner(ack,say):
    ack()
    say("hello This is Clensie, Let's clean your slack")


if __name__ == "__main__" :
    SocketModeHandler(
        app,
        os.environ["SLACK_APP_TOKEN"]
    ).start()