from flask import render_template

class SpreadSheetParseError(Exception):
    def __init__(self, error_note):
        self.error_note = error_note

def page_not_found_error(e):
    '''Invalid URL'''
    return render_template("404.html"), 404

def internal_server_error(e):
    '''Internal Server Error'''
    return render_template("500.html"), 500

def access_denied_error(e):
    '''Access Denied Error'''
    return render_template("403.html"), 403
