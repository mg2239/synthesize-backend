import json
from db import db, Class, User, Assignment
from flask import Flask, request

db_filename = "classes.db"
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
@app.route('/api/classes/')
def get_classes():
    classes = Class.query.all()
    res = {'success': True, 'data': [single_class.serialize() for single_class in classes]} 
    return json.dumps(res), 200

@app.route('/api/classes/', methods=['POST'])
def create_class():
    post_body = json.loads(request.data)

    new_class = Class(
        code = post_body.get('code'),
        name = post_body.get('name') 
    )

    db.session.add(new_class)
    db.session.commit()
    return json.dumps({'success': True, 'data': new_class.serialize()}), 201

@app.route('/api/class/<int:class_id>/')
def get_class(class_id):
    single_class = Class.query.filter_by(id = class_id).first()
    if single_class is not None:
        return json.dumps({'success': True, 'data': single_class.serialize()}), 200
    return json.dumps({'success': False, 'error': 'Task not found'}), 404

@app.route('/api/class/<int:class_id>/', methods=['DELETE'])
def delete_class(class_id):
    deleted_class = Class.query.filter_by(id = class_id).first()
    if deleted_class is not None:
        db.session.delete(deleted_class)
        db.session.commit()
        return json.dumps({'success': True, 'data': deleted_class.serialize()}), 200
    return json.dumps({'success': False, 'error': 'Task not found'}), 404

@app.route('/api/users/', methods=['POST'])
def create_user():
    post_body = json.loads(request.data)
    user = User(
        name = post_body.get('name'),
        netid = post_body.get('netid'))
    db.session.add(user)
    db.session.commit()
    return json.dumps({'success': True, 'data': user.serialize()}), 200

@app.route('/api/user/<int:user_id>/')
def get_user(user_id):
    user = User.query.filter_by(id = user_id).first()
    if user is not None:
        return json.dumps({'success': True, 'data': user.serialize()}), 200
    return json.dumps({'success': False, 'error': 'User not found'}), 404

@app.route('/api/class/<int:class_id>/add/', methods=['POST'])
def add_user_to_class(class_id): 
    post_body = json.loads(request.data)
    single_class = Class.query.filter_by(id = class_id).first()
    if single_class is not None:
        user_id = post_body.get('user_id')
        user_type = post_body.get('type')
        user = User.query.filter_by(id = user_id).first()
        if user is not None:
            if user_type == 'student':
                single_class.students.append(user)
            else:
                single_class.instructors.append(user)
            db.session.commit()
            return json.dumps({'success': True, 'data': single_class.serialize()})
        else:
            return json.dumps({'success': False, 'error': 'User not found'}), 200
    else:
        return json.dumps({'success': False, 'error': 'Class not found'}), 404

@app.route('/api/class/<int:class_id>/assignment/', methods=['POST'])
def add_assignment(class_id):
    post_body = json.loads(request.data)
    single_class = Class.query.filter_by(id = class_id).first()
    if single_class is not None:
        assignment = Assignment(
            description = post_body.get('description'),
            due_date = post_body.get('due_date'))
        single_class.assignments.append(assignment)
        db.session.commit()
        return json.dumps({'success': True, 'data':
                            assignment.serialize()}), 200
    return json.dumps({'success': False, 'error': 'Class not found'}), 404
