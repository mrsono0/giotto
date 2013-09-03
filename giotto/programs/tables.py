import six
from giotto import get_config
from django.core.management import call_command

def syncdb():
    """
    Create all the tables for the models that have been added to the manifest.
    """
    call_command('syncdb', traceback=True)

def blast_tables():
    """
    Drop all existing tables in the database, and then recreate them.
    """
    msg = "This will delete all data in your tables, are you sure? [yN]"
    if six.PY3:
        yn = input(msg)
    else:
        yn = raw_input(msg)
    if yn.lower() != 'y':
        return "Aborting"

    print("blasting away all tables...")
    return syncdb()