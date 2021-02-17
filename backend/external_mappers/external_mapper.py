class ExternalMapper:
    MAPPINGS = {
        'id': 'id', 'codigo': 'code', 'nombre': 'name', 'correlativas': 'correlatives',
        'materiaId': 'subject_id', 'docenteId': 'teacher_id', 'materia': 'subject', 'finalId': 'final_id',
        'notas': 'grades', 'departamento': 'department', 'departamentoId': 'department_id',
        'nombre': 'first_name', 'apellido': 'last_name', 'padron': 'file', 'legajo': 'file',
        'tipo_documento': 'document_type', 'numero_documento': 'dni', 'email': 'email'
    }

    def map(self, data):
        if type(data) is list:
            return [self._map(el) for el in data]
        elif type(data) is dict:
            return self._map(data)
        else:
            return data

    def _map(self, data):
        res = {}
        for key, val in data.items():
            if type(val) is list:
                res[self.MAPPINGS[key]] = [self.map(el) for el in val]
            elif type(val) is dict:
                res[self.MAPPINGS[key]] = self.map(val)
            else:
                res[self.MAPPINGS[key]] = val
        return res
