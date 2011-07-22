from repoze.who.plugins.basicauth import BasicAuthPlugin
from repoze.who.plugins.htpasswd import HTPasswdPlugin

from StringIO import StringIO
io = StringIO()
for name, password in [ ('admin', 'admin'), ('chris', 'chris') ]:
    io.write('%s:%s\n' % (name, password))
io.seek(0)

def cleartext_check(password, hashed):
    return password == hashed
htpasswd = HTPasswdPlugin(io, cleartext_check)
basicauth = BasicAuthPlugin('repoze.who')
identifiers = [('basicauth',basicauth)]
authenticators = [('htpasswd', htpasswd)]
challengers = [('basicauth',basicauth)]

from repoze.who.middleware import PluggableAuthenticationMiddleware
from repoze.who.classifiers import default_request_classifier
from repoze.who.classifiers import default_challenge_decider
def make_auth_app(app):
    new_app = PluggableAuthenticationMiddleware(app, identifiers, authenticators, challengers,[], default_request_classifier, default_challenge_decider)
    return new_app
