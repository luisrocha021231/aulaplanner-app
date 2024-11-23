from flask import jsonify, request, send_file, render_template
from werkzeug.utils import secure_filename
from utils import procesar_archivos, allowed_file
import os

def init_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/upload', methods=['POST'])
    def upload_file():
        if 'clases' not in request.files or 'salones' not in request.files:
            return 'Faltan archivos', 400

        clases = request.files['clases']
        salones = request.files['salones']

        if clases.filename == '' or salones.filename == '':
            return 'No se seleccionaron archivos', 400

        if clases and allowed_file(clases.filename, app) and salones and allowed_file(salones.filename, app):
            clases_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(clases.filename))
            salones_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(salones.filename))
            clases.save(clases_path)
            salones.save(salones_path)

            resultado_paths = procesar_archivos(clases_path, salones_path)
            
            if isinstance(resultado_paths, str):
                return resultado_paths, 400
            
            csv_path, pdf_path = resultado_paths

            return send_file(csv_path, as_attachment=True)

            # return send_file(pdf_path, as_attachment=True)

        #return 'Tipo de archivo no permitido', 400
    
    @app.route('/download/<filename>', methods=['GET'])
    def download_file(filename):
        return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)
