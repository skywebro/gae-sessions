from google.appengine.ext import db

class GoogleSession(db.Model):
    session_key = db.StringProperty()
    session_data = db.TextProperty()
    ip = db.StringProperty()
    expire_date = db.DateTimeProperty()

    @classmethod
    def get_current_session(cls, key = None, **kwargs):
        return cls.get_or_insert(key, **kwargs)