"""
src/version_refactorizada/domain/models.py: modela entidad Solicitud, deshaciendo la clase gigante que teniamos anteriormente

"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any
from src.version_refactorizada.domain.enums import EstadoSolicitudEnum, PrioridadEnum, TipoSolicitudEnum

@dataclass
class Solicitud:
    """
    Entidad de Dominio enriquecida. 
    PATRÓN: Aplicamos 'Move Method', trasladando la lógica de validación 
    y de las fechas y enums directamente a la entidad.
    """
    id: int										# Identificador único (lo asigna el repositorio)
    tipo: TipoSolicitudEnum
    estudiante_id: str
    descripcion: str
    prioridad: PrioridadEnum
    estado: EstadoSolicitudEnum = EstadoSolicitudEnum.PENDIENTE				# Estado inicial por defecto
    fecha_creacion: str = field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )											# default_factory: se calcula al instanciar
    fecha_limite: str | None = None
    responsable: str = "Sin Asignar"							# por defecto
    observaciones: str = ""
    metadata_extra: Dict[str, Any] = field(default_factory=dict)			# si no se especifica, se crea nuevo y limpio
											# así no se pisan diccionarios entre instancias

    def cambiar_estado(									# Encapsula transición de estados segun modelo
        self, 
        nuevo_estado: EstadoSolicitudEnum, 						# Estado al que pasa la solicitud
        responsable: str, 								# Quien queda a cargo
        observaciones: str								# Comentario del cambio
    ) -> None:
        self.estado = nuevo_estado
        self.responsable = responsable
        self.observaciones = observaciones
