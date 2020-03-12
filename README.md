# De-Dash Data Engineering Backend API

## API Endpoints
/health, GET, API endpoint health check, return 200

/user, POST, JSON {username: “<username>”}
Return: {history: {arr of timestamps}, 
              topComments: {arr of {karma: int, comment: str}, len 5},
        worstComments: {arr of {karma: int, comment: str}, len 5},
  wordCloud: {arr of {count: int, word: str}},
  trending: {array of {story: id}} // intersection user’s post AND top, new, trending
  stats: {totalComments: int, totalStories: int}
  }
     Fail: Response 204

/story, POST, JSON {storyID: int}
        Return: {story: {timestamp: timestamp, score: float}}
    Fail: Response 204

## Design doc
https://docs.google.com/document/d/1oPj6pcYtW1bfb_iYAIu6NUknyhDvyybfHTakk_zhEZ0

