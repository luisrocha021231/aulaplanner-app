import pandas as pd
import random
from datetime import datetime, timedelta
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pandas.plotting import table

def allowed_file(filename, app):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def procesar_archivos(clases_path, salones_path):
    try:
        clases_df = pd.read_csv(clases_path)
        salones_df = pd.read_csv(salones_path)
        
        if 'NOMBRECLASE' not in clases_df.columns or 'GRUPO' not in clases_df.columns:
            return "El archivo de clases no tiene las columnas requeridas ('NOMBRECLASE', 'GRUPO')."
        
        if 'SALON' not in salones_df.columns:
            return "El archivo de salones no tiene la columna requerida ('SALON')."

        salones = salones_df['SALON'].tolist()
        clases = clases_df.groupby('NOMBRECLASE')['GRUPO'].unique().to_dict()
        dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']

        resultados = []
        
        def generar_horario_inicio():
            horas_disponibles = [f'{h:02}:00' for h in range(7, 20)]
            return random.choice(horas_disponibles)

        def asignar_clases(clases, salones, dias):
            asignaciones = {dia: {salon: [] for salon in salones} for dia in dias}
            for nombre_clase, grupos in clases.items():
                for grupo in grupos:
                    dias_disponibles = dias[:]
                    for _ in range(2):
                        dia = random.choice(dias_disponibles)
                        dias_disponibles.remove(dia)
                        
                        salon = random.choice(salones)
                        horario_inicio = generar_horario_inicio()
                        horario_fin = (datetime.strptime(horario_inicio, '%H:%M') + timedelta(hours=2)).strftime('%H:%M')
                        
                        if len(asignaciones[dia][salon]) < 2:
                            asignaciones[dia][salon].append({
                                'Día': dia,
                                'Salón': salon,
                                'Clase': f'{nombre_clase} - Grupo {grupo}',
                                'Horario Inicio': horario_inicio,
                                'Horario Fin': horario_fin
                            })
                        else:
                            disponibles = [s for s in salones if len(asignaciones[dia][s]) < 2]
                            if disponibles:
                                salon = random.choice(disponibles)
                                asignaciones[dia][salon].append({
                                    'Día': dia,
                                    'Salón': salon,
                                    'Clase': f'{nombre_clase} - Grupo {grupo}',
                                    'Horario Inicio': horario_inicio,
                                    'Horario Fin': horario_fin
                                })
            return asignaciones

        asignaciones = asignar_clases(clases, salones, dias)
        for dia, salones_dia in asignaciones.items():
            for salon, clases_salon in salones_dia.items():
                for clase in clases_salon:
                    resultados.append(clase)

        resultados_df = pd.DataFrame(resultados)
        resultados_df = resultados_df.sort_values(by='Clase', ascending=True)

        output_file = 'uploads/asignaciones_resultado.csv'
        resultados_df.to_csv(output_file, index=False, encoding='utf-8')

        fig, ax = plt.subplots(figsize=(10, 6))

        ax.axis('off')

        tabla = table(ax, resultados_df, loc='center', colWidths=[0.2] * len(resultados_df.columns))

        tabla.auto_set_font_size(False)
        tabla.set_fontsize(10)
        tabla.auto_set_column_width(col=list(range(len(resultados_df.columns))))

        pdf_output = 'uploads/asignaciones_visual.pdf'
        with PdfPages(pdf_output) as pdf:
            pdf.savefig(fig, bbox_inches='tight')
            plt.close(fig)

        return output_file, pdf_output

    except pd.errors.EmptyDataError:
        return "Uno o ambos archivos CSV están vacíos o no tienen datos válidos."
    except Exception as e:
        return f"Ocurrió un error al procesar los archivos: {str(e)}"
