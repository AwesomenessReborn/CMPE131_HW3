from app import myapp_obj
from flask import app, render_template, url_for
from flask import redirect
from app.forms import LoginForm, RecipeForm
from app.models import Recipe, User, Profile
from app import db
# from <X> import <Y>

@app.route('/recipes')
def index():
    recipes = Recipe.query.all()
    return render_template('index.html', recipes=recipes)

@app.route('/recipe/new', methods=['GET', 'POST'])
def new_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(
            title=form.title.data,
            description=form.description.data,
            ingredients=form.ingredients.data,
            instructions=form.instructions.data
        )
        db.session.add(recipe)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('recipe_form.html', form=form, title="New Recipe")

@app.route('/recipe/<int:recipe_id>')
def recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipe.html', recipe=recipe)

@app.route('/recipe/<int:recipe_id>/edit', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    form = RecipeForm(obj=recipe)
    if form.validate_on_submit():
        recipe.title = form.title.data
        recipe.description = form.description.data
        recipe.ingredients = form.ingredients.data
        recipe.instructions = form.instructions.data
        db.session.commit()
        return redirect(url_for('recipe', recipe_id=recipe.id))
    return render_template('recipe_form.html', form=form, title="Edit Recipe")

@app.route('/recipe/<int:recipe_id>/delete', methods=['POST'])
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for('index'))
