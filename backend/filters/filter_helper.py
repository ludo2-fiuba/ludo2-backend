class FilterHelper:
    ALLOWED_FILTERS = ()

    def __init__(self, queryset, filter_params):
        self.queryset = queryset
        self.filters = self._parse_filters(filter_params)

    def filter(self):
        for f, value in self.filters.items():
            try:
                self.queryset = getattr(self, "filter_" + f)(self.queryset, value)
            except AttributeError:
                pass
        return self.queryset

    def _parse_filters(self, filter_params):
        return dict(filter(lambda elem: elem[0] in self.ALLOWED_FILTERS, filter_params.items()))
