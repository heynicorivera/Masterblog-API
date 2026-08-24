from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def generate_id():
    """Return a new unique id: one higher than the highest existing id."""
    highest_id = 0
    for post in POSTS:
        if post["id"] > highest_id:
            highest_id = post["id"]
    return highest_id + 1


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json(silent=True) or {}

    missing_fields = []
    if "title" not in data:
        missing_fields.append("title")
    if "content" not in data:
        missing_fields.append("content")
    if missing_fields:
        message = "Missing fields: " + ", ".join(missing_fields)
        return jsonify({"error": message}), 400

    new_post = {
        "id": generate_id(),
        "title": data["title"],
        "content": data["content"],
    }
    POSTS.append(new_post)
    return jsonify(new_post), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
