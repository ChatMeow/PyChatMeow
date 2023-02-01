from utils.database.db import DatabaseManager

context = {
    'db.manager': None
}


def set_db_manager(db_manager : DatabaseManager):
    context.update({'db_manager': db_manager})
    

def get_db_manager() -> DatabaseManager:
    return context.get('db_manager')