from flask import Flask

app = Flask(
    __name__,
    template_folder='frontend/templates',
    static_folder='frontend/static'
)

app.secret_key = "secret123"

# Import routes AFTER app creation
from backend import routes