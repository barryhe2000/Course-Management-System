import json
from flask import Flask, request
import dao
from db import db

app = Flask(__name__)
db_filename = "cms.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

#responses
def success_response(data, code=200):
    return json.dumps({"success": True, "data": data}), code

def failure_response(message, code=404):
    return json.dumps({"success": False, "error": message}), code

#courses
@app.route('/api/courses/')
def get_courses():
    return success_response(dao.get_all_courses())

@app.route('/api/courses/', methods=['POST'])
def create_course():
    body = json.loads(request.data)
    course = dao.create_course(
        code=body.get("code"),
        name=body.get("name")
    )
    return success_response(course, 201)

@app.route('/api/courses/<int:c_id>/')
def get_course(c_id):
    c = dao.get_course_by_id(c_id)
    if c is None:
        return failure_response("Course not found!")
    return success_response(c)

@app.route('/api/courses/<int:c_id>/', methods=['DELETE'])
def delete_course(c_id):
    c = dao.delete_course_by_id(c_id)
    if c is None:
        return failure_response("Course not found!")
    return success_response(c)

#assignments
@app.route('/api/courses/<int:c_id>/assignment/', methods=['POST'])
def create_assignment(c_id):
    c = dao.get_course_by_id(c_id)
    if c is None:
        return failure_response("Course not found!")
    body = json.loads(request.data)
    assignment = dao.create_assignment(
        body.get("title"),
        body.get("due_date"),
        c_id
    )
    return success_response(assignment)

#users
@app.route('/api/users/', methods=['POST'])
def create_user():
    body = json.loads(request.data)
    user = dao.create_user(
        name=body.get("name"),
        netid=body.get("netid")
    )
    return success_response(user, 201)

@app.route('/api/users/<int:user_id>/')
def get_user(user_id):
    u = dao.get_user_by_id(user_id)
    if u is None:
        return failure_response("User not found!")
    return success_response(u)

@app.route('/api/courses/<int:course_id>/add/', methods=['POST'])
def add_to_course(course_id):
    body = json.loads(request.data)
    type = body.get("type")
    if(type != "student" and type != "instructor"):
        return failure_response("Invalid type!")
    c = dao.add_user_to_course(body.get("user_id"), type, course_id)
    if c is None:
        return failure_response("User or Course not found!")
    return success_response(c, 201)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
