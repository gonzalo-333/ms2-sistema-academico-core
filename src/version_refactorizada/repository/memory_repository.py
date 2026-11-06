"""
src/version_refactorizada/repository/memory_repository.py: implementa concreta de la persistencia (archivo JSON)

"""
import json
import os
from typing import List, Optional
from src.version_refactorizada.repository.base import SolicitudRepository
from src.version_refactorizada.domain.models import Solicitud

class JsonFileSolicitudRepository(SolicitudRepository):		# Implementación concreta de la interfaz abstracta son sus metodos + JSON
    
    def __init__(self, archivo_db="solicitudes_db.json"):	# Inicializa ruta del archivo de base de datos JSON, definiendo su nombre
        self.archivo_db = archivo_db				# Lo guarda entre sus atributos
        if not os.path.exists(self.archivo_db):			# Si no existe ya, lo abre en modo escritura ("w")
            with open(self.archivo_db, "w") as f:		# abre para operar y cierra de manera segura
                json.dump([], f)				# escribe una lista vacia

    def guardar(self, solicitud: Solicitud) -> int:		# Recibe el objeto y retorna el id que le creó
        datos = self._leer_archivo()				# Llama a su propia funcion
        solicitud.id = len(datos) + 1
        datos.append(solicitud.__dict__)			# __dict__ transforma el objeto en un diccionario, para poder agregar a JSON
        self._escribir_archivo(datos)
        return solicitud.id

    def obtener_por_id(self, solicitud_id: int) -> Optional[Solicitud]:	# Si encuentra id que se le pasa, retorna la solicitud. Sino, None
        datos = self._leer_archivo()
        for item in datos:
            if item["id"] == solicitud_id:
                return Solicitud(**item)			# desempaqueta el diccionario (**item) para retornar un objeto Solicitud
        return None

    def actualizar(self, solicitud: Solicitud) -> bool:
        datos = self._leer_archivo()
        for i, item in enumerate(datos):
            if item["id"] == solicitud.id:			# actualiza solo el diccionario que esta en esa posicion
                datos[i] = solicitud.__dict__
                self._escribir_archivo(datos)			# Llama a su propia funcion
                return True
        return False

    def obtener_todos(self) -> List[Solicitud]:
        return [Solicitud(**item) for item in self._leer_archivo()]	# Recuperamos el diccionario de JSON y lo desarmamos como lista

    def _leer_archivo(self):
        with open(self.archivo_db, "r") as f:			# Usa with para garantizar el cierre correcto tras extraer los datos
            return json.load(f)					# Devuelve un diccionario python

    def _escribir_archivo(self, datos):
        with open(self.archivo_db, "w") as f:
            json.dump(datos, f, indent=4)			# convierte datos Python a JSON, con identado
