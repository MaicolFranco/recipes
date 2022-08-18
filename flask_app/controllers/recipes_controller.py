from wsgiref.util import request_uri
from flask_app import app
from flask import render_template, redirect, request, flash, session, url_for, jsonify
from flask_app.models.recipe import Recipe
from flask_app.models.user import User


@app.route('/recipes')
def recipes():
    if 'user_id' in session:
        user = User.get_by_id(session['user_id'])
        recipes = Recipe.get_all()
        return render_template('recipes.html', recipes=recipes, user=user)
    else:
        return redirect(url_for('index'))

@app.route('/recipe/new')
def create_recipe():
    if 'user_id' in session:
        user = User.get_by_id(session['user_id'])
        return render_template('new_recipe.html', user=user)
    else:
        return redirect(url_for('index'))
    
@app.route('/process', methods=['POST'])
def process():
    if Recipe.validate(request.form):
        data = {
            'name': request.form['name'],
            "id": request.form['id'],
            'description':request.form['description'],
            'instructions': request.form['instructions'],
            'under30': request.form['under30'],
            'date_made':request.form['date_made'],
            'user_id': session['user_id']
        }
        Recipe.create(data)
        return redirect(url_for('recipes'))   
    return redirect('/recipe/new')



@app.route('/edit/<int:id>')
def edit_recipe(id):
    user = User.get_by_id(session['user_id'])
    recipe = Recipe.get_by_id(id)
    return render_template('edit_recipe.html', recipe=recipe, user=user)

@app.route('/delete/<int:id>')
def delete_recipe(id):
    Recipe.delete(id)
    return redirect(url_for('recipes'))

@app.route('/recipe/<int:id>')
def show_recipe(id):
    user = User.get_by_id(session['user_id'])
    recipe = Recipe.get_by_id(id)
    return render_template('show_recipe.html', recipe=recipe, user=user)

@app.route('/updated', methods=['POST'])
def update():
    if Recipe.validate(request.form):
        data = {
            'id': request.form['id'],
            'name': request.form['name'],
            'description': request.form['description'],
            'instructions': request.form['instructions'],
            'under30': request.form['under30'],
            'user_id': session['user_id'],
            "date_made":request.form['date_made']
        }
        Recipe.update(data)
        return redirect(url_for('recipes'))
    return redirect('/recipes')




