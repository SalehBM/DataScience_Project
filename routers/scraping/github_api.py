from datetime import datetime
import requests
import json
import re

def github_user(user):
    req = requests.get(f'https://api.github.com/users/{user}')
    jsn = json.loads(req.text)
    if jsn.get("message") == None:
        return jsn
    else:
        raise Exception("Github Not Found!")

def get_twitter(req):
    twitter = req.get("twitter_username")
    if twitter == None:
        return False
    return True

def get_followers(req):
    return int(req.get("followers"))

def get_following(req):
    return int(req.get("following"))

def get_projects(req):
    return int(req.get("public_repos"))

def get_user_date(req):
    return datetime.strptime(re.findall(r"\d{4}-\d{2}-\d{2}", req.get("created_at"))[0], "%Y-%m-%d")

def social_rating(req, connections):
    user_creation = (datetime.now() - get_user_date(req)).days
    following, followers = get_following(req), get_followers(req)
    if user_creation > 250:
        user_creation = 250
    if following > 50:
        following = 50
    if followers > 50:
        followers = 50
    if connections > 100:
        connections = 100
    return (0.35 * (user_creation / 50) + 0.1 * get_following(req) + 0.1 * get_followers(req) + 0.05 *  int(get_twitter(req)) + 0.4 * (connections / 20))
