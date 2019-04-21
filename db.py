from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, nullable = False)
    name = db.Column(db.String, nullable = False)

    def __init__(self, **kwargs):
        self.username = kwargs.get('username', '')
        self.name = kwargs.get('name', '')

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
        }

class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key = True)
    subject = db.Column(db.String, nullable = False)
    number = db.Column(db.Integer, nullable = False)
    name = db.Column(db.String, nullable = False)
    assignments = db.relationship('Assignment', cascade = 'delete')

    def __init__(self, **kwargs):
        self.subject = kwargs.get('subject', '')
        self.number = kwargs.get('number', 0)
        self.name = kwargs.get('name', '')

    def serialize(self):
        return {
            'subject': self.subject,
            'number': self.number,
            'name': self.name
        }

class Assignment(db.Model):
	__table__ = 'assignments'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String, nullable = False)
	class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable = False)
	messages = db.relationship('Message', cascade = 'delete')

	def __init__(self, **kwargs):
		self.name = kwargs.get('name', '')
		self.class_id = kwargs.get('class_id', 0)

	def serialize(self):
		return {
			'name': self.name,
			'class_id': self.class_id,
			'messages': [message.serialize() for message in self.messages]
		}

class Message(db.Model):
	__table__ = 'messages'
	id = db.Column(db.Integer, primary_key = True)
	message = db.Column(db.String, nullable = False)
	user = db.Column(db.String, nullable = False)
	time = db.Column(db.String, nullable = False)
	assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'), nullable = False)

	def __init__(self, **kwargs):
		self.message = kwargs.get('message', '')
		self.user = kwargs.get('user', '')
		self.time = kwargs.get('time', '')

	def serialize(self):
		return {
			'id': self.id,
			'message': self.message,
			'user': self.user,
			'time': self.time,
			'assignment_id': self.assignment_id
		}
