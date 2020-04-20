from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
instr_table = db.Table("i_courses", db.Model.metadata,
    db.Column("instr_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("course_id", db.Integer, db.ForeignKey("course.id"))
)
student_table = db.Table("s_courses", db.Model.metadata,
    db.Column("student_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("course_id", db.Integer, db.ForeignKey("course.id"))
)

class Course(db.Model):
    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    assignments = db.relationship("Assignment", cascade="delete")
    instructors = db.relationship("User",
        secondary=instr_table,
        back_populates="instr_courses"
    )
    students = db.relationship("User",
        secondary=student_table,
        back_populates="student_courses"
    )

    def __init__(self, **kwargs):
        self.code = kwargs.get("code", "")
        self.name = kwargs.get("name", "")

    def serialize(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "assignments": [a.serialize() for a in self.assignments],
            "instructors": [i.serialize() for i in self.instructors],
            "students": [s.serialize() for s in self.students]
        }

    def mini_serialize(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name
        }

class Assignment(db.Model):
     __tablename__ = "assignment"
     id = db.Column(db.Integer, primary_key=True)
     title = db.Column(db.String, nullable=False)
     due_date = db.Column(db.Integer, nullable=False)
     course_id = db.Column(db.Integer, db.ForeignKey("course.id"),
        nullable=False)

     def __init__(self, **kwargs):
         self.title = kwargs.get("title", "")
         self.due_date = kwargs.get("due_date")
         self.course_id = kwargs.get("course_id")

     def serialize(self):
         return {
             "id": self.id,
             "title": self.title,
             "due_date": self.due_date
         }

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    netid = db.Column(db.String, nullable=False)
    instr_courses = db.relationship("Course",
        secondary=instr_table,
        back_populates="instructors"
    )
    student_courses = db.relationship("Course",
        secondary=student_table,
        back_populates="students"
    )

    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "")
        self.netid = kwargs.get("netid", "")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "netid": self.netid,
            "courses": [i.mini_serialize() for i in self.instr_courses] +
                [s.mini_serialize() for s in self.student_courses]
        }
