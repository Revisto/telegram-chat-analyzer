import pandas as pd
import json


def load_chat_history(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    messages = data["messages"]
    df = pd.DataFrame(messages)
    return df
