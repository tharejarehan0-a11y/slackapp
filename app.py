import os 
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import random
from supabase import create_client, Client


load_dotenv()

app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"],
)

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

@app.command("/clear")
def clear_database(ack,body,client,logger):
    ack()
    if body["user_id"] == ( "U0A2L9T7C12" ):
        try:
             response = supabase.table("suggestions").delete().neq("topic","I am Rehan").execute()
             client.chat_postMessage(
                 channel = body["user_id"],
                 text = "Table Cleared successfully thanks"
             )
        except Exception as e:
           print(e)
        logger.info(body)

@app.command("/suggestion")
def main_modal(ack,body,client):
    ack()
    client.views_open(
        trigger_id=body["trigger_id"],
        view = {
            "type": "modal",
            "callback_id":"debate_modal",
            "title": {"type": "plain_text", "text": "Debator", "emoji": True},
            "submit": {"type": "plain_text", "text": "Submit", "emoji": True},
            "close": {"type": "plain_text", "text": "Cancel", "emoji": True},
            "blocks": [
                {
                    "type": "header",
                    "text": {"type": "plain_text", "text": "Please tell about your topic", "emoji": True}
                },
                {
                    "type": "input",
                    "block_id": "topic_block",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "plain_text_input-action"
                    },
                    "label": {"type": "plain_text", "text": "Topic", "emoji": True},
                    "optional": False
                }
            ]
        }
    )

user_ids = []
submitted_topics = []
choosed_topics = []

@app.command("/topics-please")
def select_topics(ack,body,client,logger):
     ack()
     logger.info(body)
     if body["user_id"] == os.environ.get("EVAN_USER_ID"):
          count_topics = supabase.table("suggestions").select("*",count="exact").limit(1).execute()
          total_topics = count_topics.count

          if total_topics == 0:
               client.chat_postMessage(
                    channel = body["user_id"],
                    text = "No one submitted topics yet sorry for that"
               )
          else:
              client.chat_postMessage(
                   channel = body["user_id"],
                   text = f"hi <@{body['user_id']}> how are u"
                )
              
              needed_topics = min(3, total_topics)
              
              while len(choosed_topics) < needed_topics:
                  random_number = random.randint(0,total_topics-1)
                  random_row = supabase.table("suggestions").select("topic").range(random_number,random_number).execute()
                  
                  if len(random_row.data) > 0:
                      random_topic = random_row.data[0]["topic"]

                      if random_topic in choosed_topics:
                           print("already there")
                           continue
                      else:
                          choosed_topics.append(random_topic)
                          
                          client.chat_postMessage(
                               channel = body["user_id"],
                               text = f"Topic {len(choosed_topics)} is {random_topic}"
                          )
                          print(choosed_topics)
                  else:
                       client.chat_postMessage(
                            channel = body["user_id"],
                            text = f"oops <@{body['user_id']}> topic for some reason has no text"
                       )
              choosed_topics.clear()

     else:
          client.chat_postMessage(
               channel = body["user_id"],
               text = f"U are not authorized for this Sorry <@{body['user_id']}>"
          )

@app.view("debate_modal")
def handle_submission(ack, body, client, view, logger):
    ack()

    user_id = body["user"]["id"]
    submitted_topic = view["state"]["values"]["topic_block"]["plain_text_input-action"]["value"]
    print (submitted_topic)

    print(f"User submitted: {submitted_topic}")
  
    logger.info(f"{user_id} submitted topic {submitted_topic}")
            
    submitted_topics.append(submitted_topic)
    user_ids.append(user_id)

    try:
            response = supabase.table("suggestions").insert({
                "slack_user_id": user_id,
                "topic": submitted_topic
            }).execute()
            client.chat_postMessage(
                channel=user_id,
                text=f"Thanks for your submission <@{user_id}>"
            )
                
            if len(response.data) > 0:
                print(f"Success! Added to database: {response.data}")
            else:
                print("Something went wrong, no data was returned.")
                    
    except Exception as e:
        if e.message == 'duplicate key value violates unique constraint "suggestions_slack_user_id_key"':
             client.chat_postMessage(
                  channel=user_id,
                  text=f"Sorry but you already submitted <@{user_id}>"
             )
        else:
           print(f"DATABASE INSERT ERROR: {e}")
           logger.info(f"the error was {e}")
        
if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()