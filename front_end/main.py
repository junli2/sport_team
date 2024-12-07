from flask import Flask, jsonify, make_response
import requests

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
    url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams"
    response = requests.get(url)
    data = response.json()
    teams = {"teams": []}
    for t in data["sports"][0]["leagues"][0]["teams"]:
        team = {"id": t["team"]["id"], "name": t["team"]["displayName"]}
        teams["teams"].append(team)
    # teams = data["sports"][0]["leagues"][0]["teams"][0]["team"]["displayName"]
    json_teams = json.dump(teams, indent=4)
    app.logger.info("Retrieving all NFL teams from ESPN")
    return make_response(json_teams, 200)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
