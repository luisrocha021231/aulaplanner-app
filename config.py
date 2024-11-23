import os

def configure_app(app):
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['ALLOWED_EXTENSIONS'] = {'csv'}
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
