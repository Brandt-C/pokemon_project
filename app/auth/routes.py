from flask import Blueprint, render_template, request, redirect, url_for, flash

from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash

from .forms import PokeName, SignupForm, LoginForm
from ..models import User, Pokemon

import requests, json

auth = Blueprint('auth', __name__, template_folder='auth_templates')


@auth.route('/enterpokemon', methods=['GET', 'POST'])
def enterpokemon():
    form = PokeName()
    print(request.method)
    if request.method == 'POST':
        pokemon = form.pokemon.data
        print(pokemon)
        poke = Pokemon.query.filter_by(name=pokemon).first()
        if poke:
            flash(f'Wild {pokemon.capitalize()} Appeared!')
            return render_template('enterpokemon.html', form=form, poke=poke)
        

        def poke_data(pokename):
            response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokename}")
            print(response)
            if response.ok:
                data = response.json()
                pokeinfo = {}
                pokeinfo['species'] = pokename
                pokeinfo['ability'] = data["abilities"][0]['ability']['name']
                pokeinfo['base_exp'] = data["base_experience"]
                pokeinfo['sprite'] = data['sprites']['front_shiny']
                pokeinfo['attack'] = data['stats'][1]['base_stat']
                pokeinfo['defense'] = data['stats'][2]['base_stat']
                pokeinfo['hp'] = data['stats'][0]['base_stat']
                return pokeinfo
        poke = poke_data(pokemon)
        print(poke)
        new_pokemon = Pokemon(
            name=poke['species'],
            ability=poke['ability'],
            base_exp=poke['base_exp'],
            sprite=poke['sprite'],
            attack=poke['attack'],
            defense=poke['defense'],
            hp=poke['hp']
        )
        new_pokemon.save_pokemon()
        # save_pokemon(new_pokemon)


        flash(f'Wild {pokemon.capitalize()} Appeared!')        
        return render_template('enterpokemon.html', form=form, poke=poke)
    # flash(f'Wild {pokemon} Appeared!')
    return render_template('enterpokemon.html', form=form)





@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            user = User(username, email, password)
            user.save_user()
            return redirect(url_for('auth.login'))



    return render_template('signup.html', form=form)

    
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            password = form.password.data


            user = User.query.filter_by(username=username).first()
            if user:
                
                if check_password_hash(user.password, password):
                    flash('You are logged in', 'success')
                    login_user(user)
                    return redirect(url_for('team'))
                else:
                    flash('Invalid Password', 'danger')
            else:
                flash('User not found', 'warning')


    return render_template('login.html', form=form)

@auth.route('/logout')
def logout():
    flash('you\'re logged out', 'secondary')
    logout_user()
    return redirect(url_for('login'))


@auth.route('/catchpoke/<int:pokemon>', methods=['GET', 'POST'])
# @login_required
def add_to_team():
    my_poke = Pokemon.query.get(id) 
    if my_poke not in current_user.catch_poke:
        current_user.catch_it(my_poke)
        
    return redirect('/team/')
# catch release routeslike unlike follow unfollow


# battle query all users use new html button feedback win loss column