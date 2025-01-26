import os

def load_css(css_file="main.css"):
    """Load CSS from a file"""
    css_path = os.path.join(os.path.dirname(__file__), "..", "styles", css_file)
    with open(css_path) as f:
        return f"<style>{f.read()}</style>" 