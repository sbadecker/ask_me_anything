import os

import requests

from utils import load_json, save_json


class TwitterApi:
    def __init__(self, timeline_params_path="timeline_params.json"):
        self.bearer_token = self._auth()
        self.headers = self._create_headers()
        self.timeline_params = load_json(timeline_params_path)

    def build_user_dataset(self, user_name, params=None, data_dir="data"):
        user_id = self.get_user_id_by_name(user_name)
        tweets = self.get_user_tweets(user_id, params)
        n_tweets = len(tweets)
        filepath = os.path.join(data_dir, f"{user_name}_{n_tweets}_tweets.json")
        save_json(tweets, filepath)
        print(f"{n_tweets} tweets queried and stored.")

    def get_user_tweets(self, user_id, params=None):
        url = f"https://api.twitter.com/2/users/{user_id}/tweets"
        tweets = []
        timeline_params = self.timeline_params.copy()
        if params:
            timeline_params.update(**params)
        json_response = self.connect_to_endpoint(url, self.headers, timeline_params)
        tweets.extend(json_response["data"])
        while json_response["meta"].get("next_token"):
            next_token = json_response["meta"]["next_token"]
            timeline_params.update({"pagination_token": next_token})
            json_response = self.connect_to_endpoint(url, self.headers, timeline_params)
            tweets.extend(json_response["data"])
            n_tweets = len(tweets)
            if n_tweets % 1000 == 0:
                print(f"{n_tweets} queried.")
        return tweets

    def get_user_id_by_name(self, user_name, params={"user.fields": "id"}):
        url = f"https://api.twitter.com/2/users/by/username/{user_name}"
        json_response = self.connect_to_endpoint(url, self.headers, params)
        user_id = json_response["data"]["id"]
        return user_id

    def connect_to_endpoint(self, url, headers, params):
        response = requests.request("GET", url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(
                f"Request returned an error: {response.status_code} {response.text}"
            )
        return response.json()

    def _auth(self):
        return os.environ.get("BEARER_TOKEN")

    def _create_headers(self):
        headers = {"Authorization": "Bearer {}".format(self.bearer_token)}
        return headers


def main():
    user_name = "stdecker"
    twitter_api = TwitterApi()
    user_id = twitter_api.get_user_id_by_name(user_name)
    user_tweets = twitter_api.get_user_tweets(user_id)
    pprint(user_tweets)


if __name__ == "__main__":
    main()
