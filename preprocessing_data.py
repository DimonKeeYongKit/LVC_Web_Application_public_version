from textblob import TextBlob
from nltk.tokenize import sent_tokenize
import re
import emoji


def tagging(text):
    if text is not None:
        send_token_list = sent_tokenize(text)

        tag_token_list = []

        for token in send_token_list:
            content = TextBlob(token)
            tag_token_list.append(content.pos_tags)

        return tag_token_list
    else:
        return 'None'


def cleanText(text):
    if text is not None:
        text = re.sub(r"@[A-Za-z0-9_-]+", '', text)  # remove tag
        text = re.sub(r"#[A-Za-z0-9_-]+", '', text)  # remove hashtag
        text = re.sub(r"https?:\/\/\S+", '', text)  # remove hyperlink
        text = re.sub(r"[\n]+", '', text)  # remove next line
        text = re.sub(r'RT', '', text)  # remove RT
        text = re.sub(r'[0-9]+', '', text)  # remove numbering
        text = text.replace('[OC]', '')  # remove [OC]
        return text
    else:
        return 'None'


def remove_emoji(text):
    if text is not None:
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   u"\U0001f926-\U0001f937"
                                   u'\U00010000-\U0010ffff'
                                   u"\u200d"
                                   u"\u2640-\u2642"
                                   u"\u2600-\u2B55"
                                   u"\u23cf"
                                   u"\u23e9"
                                   u"\u231a"
                                   u"\u3030"
                                   u"\ufe0f"
                                   "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', text)
    else:
        return 'None'


def give_emoji_free_text(text):
    return emoji.get_emoji_regexp().sub(r'', text.decode('utf8'))


def lower_and_punctuation_process(text):
    if text is not None:
        text = text.lower()
        pattern1 = re.compile("["
                              u"\u0041-\u005A"  # unicode A to Z
                              u"\u0061-\u007A"  # unicode a to z
                              u"\u0027"  # unicode Apostrophe
                              u"\u002C"  # unicode Comma
                              u"\u002E"  # unicode Full stop
                              u"\u002D"  # unicode Hyphen-minus
                              '’'
                              '-'
                              '_'
                              '.'
                              '!'
                              '?'
                              "]+", flags=re.UNICODE)
        # using list comprehension
        return ' '.join([str(elem) for elem in pattern1.findall(text)])
    else:
        return 'None'


def full_preprocessing(text):

    output1 = cleanText(text)
    print('Out1:', output1)
    output2 = remove_emoji(output1)
    # print('Out2:', output2)
    output3 = lower_and_punctuation_process(output2)
    # print('Out3:', output3)
    output4 = tagging(output3)
    # print('Out4:', output4)
    return output3, output4

