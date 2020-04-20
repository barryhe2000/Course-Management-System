from db import db, Course, Assignment, User

#courses
def get_all_courses():
    return [c.serialize() for c in Course.query.all()]

def create_course(code, name):
    new_course = Course(code=code,name=name)
    db.session.add(new_course)
    db.session.commit()
    return new_course.serialize()

def get_course_by_id(c_id):
    c = Course.query.filter_by(id=c_id).first()
    if c is None:
        return None
    return c.serialize()

def delete_course_by_id(c_id):
    c = Course.query.filter_by(id=c_id).first()
    if c is None:
        return None
    db.session.delete(c)
    db.session.commit()
    return c.serialize()

#assignments
def create_assignment(title, due_date, course_id):
    new_assignment = Assignment(title=title,
        due_date=due_date,
        course_id=course_id
    )
    db.session.add(new_assignment)
    db.session.commit()
    return new_assignment.serialize()

#users
def create_user(name, netid):
    new_user = User(name=name, netid=netid)
    db.session.add(new_user)
    db.session.commit()
    return new_user.serialize()

def get_user_by_id(u_id):
    u = User.query.filter_by(id=u_id).first()
    if u is None:
        return None
    return u.serialize()

def add_user_to_course(user_id, type, course_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return None
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        return None
    if(type == "instructor"):
        course.instructors.append(user)
    else:
        course.students.append(user)
    db.session.commit()
    return course.serialize()
