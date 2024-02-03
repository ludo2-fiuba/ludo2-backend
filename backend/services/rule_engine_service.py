import rule_engine

#from backend.views.utils import is_before_current_datetime


class RuleEngineService:
    
    def __init__(self):
        self.rules = []
        self.evaluation_rules = []


    def generate_passing_rules(self, semester):
        if(semester['classes_amount'] and semester['minimum_attendance']):
            max_absences = semester['classes_amount'] - (semester['classes_amount'] * semester['minimum_attendance'])
            self.add_assistance_threshold(max_absences)
        for evaluation in semester['evaluations']:
            self.add_evaluation_rule(evaluation)


    def add_evaluation_rule(self, evaluation):
        if evaluation['is_graded'] and is_before_current_datetime(evaluation['end_date']):
            rule = rule_engine.Rule(f'evaluation.evaluation_name == {evaluation["evaluation_name"]} and (grade >= {evaluation["passing_grade"]} or corrector == None)')
            self.evaluation_rules.append(rule)
    

    def add_assistance_threshold(self, max_absences):
        rule = rule_engine.Rule(f'absences <= {max_absences}')
        self.rules.append(rule)

    
    def is_student_passing(self, attendances, evaluation_submissions, student):
        print(attendances)
        print(evaluation_submissions)
        model_for_rules = {}
        model_for_rules['absences'] = self.get_absences(attendances, student)
        is_passing = True
        for rule in self.rules:
            is_passing = is_passing and rule.evaluate(model_for_rules)
        for rule in self.evaluation_rules:
            passing_evaluations = rule.filter(evaluation_submissions)
            is_empty = True
            for evaluation in passing_evaluations:
                is_empty = False
            is_passing = is_passing and not is_empty
        

    
    def get_absences(self, attendances, student):
        absences = 0
        for attendace in attendances:
            is_absent = True
            for a_student in attendace['attendace']:
                if a_student['id'] == student['id']:
                    is_absent = False
            if is_absent:
                absences = absences + 1
        return absences



rule = rule_engine.Rule(f'average.exam >= 7 and average.name == "Examen 1"')
isValid = rule.is_valid(f'average.exam >= 7 and average.name == "Examen 1"')
evaluateReturn = rule.evaluate({'average': {'exam': 7, 'name': 'Examen 1'}})
matchesReturn = rule.matches({'average': {'exam': 6}})
filterReturn = rule.filter([{'average': {'exam': 7, 'name': 'Examen 1'}}, {'average': {'exam': 7, 'name': 'Examen 2'}}])
isEmpty = filterReturn
for result in filterReturn:
    currentResult = result
isValid = True