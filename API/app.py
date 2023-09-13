import os
import openai
import json
from flask import Flask, jsonify
from flask_cors import CORS
from flask_caching import Cache
from espn_api.football import League


with open('secrets.json', 'r') as f:
    secrets = json.load(f)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:*"}})

# Configuring cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Initialize the league object
league = League(league_id='749873851', year=2023, espn_s2=secrets["ESPN_S2"], swid=secrets["SWID"])

# Initialize OpenAI API
# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = secrets["OPENAI_API_KEY"]

def generate_summary(matchup):
    home_team = matchup['home_team']
    away_team = matchup['away_team']
    home_score = matchup['home_score']
    away_score = matchup['away_score']
    
    prompt = f"Generate a snarky summary for a fantasy football matchup between {home_team} and {away_team} where {home_team} scored {home_score} and {away_team} scored {away_score}."
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )
    
    summary = response.choices[0].text.strip()
    return summary

def fetch_last_week_matchups():
    last_week = league.current_week - 1
    box_scores = league.box_scores(week=last_week)
    matchups = []
    
    for box_score in box_scores:
        home_team = box_score.home_team
        away_team = box_score.away_team
        home_score = box_score.home_score
        away_score = box_score.away_score
        
        matchup = {
            "home_team": home_team.team_name,
            "away_team": away_team.team_name,
            "home_score": home_score,
            "away_score": away_score,
        }
        
        summary = generate_summary(matchup)
        
        matchup['summary'] = summary
        matchups.append(matchup)
    
    return matchups

@app.route('/last_week_matchups', methods=['GET'])
@cache.cached(timeout=3600)  # cache for 1 hour
def last_week_matchups():
    matchups = fetch_last_week_matchups()
    return jsonify(matchups)

if __name__ == '__main__':
    app.run(debug=True)