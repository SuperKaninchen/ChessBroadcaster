from flask import Flask, request
import chess
import chess.svg


app = Flask(__name__)
board = chess.Board()


@app.route("/show")
def displayBoard():
    svgdata = chess.svg.board(board)
    return f"<meta http-equiv=\"refresh\" content=\"1\"><svg>{svgdata}</svg>"


@app.post('/updateBoard')
def updateBoard():
    move_string = request.data.decode()
    print("Received move: " + move_string)
    move_uci = chess.Move.from_uci(move_string)
    board.push(move_uci)
    return "Success"


def runApp(config):
    app.run(host=config["host"], port=config["port"])


if __name__ == "__main__":
    runApp("127.0.0.1", 5001)  # Run flask app with default config
