from facebook_scraper import get_posts
import tweepy
import praw

from connectToDatabase import *
import datetime
import pandas as pd

workbookFilePath = ""
def crawl_Facebook_post(page_id, quantity):
    data_type = 'Post'
    page_id = page_id.lower()
    dataset = []
    exist_post_id = []
    count = 0
    exist_count = 0

    exist = check_crawler_workbook(page_id, data_type, "Facebook")
    if exist:
        exist_post_id = load_exist_postID(page_id, data_type, "Facebook")

    try:
        for post in get_posts(page_id, pages=quantity, options={"posts_per_page": 1, "allow_extra_requests": False}):
            if post['post_id'] in exist_post_id:
                print("Old post found!This is the id:", post['post_id'])
                exist_count += 1
            else:
                if count < quantity:
                    post_id = post['post_id']
                    text = post['text']
                    time = post['time']
                    post_date = time.strftime('%d-%m-%Y')
                    post_time = time.strftime('%H:%M:%S')
                    post_url = post['post_url']
                    author_id = post['user_id']
                    author_name = post['username']
                    date_now = datetime.date.today().strftime('%d-%m-%Y')
                    time_now = datetime.datetime.now().time().strftime('%H:%M:%S')
                    print('ID:', post_id)
                    # print('Text:', text)
                    # print('Created Date:', post_date)
                    # print('Created Time:', post_time)
                    # print('URL:', post_url)
                    # print('User_id:', author_id)
                    # print('Username:', author_name)

                    dataset.append([post_id, text, post_date, post_time, post_url, author_id, author_name, date_now,
                                    time_now])
                    count += 1
        print('Done crawl! Total crawl', str(count), ' new post"(s)"')
        return dataset, exist_count
    except:
        print('Invalid id')
        return False, exist_count


def get_date(created):
    date_time = datetime.datetime.fromtimestamp(created)
    return date_time.strftime('%d-%m-%Y'), date_time.strftime('%H:%M:%S')


def crawl_Reddit_post(topic, quantity):
    data_type = 'Post'
    topic = topic.lower()
    exist_post_id = []
    dataset = []
    count = 0
    exist_count = 0

    # get the API key
    log = pd.read_csv(workbookFilePath)
    API1, API2, API3, API4 = log['API_1'][1], log['API_2'][1], log['API_3'][1], log['API_4'][1]
    reddit = praw.Reddit(client_id=API1, client_secret=API2, user_agent='Dimon', username=API3, password=API4)

    exist = check_crawler_workbook(topic, data_type, "Reddit")

    if exist:
        exist_post_id = load_exist_postID(topic, data_type, "Reddit")

    try:
        subreddit = reddit.subreddit(topic)

        for post in subreddit.top(limit=quantity):
            if post.id in exist_post_id:
                print("Old post found!This is the id:", post.id)
                exist_count += 1
            else:
                ID = post.id
                title = post.title
                content = post.selftext
                url = reddit.config.reddit_url + post.permalink
                print("PostID", ID)
                # print("Title", title)
                # print("Body", content)
                # print("Link", url)
                try:
                    author_id = post.author.id
                    author_name = post.author.name
                except AttributeError:
                    author_id = "None"
                    author_name = "None"

                post_date, post_time = get_date(post.created)
                date_now = datetime.date.today().strftime('%d-%m-%Y')
                time_now = datetime.datetime.now().time().strftime('%H:%M:%S')
                dataset.append([ID, title, content, post_date, post_time, url, author_id, author_name, date_now, time_now])
                count += 1

        print('Done crawl! Total crawl', str(count), ' new post"(s)"')
        return dataset, exist_count
    except:
        return False, exist_count


def crawl_Twitter_post(keyword, quantity):
    data_type = 'Post'
    keyword = keyword.lower()
    exist_post_id = []
    dataset = []
    count = 0
    exist_count = 0

    # get the API key
    log = pd.read_csv(workbookFilePath)

    # Authentication
    consumerKey = log['API_1'][0]
    consumerSecret = log['API_2'][0]
    accessToken = log['API_3'][0]
    accessTokenSecret = log['API_4'][0]

    # Create the authentication object
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    # Set the access token and token secret
    auth.set_access_token(accessToken, accessTokenSecret)
    # create api object
    api = tweepy.API(auth, wait_on_rate_limit=True)

    exist = check_crawler_workbook(keyword, data_type, "Twitter")

    if exist:
        exist_post_id = load_exist_postID(keyword, data_type, "Twitter")

    try:
        posts = tweepy.Cursor(api.search, q=keyword, lang="en").items(quantity)
        for post in posts:
            if str(post.id) in exist_post_id:
                print("One old post found! This is the post id:", str(post.id))
                exist_count += 1
            else:
                post_date = post.created_at.strftime('%d-%m-%Y')
                post_time = post.created_at.strftime('%H:%M:%S')
                date_now = datetime.date.today().strftime('%d-%m-%Y')
                time_now = datetime.datetime.now().time().strftime('%H:%M:%S')
                print("PostID", post.id)
                # print("Post:", post.text)
                # print("Post user:", post.user.screen_name)
                # print("UserID", post.user.id)
                # print("Date", post_date)
                # print("time", post_time)
                dataset.append(
                    [str(post.id), post.text, post_date, post_time, "https://twitter.com/i/web/status/" + str(post.id),
                     str(post.user.id), post.user.screen_name, date_now, time_now])
                count += 1
        print('Done crawl! Total crawl', str(count), ' new post(s)')
        if not exist and not dataset:
            return False, exist_count
        return dataset, exist_count
    except:
        return False, exist_count


def crawl_post(key, quantity, platform):
    if platform == 'Facebook':
        return crawl_Facebook_post(key, quantity)
    elif platform == 'Twitter':
        return crawl_Twitter_post(key, quantity)
    elif platform == 'Reddit':
        return crawl_Reddit_post(key, quantity)
    else:
        return False, 0
