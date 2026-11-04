"""
src/version_inicial/gestor_monolitico.py: Version primigenia del sistema que viola principios del desarrollo moderno

"""

import json
import os
from datetime import datetime

class GestorSolicitudesAcademicas:
    """
    1. CLASE GIGANTE (Large Class):
    Acumula responsabilidades de negocio, validaciones y persistencia en una sola estructura.
    Violación directa al Single Responsibility Principle (SRP).
    """
    def __init__(self, archivo_db="solicitudes_db.json"):
        self.archivo_db = archivo_db
        if not os.path.exists(self.archivo_db):
            with open(self.archivo_db, "w") as f:
                json.dump([], f)

    def registrar_solicitud(self, tipo: str, estudiante_id: str, descripcion: str, prioridad: str, fecha_limite: str):
        """
        2. MÉTODO LARGO (Long Method):
        Función que intenta realizar demasiadas tareas simultáneamente (validaciones, parseo de fechas, cálculo
        de IDs y persistencia). Resulta en un código difícil de leer, entender y testear de forma aislada.
        """
        """
        3. OBSESIÓN POR PRIMITIVOS (Primitive Obsession):
        Uso de tipos de datos básicos (como String) para representar conceptos de dominio complejos,
        validar estados, tipos y prioridades, careciendo de clases de dominio dedicadas.
        """
        if not estudiante_id or len(estudiante_id) < 3:
            raise ValueError("Error: El ID del estudiante no es válido.")
        
        if not descripcion or len(descripcion) < 10:
            raise ValueError("Error: La descripción debe tener al menos 10 caracteres.")

        if prioridad not in ["Baja", "Media", "Alta", "Urgente"]:
            raise ValueError("Prioridad inválida.")

        if tipo not in ["Equivalencia", "Certificado", "Examen", "Beca"]:
            raise ValueError("Tipo de solicitud no reconocido.")

        if fecha_limite:							# Bloque repetido (1ra aparicion)
            try:
                datetime.strptime(fecha_limite, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Formato de fecha límite inválido. Use YYYY-MM-DD.")

        with open(self.archivo_db, "r") as f:
            datos = json.load(f)
        
        nuevo_id = len(datos) + 1
        fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        nueva_solicitud = {
            "id": nuevo_id,
            "tipo": tipo,
            "estudiante_id": estudiante_id,
            "descripcion": descripcion,
            "prioridad": prioridad,
            "estado": "Pendiente", 						# Obsesión por primitivos (String para estado)
            "fecha_creacion": fecha_creacion,
            "fecha_limite": fecha_limite,
            "responsable": "Sin Asignar",
            "observaciones": ""
        }

        datos.append(nueva_solicitud)
        with open(self.archivo_db, "w") as f:
            json.dump(datos, f, indent=4)

        return nuevo_id

    def actualizar_estado_solicitud(self, solicitud_id: int, nuevo_estado: str, responsable: str, observaciones: str, area_asignada: str, notificar_alumno: bool, fecha_actualizacion: str):
        """
        4. DEMASIADOS PARÁMETROS (Long Parameter List):
        Método que requiere una lista extensa de argumentos independientes (7 parámetros)
        """
        with open(self.archivo_db, "r") as f:
            datos = json.load(f)

        encontrada = False
        for sol in datos:
            if sol["id"] == solicitud_id:
                if nuevo_estado not in ["Pendiente", "En Proceso", "Aprobada", "Rechazada"]:
                    raise ValueError("Estado no válido.")
                
                sol["estado"] = nuevo_estado
                sol["responsable"] = responsable
                sol["observaciones"] = observaciones
                sol["area"] = area_asignada
                sol["fecha_actualizacion"] = fecha_actualizacion
                encontrada = True
                break

        if not encontrada:
            raise KeyError(f"No se encontró la solicitud con ID {solicitud_id}")

        with open(self.archivo_db, "w") as f:
            json.dump(datos, f, indent=4)

        return True

    def validar_fechas_sistema(self, fecha_str: str):
        """
        5. CÓDIGO DUPLICADO (Duplicated Code): ataca el principio DRY.
        Se duplica exactamente la misma lógica de validación de formato de fecha que ya se encuentra
        dentro del método 'registrar_solicitud'. Si el formato cambia, hay que modificarlo en varios lugares.
        """
        if not fecha_str:							# Bloque repetido (2da aparicion)
            return False
        try:
            datetime.strptime(fecha_str, "%Y-%m-%d")
            return True
        except ValueError:
            raise ValueError("Formato de fecha límite inválido. Use YYYY-MM-DD.")
