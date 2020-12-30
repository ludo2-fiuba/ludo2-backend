from backend.external_mappers.external_mapper import ExternalMapper


class SubjectMapper(ExternalMapper):
    MAPPINGS = {
        'id': 'id', 'codigo': 'code', 'nombre': 'name', 'correlativas': 'correlatives'
    }
