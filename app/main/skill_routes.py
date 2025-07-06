from flask import render_template, flash, redirect, url_for, abort
from flask_login import current_user, login_required
from app.models import db, Skill
from .skill_forms import SkillForm
from app.main import bp
from sqlalchemy import and_

@bp.route('/skills')
@login_required
def skills():  
    if not current_user.is_manager():
        abort(403)
    
    skills = Skill.query.all()  
    for skill in skills:
        form = SkillForm()   
        form.description.data = skill.description
        skill.form = form

    add_form = SkillForm()
    add_form.submit.label.text = "Create"       

    return render_template('skills.html', skills=skills, add_form=add_form)

@bp.route('/skills/add', methods=['POST'])
@login_required
def add_skill():  
    if not current_user.is_manager():
        abort(403)

    skill = Skill()
    form = SkillForm()
    if form.validate_on_submit():
        skill.description = form.description.data

        exists = Skill.query.filter(Skill.description == skill.description).first()                        
        if exists:
            flash("Skill already Exists", "error")
            return redirect(url_for('.skills'))

        db.session.add(skill)
        db.session.commit()               
    return redirect(url_for('.skills'))

@bp.route('/skills/update/<id>', methods=['POST'])
@login_required
def update_skill(id):  
    if not current_user.is_manager():
        abort(403)

    skill = Skill.query.get_or_404(id)
    form = SkillForm()
    if form.validate_on_submit():
        description = form.description.data        
        print("hello")

        exists = Skill.query.filter(and_(Skill.description == description, Skill.id != id)).first()                
        print("Exists:", exists)
        if exists:
            flash("Skill already Exists", "error")
            return redirect(url_for('.skills'))

        skill.description = description
        db.session.commit()               
    return redirect(url_for('.skills'))



@bp.route('/skills/delete/<id>', methods=['POST'])
@login_required
def delete_skill(id):  
    if not current_user.is_manager():
        abort(403)

    skill = Skill.query.get_or_404(id)
    db.session.delete(skill)
    db.session.commit()               
    return redirect(url_for('.skills'))    
