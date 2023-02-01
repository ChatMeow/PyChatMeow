from utils.database.db import DatabaseManager
from functools import wraps
import time
import logging

context = {
    'db.manager': None,
    'retry.timewait': 10,
    'retry.max_retries': 10,
    'retry.current_retries': 1
}


def set_db_manager(db_manager: DatabaseManager):
    context.update({'db_manager': db_manager})


def get_db_manager() -> DatabaseManager:
    return context.get('db_manager')


def set_retries(timewait: int, max_retries: int):
    context.update({'retry.max_retries': max_retries})
    context.update({'retry.timewait': timewait})


def retry(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        code, text = f(*args, **kwargs)
        while code == 1:
            logging.info('Wait {}s before retry, current retries [{}] , max retries [{}]'.format(context['retry.timewait'],
                                                                                                context['retry.current_retries'], context['retry.max_retries']))
            time.sleep(context['retry.timewait'])
            code, text = f(*args, **kwargs)
            context['retry.current_retries'] = context['retry.current_retries'] + 1
            if context['retry.current_retries'] > context['retry.max_retries']:
                raise Exception('Max retries exceeded')
        context['retry.current_retries'] = 1
        return code, text
    return decorated


def logit(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        logging.debug(func.__name__ + " was called")
        return func(*args, **kwargs)
    return with_logging