from gcp_wrappers.producer import publish_message
import json
import os

if __name__ == "__main__":
    BASE_DIR = "static"
    conversations = []
    for filename in os.listdir(BASE_DIR):
        if filename.endswith(".json") and "tangome" in filename:
            file_path = os.path.join(BASE_DIR, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                conversations.append(json.load(file))

    for conversation in conversations:
        for message in conversation:
            print(message)
            publish_message(message)