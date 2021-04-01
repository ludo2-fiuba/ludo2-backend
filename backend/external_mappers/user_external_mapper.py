from backend.external_mappers.external_mapper import ExternalMapper


class UserExternalMapper(ExternalMapper):
    MAPPINGS = {**ExternalMapper.MAPPINGS, **{
        'nombre': 'first_name', 'apellido': 'last_name', 'padron': 'file', 'legajo': 'file'
    }}
