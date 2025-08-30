from flask import Flask, request, jsonify
from flask_cors import CORS
from game import Minesweeper

app = Flask(__name__)
CORS(app)

game = None

@app.route("/start", methods=["POST"])
def start_game():
    global game
    data = request.get_json()
    game = Minesweeper(
        rows=data.get("rows", 10),
        cols=data.get("cols", 10),
        mines=data.get("mines", 10)
    )
    return jsonify(game.get_state())

@app.route("/reveal", methods=["POST"])
def reveal():
    global game
    data = request.get_json()
    result = game.reveal_cell(data["x"], data["y"])
    return jsonify({"result": result, **game.get_state()})

@app.route("/flag", methods=["POST"])
def flag():
    global game
    data = request.get_json()
    game.flag_cell(data["x"], data["y"])
    return jsonify(game.get_state())

if __name__ == "__main__":
    app.run(debug=True)