'''Account controller module.

This module handles user authentication and session management.
'''

from flask import Blueprint, render_template, request, redirect, session

from services.todoist import ServiceTodoist
from services.notion import ServiceNotion
from services.zenkit import ServiceZenkit


class AccountController:
    '''Controller for account-related operations.'''

    bp = Blueprint('account', __name__, url_prefix='/account')

    @bp.route('/login', methods=['GET'])
    def render_login_page():
        '''Renders the login page.

        Returns:
            str: The rendered HTML of the login page.
        '''
        return render_template('login.html')

    @bp.route('/login', methods=['POST'])
    def login():
        '''Handles the login request.

        Returns:
            Response: Redirects to home on success, or returns an error message.
        '''
        session['source'] = request.form['source']
        token = request.form['token']
        auth_status = False

        match session['source']:
            case 'Todoist':
                todoist = ServiceTodoist()
                auth_status = todoist.check_token_auth(token)
            case 'Notion':
                notion = ServiceNotion()
                auth_status = notion.check_token_auth(token)
            case 'Zenkit':
                zenkit = ServiceZenkit(token)
                auth_status = zenkit.check_token_auth()

        if auth_status:
            session['token'] = token
            return redirect('/')
        return {'msg': 'Error the token is invalid'}

    @bp.route('/logout', methods=['GET'])
    def logout():
        '''Handles the logout request.

        Returns:
            Response: Redirects to the home page after clearing the session.
        '''
        session.clear()
        return redirect('/')
