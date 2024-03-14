from flask import Flask, session, flash, redirect, g

def user_not_in_session():
    """Check if user is logged in."""
    if not g.user:
        flash("You need to log in to access this page.", "danger")
        return True
        
def not_same_username(username):
    """Check if the provided username matches the logged-in user."""
    if username != session['username']:
        flash("You are not authorized to view this page.", "danger")
        return True
        
def check_api(key):
    """Check if API KEY is None"""
    if key is None:
        raise ValueError("API Key is not provided")