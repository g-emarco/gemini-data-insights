import ast
import base64

from cloudevents.http import CloudEvent
import functions_framework
from google.cloud import firestore
from langchain_core.prompts import PromptTemplate

from langchain_google_vertexai import ChatVertexAI

llm = ChatVertexAI(model_name="gemini-pro")

if __name__ == "__main__":
    print(llm.invoke("hello how r u "))



# {'message_id': '008', 'timestamp': '2023-12-23T10:12:00Z', 'sender': 'buyer456', 'text': 'GOALLL'}

db = firestore.Client(database="firestore1")

def process_pubsub_message(event, context):
    pubsub_message = base64.b64decode(event["data"]).decode("utf-8")
    print(f"Received message: {pubsub_message}")
    message_text = pubsub_message["text"]
    llm = ChatVertexAI(model_name="gemini-pro")

def fetch_prompt_from_firestore():
    doc_ref = db.collection('analsysis-queries').document('pPpx8y3za2kHgxKsmbk9')
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict().get('prompt', '')
    else:
        raise ValueError("Document does not exist in Firestore")


@functions_framework.cloud_event
def subscribe(cloud_event: CloudEvent) -> None:
    # Print out the data from Pub/Sub, to prove that it worked
    print("******")
    decoded_str = base64.b64decode(cloud_event.data["message"]["data"]).decode("utf-8")
    print(f"{decoded_str=}")
    message_dict = ast.literal_eval(decoded_str)
    print(f"{message_dict=}")

    template = (
        "You are a helpful assitant with the goal of detecting if there is an attempt to move a transaction of the tangome platfrom."
        "Given the the message {text} you should determine wether there is such an attempt to start a conversation on another platform"
        "like zoom session / google meet session/ phone call or either to transfer money/ funds/ gifst outside"
        "of the tangome platform such as using other paymenr vendors paypal/payoneer/vinmo etc."
        "The users might obfuscate the vendor name so try and see through that like P$YP$L "
        "Your answer should be only YES or NO."
        "Your answer should be only YES or NO."
        "Your answer should be only YES or NO."
        "Your answer should be only YES or NO."
        "Your answer should be only YES or NO."
    )

    try:
        template = fetch_prompt_from_firestore()
        print(f"prompt from firestore is {template=}")
    except Exception as e:
        print(f"Error fetching prompt from Firestore: {e}")
        print(f"Using default prompt")

    prompt = PromptTemplate.from_template(template)
    llm = ChatVertexAI(model_name="gemini-pro")
    chain = prompt | llm
    is_disintermediation = chain.invoke({"text": message_dict["text"]})
    print(is_disintermediation)
    if is_disintermediation == 'YES':
        print("Detected disintermediation")
    else:
        print("Message valid")
