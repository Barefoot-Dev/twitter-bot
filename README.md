This is a simple Twitter bot to automate the following of users based on terms in their tweets and number of followers.

# Install

`pip install -r requirements.txt`


# Usage

Create and fill a credentials.json and config.json, based on the example file of each, before running main.py. You will need to get the Twitter API keys from their developer portal.

In this package, each 'account' has a corresponding twitter handle, credentials, and config entry. 

### Follow accounts based on search terms in the config:
`python main.py -a <account`>


### Unfollow accounts:
`python unfollow.py -a <account>`