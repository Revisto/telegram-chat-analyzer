import pandas as pd
import re


def preprocess_data(df):
    df = df.dropna(subset=["from", "text"]).copy()

    def normalize_text(text):
        if isinstance(text, str):
            text = text.replace("\n", "")
            # Normalize repeated characters
            text = re.sub(r"(.)\1+", r"\1", text)
        return text

    df.loc[:, "text"] = df["text"].apply(normalize_text)
    return df
