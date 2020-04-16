from backend.filters.filter_helper import FilterHelper


class SubjectFilter(FilterHelper):
    ALLOWED_FILTERS = ("name", "grade", "year")

    def filter_name(self, queryset, value):
        return queryset.filter(name=value)

    def filter_grade(self, queryset, value):
        return queryset.filter(final__finalexam__grade=value)

    def filter_year(self, queryset, value):
        return queryset.filter(final__date__year=value)
