"""
src/version_refactorizada/repository/base.py: hacemos una inversión de dependencias mediante una interfaz abstracta

"""
from abc import ABC, abstractmethod	# ABC: clase base abstracta; @abstractmethod: marca métodos que las subclases DEBEN implementar
from typing import List, Optional	# Tipos para anotar listas y valores que pueden ser None
from src.version_refactorizada.domain.models import Solicitud		# La entidad que se persiste

class SolicitudRepository(ABC):		# Interfaz abstracta (no se instancia): desacopla la lógica de negocio del almacenamiento
    
    @abstractmethod					# Persiste una solicitud nueva, le asigna un ID y devuelve ese ID.
    def guardar(self, solicitud: Solicitud) -> int:
        pass						# Sin cuerpo: la implementación la da cada subclase

    @abstractmethod					# Devuelve la solicitud con ese ID, o None si no existe
    def obtener_por_id(self, solicitud_id: int) -> Optional[Solicitud]:
        pass

    @abstractmethod					# Sobrescribe una solicitud existente. Devuelve True si la encontró, si no, False
    def actualizar(self, solicitud: Solicitud) -> bool:
        pass

    @abstractmethod
    def obtener_todos(self) -> List[Solicitud]:		# Devuelve todas las solicitudes almacenadas
        pass
