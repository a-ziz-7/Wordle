from flask import Flask, request, jsonify, render_template
import re

app = Flask(__name__)

# Load words into an array
with open("words.txt", "r") as file:
    words = [line.strip() for line in file]

# Helper function to filter words based on the pattern
def match_pattern(pattern):
    # Replace underscores with '.' to match any character
    regex_pattern = pattern.replace('_', '.')
    regex = re.compile(f"^{regex_pattern}$")
    return [word for word in words if regex.match(word)]

def match_pattern2(pattern, contains):
    # Replace underscores with '.' to match any character
    regex_pattern = pattern.replace('_', '.')
    regex = re.compile(f"^{regex_pattern}$")
    return [word for word in words if regex.match(word) and contains in word]

# API endpoint to get words matching the pattern
@app.route("/api/words", methods=["GET"])
def get_matching_words():
    pattern = request.args.get("pattern", "")
    matching_words = match_pattern(pattern)
    return jsonify(matching_words)

@app.route("/api/words2", methods=["GET"])
def get_matching_words2():
    pattern = request.args.get("pattern", "").lower()
    contains = request.args.get("contains", "").lower()
    regex_pattern = pattern.replace('_', '.')
    regex = re.compile(f"^{regex_pattern}$")  # Compile regex pattern
    matched_words = []

    for word in words:
        if regex.match(word) and sum(char in word for char in contains) >= len(contains):
            matched_words.append(word)
    return jsonify(matched_words)

@app.route("/api/words3", methods=["GET"])
def get_matching_words3():
    pattern = request.args.get("pattern", "").lower()
    contains = request.args.get("contains", "").lower()
    exclude = request.args.get("exclude", "").lower()
    regex_pattern = pattern.replace('_', '.')
    regex = re.compile(f"^{regex_pattern}$")  # Compile regex pattern
    matched_words = []

    for word in words:
        if regex.match(word) and sum(char in word for char in contains) >= len(contains) and not any(char in word for char in exclude):
            matched_words.append(word)
    return jsonify(matched_words)

# Render the main HTML page
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/level1")
def level1():
    return render_template("index.html")

@app.route("/level2")
def level2():
    return render_template("level2.html")

@app.route("/level3")
def level3():
    return render_template("level3.html")

if __name__ == "__main__":
    app.run(debug=True)
