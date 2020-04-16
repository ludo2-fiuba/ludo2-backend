from backend.filters.filter_helper import FilterHelper


class FinalExamFilter(FilterHelper):
    ALLOWED_FILTERS = ("grade",)

    def filter_grade(self, queryset, value):
        return queryset.filter(grade=value)

