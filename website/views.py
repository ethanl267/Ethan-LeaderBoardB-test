from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Team, User, Work
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added', category='success')

    return render_template('home.html', user=current_user)



@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data) # takes data from post req, turns into dictionary
    noteId = note['noteId'] # gets note id
    note = Note.query.get(noteId) # search db for note with this id
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({}) # return empty response



@views.route('/my-team', methods=['GET', 'POST'])
@login_required
def my_team():
    
    if request.method == 'POST':
        team_name = request.form.get('teamName')
        all_teams_names = db.session.query(Team.name).all()
        all_teams_names = [value for value, in all_teams_names]

        if len(team_name) < 3:
            flash('Please enter a longer name', category='error')
        # if name exists in db 
        elif team_name in all_teams_names:
            flash('Team name is already in use', category='error')
        else:
            # create new team
            new_team = Team(name=team_name)
            db.session.add(new_team)
            db.session.commit()
            # get id of team
            teamId = new_team.id
            # get current user
            user = User.query.get(current_user.id)
            # update user to become team leader
            user.team_leader = True
            # update user team id
            user.team_id = teamId
            db.session.commit()
            flash('Team added', category='success')
    
    all_teams = Team.query.all()
    all_users = User.query.all()
    
    return render_template('myteam.html', user=current_user, teams = all_teams, users=all_users)




@views.route('/settings', methods=['GET'])
@login_required
def settings():
    return render_template('settings.html', user=current_user)



@views.route('/my-work', methods=['GET'])
@login_required
def my_work():
    return render_template('mywork.html', user=current_user)



@views.route('/manage-work', methods=['GET', 'POST'])
@login_required
def manage_work():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        points = request.form.get('points')
        # get list of users
        user_list = request.form.getlist('user')
        
        if len(title) < 1:
            flash('Please add a title', category='error')
        elif len(description) < 1:
            flash('Please add a description', category='error')
        elif int(points) < 1:
            flash('Please add points for this task', category='error')
        else:
            # for each user in user list save the new task
            for user in user_list:
                new_task = Work(title=title, description=description, user_id=user, status='To-Do', points=points)
                db.session.add(new_task)
                db.session.commit()
            flash('Work added', category='success')
    
    members = db.session.query(User).filter(User.team_id == current_user.team_id)
    
    return render_template('managework.html', user=current_user, members=members)



@views.route('/delete-team', methods=['POST'])
def delete_team():
    team = json.loads(request.data) 
    print(team)
    teamId = team['teamId'] 
    team = Team.query.get(teamId)
    if team:
        db.session.delete(team)
        db.session.commit()
    
    return jsonify({}) # return empty response



@views.route('/join-team', methods=['POST'])
def join_team():
    team = json.loads(request.data) 
    teamId = team['teamId'] 
    team = Team.query.get(teamId)
    if not current_user.team_id:
        # get current user
        user = User.query.get(current_user.id)
        # update user team name
        user.team_id = teamId
        db.session.commit()
        flash('You have joined a team', category='success')

    return jsonify({}) # return empty response



@views.route('/leave-team', methods=['GET'])
def leave_team():
    # get current user
    user = User.query.get(current_user.id)
    # update user team name
    user.team_id = 0
    db.session.commit()
    flash('You have left your team', category='success')

    return jsonify({}) # return empty response