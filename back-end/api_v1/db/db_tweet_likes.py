from .db_utils import get, put, put_return_id, put_return_row_count

def get_likes_by_tweet_id(tweet_id):
    likes = get("""
        SELECT
	        tweetId,
            userId,            
            username
        FROM
        (
            SELECT
                Id,
                Username as username
            FROM
                Users
        ) AS User
        JOIN (
            SELECT
                Id AS tweetId,
                User_Id as userId
            FROM
                Tweet_Likes
            WHERE
                tweetId = (?)
        ) AS Tweet_Likes ON  Tweet_Likes.userId = User.Id
        """, [tweet_id])
    return likes

def get_all_likes():
    pass

def create_like(tweet_id, user_id):
    put("""
    INSERT INTO
        Tweet_Likes (Tweet_Id, User_Id)
    VALUES (?, ?)""", [tweet_id, user_id])

def like_exists(tweet_id, user_id):
    like = get("""
        SELECT
            *
        FROM
            Tweet_Likes
        WHERE
            Tweet_Id = (?)
            AND User_Id = (?)""", [tweet_id, user_id])
    
    if like:
        return True
    else:
        return False

def delete_like(tweet_like_id):
    pass