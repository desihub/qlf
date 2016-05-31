from contextlib import closing
from bokeh.client import push_session, pull_session
from bokeh.document import Document
from bokeh.embed import autoload_server
from django.conf import settings
from django.contrib.auth.models import User

try:
    bokeh_url = settings.BOKEH_URL
except AttributeError:
    # if not specified use the default which is localhost:5006
    bokeh_url = 'default'


def update_time_series_data(user, session):
    # TODO: this can be used to update bokeh sessions in realtime
    pass


def get_bokeh_script(plot):

    from .models import UserSession

    document = Document()
    document.add_root(plot)

    with closing(push_session(document, url=bokeh_url)) as session:
        # Save the session id
        UserSession.objects.create(user=User.objects.get(),
                                   bokehSessionId=session.id)
        # Get the script to pass into the template
        script = autoload_server(None, session_id=session.id, url=bokeh_url)

    return script


def update_bokeh_sessions(user_sessions):
    for us in user_sessions:
        with closing(pull_session(session_id=us.bokehSessionId,
                                  url=bokeh_url)) as session:
            if len(session.document.roots) == 0:
                # In this case, the session_id was from a dead session and
                # calling pull_session caused a new empty session to be
                # created. So we just delete the UserSession and move on.
                # It would be nice if there was a more efficient way - where I
                # could just ask bokeh if session x is a session.
                us.delete()
            else:
                update_time_series_data(user=us.user, session=session)
