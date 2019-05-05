from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

classes_table = db.Table('classes_table', db.Model.metadata,
    db.Column('left_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('right_id', db.Integer, db.ForeignKey('classes.id'))
)

assignments_table = db.Table('assignments_table', db.Model.metadata,
    db.Column('left_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('right_id', db.Integer, db.ForeignKey('assignments.id'))
)

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String, nullable = False)
	name = db.Column(db.String, nullable = False)
	classes = db.relationship('Class', secondary=classes_table)
	assignments = db.relationship('Assignment', secondary=assignments_table)

	def __init__(self, **kwargs):
		self.username = kwargs.get('username', '')
		self.name = kwargs.get('name', '')
		classes = []
		assignments = []

	def serialize(self):
		my_classes = []
		my_assign = []
		for my_class in self.classes:
			my_classes.append({
				'id': my_class.id,
				'subject': my_class.subject,
				'number': my_class.number,
				'name': my_class.name
			})
		for assign in self.assignments:
			my_assign.append({
				'id': assign.id,
				'name': assign.name,
				'class_id': assign.class_id,
			})
		return {
			'id': self.id,
			'username': self.username,
			'name': self.name,
			'classes': my_classes,
			'assignments': my_assign
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
			'id': self.id,
			'subject': self.subject,
			'number': self.number,
			'name': self.name,
			'assignments': [assignment.serialize() for assignment in self.assignments]
		}

class Assignment(db.Model):
	__tablename__ = 'assignments'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String, nullable = False)
	class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable = False)
	messages = db.relationship('Message', cascade = 'delete')

	def __init__(self, **kwargs):
		self.name = kwargs.get('name', '')
		self.class_id = kwargs.get('class_id', 0)
		self.messages = []

	def serialize(self):
		return {
			'id': self.id,
			'name': self.name,
			'class_id': self.class_id,
			'messages': [message.serialize() for message in self.messages]
		}

class Message(db.Model):
	__tablename__ = 'messages'
	id = db.Column(db.Integer, primary_key = True)
	message = db.Column(db.String, nullable = False)
	username = db.Column(db.String, nullable = False)
	name = db.Column(db.String, nullable = False)
	time = db.Column(db.String, nullable = False)
	assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'), nullable = False)

	def __init__(self, **kwargs):
		self.message = kwargs.get('message', '')
		self.username = kwargs.get('username', '')
		self.name = kwargs.get('name', '')
		self.time = kwargs.get('time', '')
		self.assignment_id = kwargs.get('assignment_id', 0)

	def serialize(self):
		return {
			'id': self.id,
			'message': self.message,
			'username': self.username,
			'name': self.name,
			'time': self.time,
			'assignment_id': self.assignment_id
		}
