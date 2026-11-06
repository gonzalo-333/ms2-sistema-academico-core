""" 
src/version_refactorizada/domain/dtos.py: hacemos mas seguro y desacoplado el codigo inicial

"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from src.version_refactorizada.domain.enums import EstadoSolicitudEnum, PrioridadEnum, TipoSolicitudEnum

class RegistroSolicitudDTO(BaseModel):			            # Objeto de transferencia de datos para el registro
    model_config = ConfigDict(frozen=True)		          # frozen=True: una vez creado, el objeto no se puede modificar

    tipo: TipoSolicitudEnum
    estudiante_id: str = Field(..., min_length=3)
    descripcion: str = Field(..., min_length=10)
    prioridad: PrioridadEnum
    fecha_limite: Optional[str] = None			# Opcional

class ActualizacionSolicitudDTO(BaseModel):
    """
    PATRÓN: Parameter Object (Solución a Long Parameter List).
    Agrupa todos los parámetros de actualización en un objeto cohesivo e inmutable.
    Si mañana hace falta un octavo dato, se agrega un campo acá y no cambia la firma de ningún método.
    """
    model_config = ConfigDict(frozen=True)              # Inmutable, igual que el DTO de registro

    solicitud_id: int
    nuevo_estado: EstadoSolicitudEnum
    responsable: str
    observaciones: str
    area_asignada: str
    notificar_alumno: bool = True
    fecha_actualizacion: str
