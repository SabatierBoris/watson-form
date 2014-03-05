# -*- coding: utf-8 -*-
# Support functions, classes
from io import BufferedReader, BytesIO
from watson.form import Form, fields
from watson.form.decorators import has_csrf
from wsgiref import util


def sample_environ(**kwargs):
    environ = {}
    util.setup_testing_defaults(environ)
    environ.update(kwargs)
    return environ


def environ_with_file(**kwargs):
    kwargs['REQUEST_METHOD'] = 'POST'
    kwargs['CONTENT_TYPE'] = 'multipart/form-data; boundary=---------------------------721837373350705526688164684'
    environ = sample_environ(**kwargs)
    postdata = """-----------------------------721837373350705526688164684
Content-Disposition: form-data; name="first_name"

1234
-----------------------------721837373350705526688164684
Content-Disposition: form-data; name="test"

blah
-----------------------------721837373350705526688164684
Content-Disposition: form-data; name="file"; filename="test.txt"
Content-Type: text/plain

Testing 123.

-----------------------------721837373350705526688164684
Content-Disposition: form-data; name="submit"

Add\x20
-----------------------------721837373350705526688164684--
"""
    environ['CONTENT_LENGTH'] = len(postdata)
    encoding = 'utf-8'
    fp = BufferedReader(BytesIO(postdata.encode(encoding)))
    environ['wsgi.input'] = fp
    return environ

form_user_mapping = {
    'first_name': (
        'personal',
        'first_name'),
    'email': (
        'personal',
        'contact',
        'email')}


class LoginForm(Form):
    username = fields.Text(required=True)
    password = fields.Password(required=True)
    first_name = fields.Text()
    last_name = fields.Text()
    email = fields.Text()


@has_csrf
class ProtectedForm(Form):
    pass


class UnprotectedForm(Form):
    test = fields.Text()


class UploadForm(Form):
    image = fields.File(name='upload_image')


class Other(object):
    test = None


class Contact(object):
    email = None


class Personal(object):
    first_name = None
    last_name = None
    contact = None

    def __init__(self):
        self.contact = Contact()


class SampleFormValidator(object):
    def __call__(self, form):
        if form.username.value != 'Simon':
            raise ValueError('Username does not match.')


class User(object):
    id = None
    username = None
    password = None
    personal = None

    def __init__(self, username=None, password=None):
        self.personal = Personal()
        if username:
            self.username = username
        if password:
            self.password = password

    def __repr__(self):
        return (
            '<User username:{0} password:{1}>'.format(
                self.username, self.password)
        )
