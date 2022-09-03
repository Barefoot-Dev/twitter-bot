import json
import tweepy


def get_api(account):

    with open("./credentials.json") as f:
        credentials = json.load(f)

    api_key = credentials[account]["API_KEY"]
    api_secret = credentials[account]["API_SECRET"]
    access_token = credentials[account]["ACCESS_TOKEN"]
    access_token_secret = credentials[account]["ACCESS_TOKEN_SECRET"]

    tweepy_auth = tweepy.OAuthHandler(api_key, api_secret)
    tweepy_auth.set_access_token(access_token, access_token_secret)
    # client = tweepy.Client(tweepy_auth)
    api = tweepy.API(tweepy_auth)
    return api


def get_config():
    with open("./config.json") as f:
        config = json.load(f)
    return config
