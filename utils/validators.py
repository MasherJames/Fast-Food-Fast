import re


class Validators:
    def valid_username(self, username):
        """ valid username """
        return re.match("^[a-zA-Z0-9]{6,20}$", username)

    def valid_password(self, password):
        """ valid password """
        regex = "^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])[a-zA-Z0-9]{8,15}$"
        return re.match(regex, password)

    def valid_email(self, email):
        """ valid email """
        return re.match("^[^@]+@[^@]+\.[^@]+$", email)

    def valid_is_admin(self, value):
        """ valid is admin value """
        return re.match("^ [0-1]{1}$", value)

    def valid_inputs(self, string_inputs):
        """ valid input strings """
        return re.match("^[a-zA-Z0-9-\._@ ]+$", string_inputs)
