import json
import requests
from db import db, Class, User, Assignment, Message
from flask import Flask, request

db_filename = "info.db"
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
	db.create_all()

@app.route('/api/classes/')
def get_classes():
	classes = Class.query.all()
	if not classes:
		subj_url = 'https://classes.cornell.edu/api/2.0/config/subjects.json?roster=SP19'
		subjects = requests.get(subj_url).json().get('data', '').get('subjects', '')
		subject_list = []
		for subject in subjects:
			subject_list.append(subject.get('value', ''))
		classes = []
		class_url = 'https://classes.cornell.edu/api/2.0/search/classes.json?roster=SP19&subject='
		for subject in subject_list:
			classes = requests.get(class_url + str(subject)).json().get('data', '').get('classes', '')
			for single_class in classes:
				new_class = Class(
					subject = single_class.get('subject', ''),
					number = single_class.get('catalogNbr', ''), 
					name = single_class.get('titleLong', '')
					)
				db.session.add(new_class)
		db.session.commit()
		res = {'success': True, 'data': [single_class.serialize() for single_class in classes]} 
		return json.dumps(res), 200
	return json.dumps({'success': True, 'data': [single_class.serialize() for single_class in classes]})

@app.route('/api/user/', methods=['POST'])
def create_user():
	post_body = json.loads(request.data)
	new_user = User(
		username = post_body.get('username'),
		name = post_body.get('name') 
	)
	db.session.add(new_user)
	db.session.commit()
	return json.dumps({'success': True, 'data': new_user.serialize()}), 201

@app.route('/api/user/<int:user_id>/')
def get_user(user_id):
	user = User.query.filter_by(id = user_id).first()
	if user is not None:
		return json.dumps({'success': True, 'data': user.serialize()}), 200
	return json.dumps({'success': False, 'error': 'User not found'}), 404

@app.route('/api/user/<int:user_id>/', methods=['POST'])
def modify_user(user_id):
	user = User.query.filter_by(id = user_id).first()
	if user is not None:
		post_body = json.loads(request.data)
		user.username = post_body.get('username', user.username)
		user.name = post_body.get('name', user.name)
		db.session.commit()
		return json.dumps({'success': True, 'data': user.serialize()}), 200
	return json.dumps({'success': False, 'error': 'User not found'}), 404

@app.route('/api/users/', methods=['GET'])
def get_users():
	users = User.query.all()
	res = {'success': True, 'data': [user.serialize() for user in users]} 
	return json.dumps(res), 200

@app.route('/api/users/', methods=['DELETE'])
def delete_users():
	User.query.delete()
	db.session.commit()
	return json.dumps({'success': True}), 200

@app.route('/api/class/<int:class_id>/', methods=['DELETE'])
def delete_class(class_id):
   deleted_class = Class.query.filter_by(id = class_id).first()
   if deleted_class is not None:
       db.session.delete(deleted_class)
       db.session.commit()
       return json.dumps({'success': True, 'data': deleted_class.serialize()}), 200
   return json.dumps({'success': False, 'error': 'Class not found'}), 404

@app.route('/api/class/<int:class_id>/assignment/', methods=['POST'])
def add_assignment(class_id):
   post_body = json.loads(request.data)
   single_class = Class.query.filter_by(id = class_id).first()
   if single_class is not None:
       assignment = Assignment(
           name = post_body.get('name', ''),
		   class_id = class_id
	   )
       single_class.assignments.append(assignment)
       db.session.add(assignment)
       db.session.commit()
       return json.dumps({'success': True, 'data': assignment.serialize()}), 200
   return json.dumps({'success': False, 'error': 'Class not found'}), 404

@app.route('/api/class/<int:class_id>/assignments/')
def get_assignments_of_class(class_id):
	single_class = Class.query.filter_by(id = class_id).first()
	if single_class is not None:
		assignments = [assignment.serialize() for assignment in single_class.assignments]
		return json.dumps({'success': True, 'data': assignments}), 200
	return json.dumps({'success': False, 'error': 'Class not found'}), 404

@app.route('/api/class/<int:class_id>/assignment/<int:assign_id>/', methods=['POST'])
def add_message_to_assignment(class_id, assign_id):
	post_body = json.loads(request.data)
	single_class = Class.query.filter_by(id = class_id).first()
	assignment = Assignment.query.filter_by(id = assign_id).first()
	user = User.query.filter_by(username = post_body.get('username')).first()
	if single_class is None:
		return json.dumps({'success': False, 'error': 'Class not found'}), 404
	elif assignment is None:
		return json.dumps({'success': False, 'error': 'Assignment not found'}), 404
	message = Message(
		message = post_body.get('message', ''),
		username = post_body.get('username', 'anonymous'),
		name = post_body.get('name', 'anonymous'),
		time = post_body.get('time', '2000-01-01T00:00:00'),
		assignment_id = assign_id
	)
	if user is not None:
		user.classes.append(single_class)
		user.assignments.append(assignment)
	assignment.messages.append(message)
	db.session.add(message)
	db.session.commit()
	return json.dumps({'success': True, 'data': message.serialize()}), 200

@app.route('/api/class/<int:class_id>/assignment/<int:assign_id>/')
def get_messages(class_id, assign_id):
	single_class = Class.query.filter_by(id = class_id).first()
	if single_class is not None:
		assignment = Assignment.query.filter_by(id = assign_id).first()
		if assignment is not None:
			return json.dumps({'success': True, 'data': [message.serialize() for message in assignment.messages]}), 200
		return json.dumps({'success': False, 'error': 'Assignment not found'})
	return json.dumps({'success': False, 'error': 'Class not found'})

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
