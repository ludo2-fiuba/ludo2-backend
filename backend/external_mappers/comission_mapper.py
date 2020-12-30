from backend.external_mappers.external_mapper import ExternalMapper


class ComissionMapper(ExternalMapper):
    MAPPINGS = {
        'id': 'id', 'nombre': 'name', 'materiaId': 'subject_id', 'docenteId': 'teacher_id'
    }
