from flask import Blueprint, jsonify, make_response, request
from flask_api import status
from ..security.sec_utils import token_required, api_key_required
from ..db import db_tweets

tweets = Blueprint('/api/tweets', __name__)

@tweets.route("/api/tweets", methods=["GET"])
@api_key_required
def get_tweets():
    user_id = None

    if request.args:
        user_id = request.args["userId"]
        
    # Get Tweets by User Id
    if user_id:
        user_tweets = db_tweets.get_tweets_by_user_id(user_id)             
        if user_tweets:
            return make_response(jsonify(user_tweets), status.HTTP_200_OK)
        else:
            return make_response(jsonify({"message": "User not found"}), status.HTTP_404_NOT_FOUND)
            
    # Get all Tweets
    else:
        result = db_tweets.get_all_tweets()
        if not result:
            return make_response(jsonify({"message": "No results found"}), status.HTTP_404_NOT_FOUND)
        else:
            return make_response(jsonify(result), status.HTTP_200_OK)

@tweets.route("/api/tweets", methods=["POST"])
@api_key_required
@token_required
def create_tweet(user_id):   
    try:
        data = request.get_json()
        content = data["content"]

        new_tweet_id = db_tweets.create_tweet(user_id, content)

        new_tweet = db_tweets.get_tweet_by_id(new_tweet_id)        

        return make_response(jsonify(new_tweet), status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return make_response("", status.HTTP_500_INTERNAL_SERVER_ERROR)

@tweets.route("/api/tweets", methods=["DELETE"])
@api_key_required
@token_required
def delete_tweet(user_id):   
    try:
        data = request.get_json()
        tweet_id = data["tweetId"]
        deleted = db_tweets.delete_tweet(user_id, tweet_id)

        if deleted != 1:
            return make_response("", status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return "", status.HTTP_204_NO_CONTENT
    except Exception as e:
        print(e)
        return make_response("", status.HTTP_500_INTERNAL_SERVER_ERROR)

@tweets.route("/api/tweets", methods=["PATCH"])
@api_key_required
@token_required
def update_tweet(user_id):
    try:
        data = request.get_json()
        tweet_id = data["tweetId"]
        content = data["content"]

        db_tweets.update_tweet(user_id, tweet_id, content)
    except Exception as e:
        print(e)
        return make_response("", status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        tweet = db_tweets.get_brief_tweet_by_id(tweet_id)
        return make_response(jsonify(tweet), status.HTTP_200_OK)