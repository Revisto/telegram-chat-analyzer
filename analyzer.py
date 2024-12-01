import pandas as pd
from collections import Counter
import re
import emoji
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter


def count_messages_by_sender(df):
    return df["from"].value_counts()


def count_messages_by_sender_and_type(df):
    return df.groupby(["from", "media_type"]).size()


def get_character_counts(df, sender=None):
    if sender:
        df = df[df["from"] == sender]
    text_data = df["text"].apply(lambda x: x if isinstance(x, str) else "")
    all_text = "".join(text_data)
    character_counts = Counter(all_text)
    return character_counts


def get_monthly_message_counts(df, sender=None):
    if sender:
        df = df.reset_index()
        df = df[df["from"] == sender]
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    monthly_counts = df.resample("M").size()
    plt.figure(figsize=(10, 6))
    monthly_counts.plot(kind="bar", color="skyblue")
    plt.title(f'Monthly Message Counts {"for " + sender if sender else ""}')
    plt.xlabel("Month")
    plt.ylabel("Message Count")
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_formatter(
        plt.FixedFormatter(monthly_counts.index.strftime("%b %Y"))
    )
    plt.tight_layout()
    plt.show()

    return monthly_counts


def get_count_of_messages_edited(df):
    edited_messages = df[df["edited"].notnull()]
    edited_count = edited_messages["from"].value_counts()
    return edited_count


def get_length_of_video_messages(df):
    video_messages = df[df["media_type"] == "video_message"]
    duration_by_sender = video_messages.groupby("from")["duration_seconds"].sum()
    return duration_by_sender


def get_length_of_voice_messages(df):
    audio_messages = df[df["media_type"] == "voice_message"]
    duration_by_sender = audio_messages.groupby("from")["duration_seconds"].sum()
    return duration_by_sender


def get_word_frequencies(df, sender=None):
    if sender:
        df = df[df["from"] == sender]
    text_data = df["text"].apply(lambda x: x if isinstance(x, str) else "")
    all_words = " ".join(text_data).lower()
    words = re.findall(r"\w+", all_words)
    word_counts = Counter(words)
    return word_counts.most_common(10)


def count_emojis(df, sender=None):
    if sender:
        df = df[df["from"] == sender]
    text_data = df["text"].apply(lambda x: x if isinstance(x, str) else "")
    all_text = "".join(text_data)
    emojis_list = [char for char in all_text if char in emoji.EMOJI_DATA]
    emoji_counts = Counter(emojis_list)

    for emoji_char, count in emoji_counts.most_common(10):
        print(f"{emoji_char}: {count}")

    return emoji_counts.most_common(10)


def get_most_forwarded_by_sender(df):
    forwarded_messages = df[df["forwarded_from"].notnull()]
    forwarded_count = forwarded_messages["from"].value_counts()
    return forwarded_count


def get_most_common_sources_forwarded_from(df):
    forwarded_messages = df[df["forwarded_from"].notnull()]
    common_sources = forwarded_messages.groupby("from")["forwarded_from"].apply(
        lambda x: x.value_counts().head(10)
    )
    return common_sources


import pandas as pd


def get_most_first_messages(df):
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(by=["from", "date"])
    df["time_diff"] = df.groupby("from")["date"].diff()
    first_messages = df[df["time_diff"] > pd.Timedelta(minutes=60)]
    first_message_count = first_messages["from"].value_counts()
    return first_message_count


def get_most_replies(df):
    reply_messages = df[df["reply_to_message_id"].notnull()]
    reply_count = reply_messages["from"].value_counts()
    return reply_count


def get_most_replied_message(df):
    reply_messages = df[df["reply_to_message_id"].notnull()]
    reply_counts = (
        reply_messages.groupby("reply_to_message_id")
        .size()
        .reset_index(name="reply_count")
    )
    merged_df = df.merge(
        reply_counts, left_on="id", right_on="reply_to_message_id", how="left"
    )
    top_10_replied_messages_by_user = (
        merged_df.groupby("from")
        .apply(lambda x: x.nlargest(10, "reply_count"))
        .reset_index(drop=True)
    )
    return top_10_replied_messages_by_user


def get_average_message_length(df):
    df["message_length"] = df["text"].apply(lambda x: len(str(x)))
    avg_length = df.groupby("from")["message_length"].mean()
    return avg_length


def plot_activity_heatmap(df):
    df["date"] = pd.to_datetime(df["date"])
    df["hour"] = df["date"].dt.hour
    df["day_of_week"] = df["date"].dt.day_name()
    pivot = df.pivot_table(
        index="day_of_week", columns="hour", values="id", aggfunc="count"
    ).fillna(0)
    days_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    pivot = pivot.reindex(days_order)
    plt.figure(figsize=(12, 6))
    sns.heatmap(pivot, cmap="Blues")
    plt.title("Message Activity Heatmap")
    plt.show()


def get_reactions_count_by_user(df):
    reactions_data = []
    for _, row in df.iterrows():
        if "reactions" in row and isinstance(row["reactions"], list):
            for reaction in row["reactions"]:
                if "emoji" in reaction:
                    for recent in reaction["recent"]:
                        reactions_data.append(
                            {"from": recent["from"], "emoji": reaction["emoji"]}
                        )

    reactions_df = pd.DataFrame(reactions_data)
    reactions_count_by_user = reactions_df["from"].value_counts()
    for user, count in reactions_count_by_user.items():
        print(f"{user}: {count}")
    return reactions_count_by_user
