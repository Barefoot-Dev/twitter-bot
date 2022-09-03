This is a simple Twitter bot to automate the following and unfollowing based on keywords in tweets and follower/following numbers.

# Install

`pip install -r requirements.txt`


# Usage

In this package, each handle requires corresponding twitter  credentials and has its own config entry. 

Create and fill a credentials.json and config.json, based on the example file of each, before running main.py. You will need to get the Twitter API keys from their developer portal.


### Follow accounts based on search terms in the config:
`python follow.py -h <handle>`


### Unfollow accounts:
`python unfollow.py -h <handle>`