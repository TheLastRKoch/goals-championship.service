'''Goal controller module.

This module handles goal-related operations, including filtering and listing tasks.
'''

from os import environ as env

from flask import Blueprint, render_template, session, redirect, request, Response

from services.formatter import ServiceFormatter
from services.todoist import ServiceTodoist
from services.zenkit import ServiceZenkit
from services.notion import ServiceNotion
from utils.files import UtilFile
from utils.dates import UtilsDate
from environment import DATE_FORMAT_RESULT


def get_task_list(filter_month, filter_year, project_list):
    '''Retrieves and formats the task list based on the user's source and filters.

    Args:
        filter_month (str): The month to filter tasks by.
        filter_year (str): The year to filter tasks by.
        project_list (list): A list of project IDs to filter tasks by.

    Returns:
        list: A list of formatted tasks with scores calculated.
    '''
    # Init services
    formatter = ServiceFormatter()

    source = session.get('source')
    token = session.get('token')
    start_date = formatter.get_start_date(filter_month, filter_year)
    end_date = formatter.get_end_date(filter_month, filter_year)
    task_list = []

    match source:
        case 'Todoist':
            todoist = ServiceTodoist()
            task_list = todoist.get_task_list(token, start_date)
            if not task_list:
                return task_list
            project_list = todoist.get_project_list(token)
            task_list = todoist.merge_tasks_projects(task_list, project_list)

        case 'Notion':
            notion = ServiceNotion()
            task_list = notion.get_task_list(token, filter_month)

        case 'Zenkit':
            zenkit = ServiceZenkit(token)
            task_list = []
            for project_id in project_list:
                column_list = zenkit.get_list_columns(project_id)
                done_category_id = zenkit.get_done_stage(project_id)[0].get(
                    'id')
                task_list += zenkit.get_entry_list_per_list(
                    list_id=project_id,
                    column_list=column_list,
                    done_category_id=done_category_id,
                    start_date=start_date,
                    end_date=end_date,
                )

    # Formatting task list
    task_list = formatter.format_dates(task_list, DATE_FORMAT_RESULT)
    return formatter.calculate_score(task_list)


class GoalController:
    '''Controller for goal-related operations.'''

    bp = Blueprint('goal', __name__, url_prefix='/goal')

    @bp.route('/', methods=['GET'])
    def home():
        '''Redirects to the goal filter page.

        Returns:
            Response: Redirect to /goal/filter.
        '''
        return redirect('/goal/filter')

    @bp.route('/filter', methods=['GET'])
    def render_goal_filter():
        '''Renders the goal filter page.

        Returns:
            str: The rendered HTML of the goal filter page.
        '''
        if 'token' not in session:
            return render_template('index.html')

        # Clean session data
        session['filter_month'] = ''
        session['filter_year'] = ''
        session['project_list'] = ''

        # Get the list of projects
        project_list = []
        filter_projects = False

        match session['source']:
            case 'Zenkit':
                # Init services
                zenkit = ServiceZenkit(session['token'])
                project_list = zenkit.get_list_of_lists()
                filter_projects = True

        return render_template(
            'goal_filter.html',
            project_list=project_list,
            filter_projects=filter_projects,
        )

    @bp.route('/filter', methods=['POST'])
    def goal_filter():
        '''Handles the goal filter form submission.

        Returns:
            Response: Redirect to the goal list page.
        '''
        session['filter_month'] = request.form.get('filterMonth')
        session['filter_year'] = request.form.get('filterYear')
        session['project_list'] = request.form.get('selectedProjects',
                                                   '').split(',')

        return redirect('/goal/list')

    @bp.route('/list', methods=['GET'])
    def goal_list():
        '''Renders the goal list page.

        Returns:
            str or list: The rendered HTML of the goal list or JSON data.
        '''
        if 'token' not in session:
            return render_template('index.html')

        filter_month = session.get('filter_month')
        filter_year = session.get('filter_year')
        project_list = session.get('project_list', [])
        output = request.args.get('output')

        task_list = get_task_list(filter_month=filter_month,
                                  filter_year=filter_year,
                                  project_list=project_list)

        if output == 'json':
            return task_list
        return render_template('goal_list.html', task_list=task_list)

    @bp.route('/list/download', methods=['GET'])
    def download_goal_list():
        '''Handles the download of the goal list as a CSV file.

        Returns:
            Response: The CSV file as an attachment.
        '''
        # Init utils
        dates = UtilsDate()
        files = UtilFile()

        filter_month = session.get('filter_month')
        filter_year = session.get('filter_year')
        project_list = session.get('project_list', [])
        task_list = get_task_list(filter_month=filter_month,
                                  filter_year=filter_year,
                                  project_list=project_list)
        csv_data = files.json_to_csv(task_list)
        file_name = env['TASK_FILE_NAME'].format(
            timespan=dates.timestamp(env['FILE_TIMESPAN_FORMAT']))

        return Response(
            csv_data,
            mimetype='text/csv',
            headers={
                'Content-Disposition': f'attachment;filename={file_name}'
            },
        )
