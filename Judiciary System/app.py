from flask import Flask, request
from final import ipc_suggest, case_reccomender
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)
app.config["CORS_HEADERS"] = "Content-Type"


@app.route("/")
@cross_origin()
def homepage():
    return {"message": "Hello World"}


@app.route("/ipc", methods=["POST"])
def ipc_suggestions():
    text = request.json["description"]
    output = ipc_suggest(text)
    return {"ipc": output}


@app.route("/cases", methods=["POST"])
def case_suggestions():
    text = request.json["text"]
    date = request.json["date"]
    output = case_reccomender(date, text)
    return {"cases": output}


if __name__ == "__main__":
    app.run(debug=True)
