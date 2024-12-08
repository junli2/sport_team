from flask import Flask, jsonify, make_response, Response, request
import requests
import json

app = Flask(__name__)

@app.route('/')
def main():
    app.logger.info("Sport Team!!!")
    response = {
        "message": "Sport Team!!!!",
        "status": "success",
    }
    return make_response(jsonify(response), 200)

@app.route('/login')
def login():
    return '<center><h2>Welcome to Sport Team</h2></center><h3>Hello team player!</h3>'

@app.route('/health')
def health_check():
    app.logger.info("Health Check")
    health_status = {
        "status": "healthy",
    }
    return make_response(jsonify(health_status), 200)

@app.route('/teams')
def teams():
    app.logger.info("Retrieving all NFL teams from ESPN")
    try:
        url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams"
        response = requests.get(url)
        data = response.json()
        teams = {"teams": []}
        for t in data["sports"][0]["leagues"][0]["teams"]:
            team = {"id": t["team"]["id"], "name": t["team"]["displayName"]}
            teams["teams"].append(team)
        # json_teams = json.dumps(teams, indent=4)
        return make_response(jsonify(teams), 200)
    except Exception as e:
        app.logger.error("Failed to retrieve NFL teams from ESPN: %s", str(e))
        return make_response(jsonify({'error': str(e)}), 500)

@app.route('/team-schedule/<int:team_id>', methods=['GET'])
def team_schedule(team_id: int) -> Response:
    app.logger.info("Retrieving the team schedule from ESPN")
    try:
        url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}/schedule"
        response = requests.get(url)
        data = response.json()
        events = {"events": []}
        for e in data["events"]:
            event = {"week": e["week"]["text"], "date": e["date"], "name": e["name"]}
            events["events"].append(event)
        return make_response(jsonify(events), 200)
    except Exception as e:
        app.logger.error("Failed to retrieve the team schedule from ESPN: %s", str(e))
        return make_response(jsonify({'error': str(e)}), 500)

@app.route('/team-roster/<int:team_id>', methods=['GET'])
def team_roster(team_id: int) -> Response:
    app.logger.info("Retrieving the team roster from ESPN")
    try:
        url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}/roster"
        response = requests.get(url)
        data = response.json()
        roster = {"athletes": []}
        for p in data["athletes"]:
            for a in p["items"]:
                athlete = {"name": a["displayName"], "position": p["position"]}
                roster["athletes"].append(athlete)
        return make_response(jsonify(roster), 200)
    except Exception as e:
        app.logger.error("Failed to retrieve the team roster from ESPN: %s", str(e))
        return make_response(jsonify({'error': str(e)}), 500)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
