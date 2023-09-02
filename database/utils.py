import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def session_handle(func, *args, **kwargs):
    def wrapper(*args, **kwargs):
        db_url = os.getenv('DATABASE_URL')
        if db_url:
            session = None
            try:
                engine = create_engine(os.environ.get('DATABASE_URL'), echo=False)
                session = sessionmaker(bind=engine)()
                return func(session, *args, **kwargs)
            except Exception as e:
                raise e
            finally:
                if session is not None:
                    session.close()
        else:
            raise 'DATABASE_URL not in .env'

    return wrapper

