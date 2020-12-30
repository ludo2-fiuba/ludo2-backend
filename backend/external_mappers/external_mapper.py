class ExternalMapper:
    def map_multiple(self, elements):
        return [self.map_single(el) for el in elements]

    def map_single(self, el):
        return {
            val: el[key] for key, val in self.MAPPINGS.items()
        }

