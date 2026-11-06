"""
src/version_refactorizada/domain/enums.py: Elminamos la 'obsesión por los primitivos'

"""

from enum import Enum

class TipoSolicitudEnum(str, Enum):             # Define los tipos de solicitudes válidos del dominio
    EQUIVALENCIA = "Equivalencia"
    CERTIFICADO = "Certificado"
    EXAMEN = "Examen"
    BECA = "Beca"

class PrioridadEnum(str, Enum):                 # Define las prioridades permitidas
    BAJA = "Baja"
    MEDIA = "Media"
    ALTA = "Alta"
    URGENTE = "Urgente"

class EstadoSolicitudEnum(str, Enum):		        # Define los estados posibles del ciclo de vida de una solicitud
    PENDIENTE = "Pendiente"
    EN_PROCESO = "En Proceso"
    APROBADA = "Aprobada"
    RECHAZADA = "Rechazada"
