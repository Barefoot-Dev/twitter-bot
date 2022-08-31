def check_account(
    tweepy_api,
    user,
    my_handle,
    min_followers=500,
    min_friends=500,
    max_followers=20000,
    max_friends=20000,
):

    try:
        followers_count = user.followers_count
        friends_count = user.friends_count
        screen_name = user.screen_name
    except AttributeError:
        followers_count = user["followers_count"]
        friends_count = user["friends_count"]
        screen_name = user["screen_name"]

    if min_followers < followers_count < max_followers:
        if min_friends < friends_count < max_friends:
            if followers_count < friends_count:
                friendship = tweepy_api.get_friendship(
                    source_screen_name=my_handle,
                    target_screen_name=screen_name,
                )[0]
                if not friendship.following:
                    return True
                else:
                    print("already following", screen_name)

    return False


def get_current_handles_followed():

    user = tweepy_api.get_user(screen_name=SCREEN_NAME)
    user_id = user.id
    followed = []
    cursor = -1
    for i in range(100):
        time.sleep(20)
        page_res = tweepy_api.get_friends(user_id=user_id, cursor=cursor)

        followed.extend([f.id for f in page_res[0]])
        cursor = page_res[1][1]

        if len(page_res[0]) < 20:  # last page
            break

        print("got {} followed".format(len(followed)))

    print("finished")

    # write list to json
    with open("followed.json", "w") as f:
        json.dump(followed, f)
