from fuzzingbook.WebFuzzer import start_httpd
from http.server import HTTPServer, BaseHTTPRequestHandler, HTTPStatus
from luhn import luhn
import sqlite3
import os
import re
import urllib

HTML_REGISTER_FORM = """
<html><body>
<form action="/register" style="border:3px; border-style:solid; border-color:#FF0000; padding: 1em;">
  <strong id="title" style="font-size: x-large">Register</strong>
  <p>
  <label for="name">Name: </label><input type="text" name="name"><br>
  <label for="lastname">Last Name: </label><input type="text" name="lastname"><br>
  <label for="email">Email: </label><input type="email" name="email"><br>
  <label for="password">Password: </label><input type="password" name="password"><br>
  <label for="password2">Repeat Password: </label><input type="password" name="password2"><br>
  <label for="banking">Creditcard: </label><input type="text" name="banking"><br>
  <input type="submit" name="submit" value="register">
</p>
</form>
</body></html>
"""

HTML_REGISTERED = """
<html><body>
<div style="border:3px; border-style:solid; border-color:#FF0000; padding: 1em;">
  <strong id="title" style="font-size: x-large">Welcome {name} {lastname}!</strong>
  <p id="confirmation">
  Thank you for your registration.
  We will send a confirmation mail to {email}.
  </p>
  <p>
  Back to the <a href="/">registration</a>!
  </p>
</div>
</body></html>
"""

HTML_NOT_REGISTERED = """
<html><body>
<div style="border:3px; border-style:solid; border-color:#FF0000; padding: 1em;">
  <strong id="title" style="font-size: x-large">Something was wrong with the form!</strong>
  <p>
  Back to the <a href="/">registration</a>!
  </p>
</div>
</body></html>
"""

HTML_NOT_FOUND = """
<html><body>
<div style="border:3px; border-style:solid; border-color:#FF0000; padding: 1em;">
  <strong id="title" style="font-size: x-large">Sorry.</strong>
  <p>
  This page does not exist.  Try our <a href="/">registration form</a> instead.
  </p>
</div>
</body></html>
"""

HTML_INTERNAL_SERVER_ERROR = """
<html><body>
<div style="border:3px; border-style:solid; border-color:#FF0000; padding: 1em;">
  <strong id="title" style="font-size: x-large">Internal Server Error</strong>
  <p>
  The server has encountered an internal error.  Go to our <a href="/">order form</a>.
  <pre>{error_message}</pre>
  </p>
</div>
</body></html>
"""

USERS_DB = "users.db"

def init_db():
    if os.path.exists(USERS_DB):
        os.remove(USERS_DB)

    db_connection = sqlite3.connect(USERS_DB)
    db_connection.execute("DROP TABLE IF EXISTS users")
    db_connection.execute("CREATE TABLE users "
                          "(name text, lastname text, email text, "
                          "password text, banking text)")
    db_connection.commit()

    return db_connection

mail_pattern = re.compile(r'[^@]+@[^@]+\.[^@.]+')

class RegisterHTTPRequestHandler(BaseHTTPRequestHandler):
    
    bugs = {}
    users = 0
    
    def do_GET(self):
        try:
            if self.path == "/":
                self.send_registration_form()
            elif self.path.startswith("/register"):
                self.handle_register()
            else:
                self.not_found()
        except Exception:
            self.internal_server_error('GET')
    
    def do_HEAD(self):
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "text/html")
        self.end_headers()
            
    def get_field_values(self):
        query_string = urllib.parse.urlparse(self.path).query
        fields = urllib.parse.parse_qs(query_string, keep_blank_values=True)
        values = {}
        for key in fields:
            values[key] = fields[key][0]
        return values
    
    def send_registration_form(self):
        self.send_response(HTTPStatus.OK, "Register yourself")
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(HTML_REGISTER_FORM.encode("utf8"))
        
    def handle_register(self):
        values = self.get_field_values()
        state = 0
        if not values['name'].isalpha():
            if 0 not in RegisterHTTPRequestHandler.bugs:
                RegisterHTTPRequestHandler.bugs[0] = self.path
            state = 2
        if not values['lastname'].isalpha():
            if 1 not in RegisterHTTPRequestHandler.bugs:
                RegisterHTTPRequestHandler.bugs[1] = self.path
            state = 2
        if not mail_pattern.match(values['email']):
            state = max(state, 1)
        if values['password'].isalnum():
            if not values['password'].isalpha():
                if 2 not in RegisterHTTPRequestHandler.bugs:
                    RegisterHTTPRequestHandler.bugs[2] = self.path
                state = 2
            else:
                state = max(state, 1)
        if values['password'] != values['password2']:
            if 3 not in RegisterHTTPRequestHandler.bugs:
                RegisterHTTPRequestHandler.bugs[3] = self.path
            state = 2
        if str(luhn(values['banking'][:-1])) != values['banking'][-1]:
            state = max(state, 1)
        if state == 0 and len(values['email'].split('.')[-1]) > 3:
            if 4 not in RegisterHTTPRequestHandler.bugs:
                RegisterHTTPRequestHandler.bugs[4] = self.path
            state = 3
        if (state == 0 or state == 3) and len(values['password']) < 4:
            if 5 not in RegisterHTTPRequestHandler.bugs:
                RegisterHTTPRequestHandler.bugs[5] = self.path
            state = 3
        if (state == 0 or state == 3) and len(values['password']) > 16:
            if 6 not in RegisterHTTPRequestHandler.bugs:
                RegisterHTTPRequestHandler.bugs[6] = self.path
            state = 3
        if state == 0 and RegisterHTTPRequestHandler.users > 20:
            if 7 not in RegisterHTTPRequestHandler.bugs:
                RegisterHTTPRequestHandler.bugs[7] = self.path
            state = 3
        if state == 0:
            RegisterHTTPRequestHandler.users += 1
            self.store_user(values)
            self.send_user_registered(values)
        elif state == 1:
            self.bad_request()
        else:
            with open('bugs.py', 'w') as fp:
                fp.write(f'bugs = {RegisterHTTPRequestHandler.bugs}')
            self.internal_server_error(RegisterHTTPRequestHandler.bugs)
        
    def store_user(self, values):
        db = sqlite3.connect(USERS_DB)
        sql_command = "INSERT INTO users VALUES ('{name}', '{lastname}', '{email}', '{password}', '{banking}')".format(**values)
        self.log_message("%s", sql_command)
        db.executescript(sql_command)
        db.commit()
    
    def send_user_registered(self, values):
        self.send_response(HTTPStatus.OK, "Registered")
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(HTML_REGISTERED.format(**values).encode("utf8"))
        
    def not_found(self):
        self.send_response(HTTPStatus.NOT_FOUND, "Not found")
        self.send_header("Content-type", "text/html")
        self.end_headers()
        message = HTML_NOT_FOUND
        self.wfile.write(message.encode("utf8"))
        
    def bad_request(self):
        self.send_response(HTTPStatus.BAD_REQUEST, "Bad request")
        self.send_header("Content-type", "text/html")
        self.end_headers()
        message = HTML_NOT_REGISTERED
        self.wfile.write(message.encode("utf8"))
    
    def internal_server_error(self, bugid):
        self.log_message("%s", str(bugid))
        self.send_response(HTTPStatus.INTERNAL_SERVER_ERROR, "Internal Error")
        self.send_header("Content-type", "text/html")
        self.end_headers()
        message = HTML_INTERNAL_SERVER_ERROR.format(error_message=str(bugid))
        self.wfile.write(message.encode("utf8"))
        

if __name__ == '__main__':
    httpd_process, httpd_url = start_httpd(RegisterHTTPRequestHandler)
    print(httpd_url)