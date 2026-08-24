from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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


def find_post_by_id(post_id):
    """Return the post with the given id, or None if it does not exist."""
    for post in POSTS:
        if post["id"] == post_id:
            return post
    return None


@app.route('/api/posts', methods=['GET'])
def get_posts():
    sort_field = request.args.get('sort')
    direction = request.args.get('direction')

    if sort_field is not None and sort_field not in ["title", "content"]:
        message = (f"Invalid sort field: {sort_field}. "
                   "Use 'title or 'content. ")
        return jsonify({"error": message}), 400
    if direction is not None and direction not in ["asc", "desc"]:
        message = f"Invalid direction: {direction}. Use 'asc' or 'desc'."
        return jsonify({"error": message}), 400

    if sort_field is None:
        return jsonify(POSTS)

    reverse = direction == "desc"
    sorted_posts = sorted(POSTS, key=lambda post: post[sort_field],
                          reverse=reverse)
    return jsonify(sorted_posts)


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


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = find_post_by_id(post_id)
    if post is None:
        message = f"Post with id {post_id} was not found."
        return jsonify({"error": message}), 404

    POSTS.remove(post)
    message = f"Post with id {post_id} has been deleted successfully."
    return jsonify({"message": message}), 200


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post = find_post_by_id(post_id)
    if post is None:
        message = f"Post with id {post_id} was not found."
        return jsonify({"error": message}), 404

    data = request.get_json(silent=True) or {}
    post["title"] = data.get("title", post["title"])
    post["content"] = data.get("content", post["content"])
    return jsonify(post), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title_term = request.args.get('title')
    content_term = request.args.get('content')

    results = []
    for post in POSTS:
        title_matches = title_term and title_term in post["title"]
        content_matches = content_term and content_term in post["content"]
        if title_matches or content_matches:
            results.append(post)
    return jsonify(results)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
