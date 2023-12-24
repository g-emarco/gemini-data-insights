from langchain.llms import VertexAI
import json

from langchain_core.prompts import PromptTemplate

llm = VertexAI(model_name="gemini-pro")

if __name__ == "__main__":
    print(llm("hello how r u "))

import ast
import base64

from cloudevents.http import CloudEvent
import functions_framework

# {'message_id': '008', 'timestamp': '2023-12-23T10:12:00Z', 'sender': 'buyer456', 'text': 'I see your point. Do you have a platform in mind?'}


def process_pubsub_message(event, context):
    pubsub_message = base64.b64decode(event["data"]).decode("utf-8")
    print(f"Received message: {pubsub_message}")
    message_text = pubsub_message["text"]
    llm = VertexAI(model_name="gemini-pro")


@functions_framework.cloud_event
def subscribe(cloud_event: CloudEvent) -> None:
    # Print out the data from Pub/Sub, to prove that it worked
    print("******")
    decoded_str = base64.b64decode(cloud_event.data["message"]["data"]).decode("utf-8")
    print(f"{decoded_str=}")
    message_dict = ast.literal_eval(decoded_str)
    print(f"{message_dict=}")

    template = (
        "You are a helpful assitant with the goal of detecting if there is an attempt to move a transaction of the Fiverr marketplace."
        "Given the the message {text} you should determine wether there is such an attempt to start a zoom session / google meet session/ phone call"
        "outside of the fiverr platform."
        "Your answer should be YES or NO."
    )

    prompt = PromptTemplate.from_template(template)
    llm = VertexAI(model_name="gemini-pro")
    chain = prompt | llm
    is_disintermediation = chain.invoke({"text": message_dict["text"]})
    if is_disintermediation == 'YES':
        print("Detected disintermediation")
    else:
        print("Message valid")
