"""
src/version_refactorizada/services/estrategias_validacion.py: antes teniamos un metodo super largo, aca lo desarmamos con dos patrones

"""
from abc import ABC, abstractmethod				        #  Importa ABC (Abstract Base Class) y decorador @abstractmethod
from datetime import datetime
from src.version_refactorizada.domain.dtos import RegistroSolicitudDTO

class ValidacionStrategy(ABC):					          # Clase abstracta
    """
    PATRÓN: Strategy (Estrategia).
    Permite encapsular y aislar los algoritmos de validación según el tipo de solicitud,
    cumpliendo con el principio Open/Closed (OCP) ->  lo usamos para aislar el "cómo" se valida cada trámite
    """
    @abstractmethod						                    # Metodos que deben ser implementados a la manera de cada clase
    def validar(self, dto: RegistroSolicitudDTO) -> None:
        pass

class ValidacionEquivalencia(ValidacionStrategy):	# Valida reglas de negocio de este tramite
    def validar(self, dto: RegistroSolicitudDTO) -> None:	# Impplementacion concreta para el tramite de equivalencia
        if not dto.fecha_limite:
            raise ValueError("Las solicitudes de equivalencia requieren una fecha límite.")
        datetime.strptime(dto.fecha_limite, "%Y-%m-%d")

class ValidacionGenerica(ValidacionStrategy):			# Estrategia por defecto para los tipos sin reglas propias
    def validar(self, dto: RegistroSolicitudDTO) -> None:
        if len(dto.descripcion) < 15:
            raise ValueError("La descripción detallada debe tener al menos 15 caracteres para este trámite.")

class ValidadorFactory:
    """
    PATRÓN: Factory Method (Fábrica).
    Encapsula la lógica de creación y selección de la estrategia de validación correcta.
    -> lo usamos para que obntener la validacion correspondiente al tramite que queremos hacer
    """
    @staticmethod						                      #  no se instancia, se llama como metodo de ValidadorFactory
    def obtener_validador(tipo: str) -> ValidacionStrategy:
        if tipo == "Equivalencia":
            return ValidacionEquivalencia()
        return ValidacionGenerica()
