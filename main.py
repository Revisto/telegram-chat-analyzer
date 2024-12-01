from data_loader import load_chat_history
from data_processor import preprocess_data
from analyzer import (
    count_messages_by_sender,
    get_word_frequencies,
    count_emojis,
    get_monthly_message_counts,
    count_messages_by_sender_and_type,
    get_count_of_messages_edited,
    get_length_of_video_messages,
    get_length_of_voice_messages,
    get_most_forwarded_by_sender,
    get_most_common_sources_forwarded_from,
    get_most_first_messages,
    get_most_replies,
    get_most_replied_message,
    get_average_message_length,
    plot_activity_heatmap,
    get_reactions_count_by_user,
)


def main():
    file_path = "chat_history.json"
    df = load_chat_history(file_path)
    df = preprocess_data(df)

    print("Messages by sender:")
    print(count_messages_by_sender(df))

    print("\nMost common words (All):")
    print(get_word_frequencies(df))

    print("\nMost common words (You):")
    print(get_word_frequencies(df, sender="Revisto"))

    print("\nMost common words (Partner):")
    print(get_word_frequencies(df, sender="Your Partnet ID"))

    print("\nMost common emojis (All):")
    print(count_emojis(df))

    print("\nMost common emojis (You):")
    print(count_emojis(df, sender="Revisto"))

    print("\nMost common emojis (Partner):")
    print(count_emojis(df, sender="Your Partnet ID"))

    print("\nMonthly message count (All):")
    print(get_monthly_message_counts(df))

    print("\nMonthly message count (You):")
    print(get_monthly_message_counts(df, sender="Revisto"))

    print("\nMonthly message count (Partner):")
    print(get_monthly_message_counts(df, sender="Your Partnet ID"))

    print("\nMessage count by sender and type:")
    print(count_messages_by_sender_and_type(df))

    print("\nMessage count by sender and edited status:")
    print(get_count_of_messages_edited(df))

    print("\nTotal video message duration by sender:")
    print(get_length_of_video_messages(df))

    print("\nTotal voice message duration by sender:")
    print(get_length_of_voice_messages(df))

    print("\nMost forwarded messages by sender:")
    print(get_most_forwarded_by_sender(df))

    print("\nMost common sources forwarded from:")
    print(get_most_common_sources_forwarded_from(df))

    print("\nMost first messages:")
    print(get_most_first_messages(df))

    print("\nMost replies:")
    print(get_most_replies(df))

    print("\nMost replied message:")
    print(get_most_replied_message(df))

    print("\nAverage message length:")
    print(get_average_message_length(df))

    ("\nActivity heatmap:")
    plot_activity_heatmap(df)

    print("\nReactions count by user:")
    print(get_reactions_count_by_user(df))


if __name__ == "__main__":
    main()
