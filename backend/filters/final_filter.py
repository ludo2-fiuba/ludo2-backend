from backend.filters.filter_helper import FilterHelper


class FinalFilter(FilterHelper):
    ALLOWED_FILTERS = ("grade", "year")

    def filter_grade(self, queryset, value):
        return queryset.filter(finalexam__grade=value)

    def filter_year(self, queryset, value):
        return queryset.filter(date__year=value)
