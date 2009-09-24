import datetime
from hashlib import md5
from django.conf import settings
from django.utils import simplejson
from gae_sessions.models import GoogleSession

class SessionMiddleware(object):
    def process_request(self, request):
        try:
            sess_key = request.COOKIES['__gae_session__']
        except KeyError:
            sess_key = md5('%s%s' % (datetime.datetime.now(), settings.SECRET_KEY)).hexdigest()
        current_session = GoogleSession.get_or_insert(sess_key, session_key = sess_key, expire_date = datetime.datetime.now())
        request.session = simplejson.loads(current_session.session_data) if current_session.session_data else {}
        request.session_key = sess_key

    def process_response(self, request, response):
        current_session = GoogleSession.get_by_key_name(request.session_key)
        current_session.session_data = simplejson.dumps(request.session)
        current_session.put()
        response.set_cookie('__gae_session__', current_session.session_key)
        return response
