import os


class ServiceCommand:
    '''Service for executing system commands.'''

    def clear(self):
        '''Clears the terminal screen.'''
        os.system('clear')
