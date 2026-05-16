'''Index controller module.

This module handles the root URL routing.
'''

from flask import Blueprint, redirect, session


class IndexController:
    '''Controller for the index page.'''

    bp = Blueprint('index', __name__, url_prefix='/')

    @bp.route('/', methods=['GET'])
    def get():
        '''Handles GET requests to the root URL.

        Returns:
            Response: Redirects to either goal or login page based on session.
        '''
        if 'token' in session.keys():
            return redirect('goal')
        return redirect('account/login')
