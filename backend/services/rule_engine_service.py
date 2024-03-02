import rule_engine

from backend.views.utils import is_before_current_datetime


class RuleEngineService:
    
    def __init__(self):
        self.rules = []
        self.evaluation_rules = []


    def generate_passing_rules(self, semester):
        if(semester['classes_amount'] and semester['minimum_attendance']):
            max_absences = semester['classes_amount'] - (semester['classes_amount'] * semester['minimum_attendance'])
            self.add_assistance_threshold(max_absences)

        evaluations_accounted_for = []
        for evaluation in semester['evaluations']:
            print(evaluation)
            if evaluation not in evaluations_accounted_for:
                evaluations_for_rule = []
                evaluations_for_rule.append(evaluation)
                while evaluation['make_up_evaluation']:
                    evaluation = evaluation['make_up_evaluation']
                    print(evaluation)
                    evaluations_for_rule.append(evaluation)
                self.add_evaluation_rule(evaluations_for_rule)
                evaluations_accounted_for.append(evaluations_for_rule)
        print(evaluations_accounted_for)


    def add_evaluation_rule(self, evaluations): # ESTO ESTA MAL
        rule_string = ""
        for evaluation in evaluations:
            if evaluation['is_graded'] and is_before_current_datetime(evaluation['end_date']):
                rule_string += f'(evaluation.evaluation_name == "{evaluation["evaluation_name"]}" and (grader == null or grade >= {evaluation["passing_grade"]})) or '
        rule_string = rule_string[:-4]
        rule = rule_engine.Rule(rule_string)
        print(rule_string)
        self.evaluation_rules.append(rule)
    

    def add_assistance_threshold(self, max_absences):
        rule = rule_engine.Rule(f'absences <= {max_absences}')
        print(f'absences <= {max_absences}')
        self.rules.append(rule)

    
    def is_student_passing(self, attendanceQRs, evaluation_submissions, student):
        print(attendanceQRs)
        print(evaluation_submissions)
        print(student)
        model_for_rules = {}
        model_for_rules['absences'] = self.get_absences(attendanceQRs, student)
        is_passing = True

        for rule in self.rules:
            is_passing = is_passing and rule.evaluate(model_for_rules)

        print(is_passing)

        for rule in self.evaluation_rules:
            passing_evaluations = rule.filter(evaluation_submissions)
            is_empty = True
            for evaluation in passing_evaluations:
                is_empty = False
            is_passing = is_passing and not is_empty

        print(is_passing)
        print(model_for_rules)
        
        return is_passing
        

    
    def get_absences(self, attendanceQRs, student):
        absences = 0
        for attendances in attendanceQRs:
            is_absent = True
            for attendance in attendances['attendances']:
                a_student = attendance['student']
                if a_student['id'] == student['id']:
                    is_absent = False
            if is_absent:
                absences = absences + 1
        return absences



""" rule = rule_engine.Rule(f'average.exam >= 7 and average.name == "Examen 1"')
isValid = rule.is_valid(f'average.exam >= 7 and average.name == "Examen 1"')
evaluateReturn = rule.evaluate({'average': {'exam': 7, 'name': 'Examen 1'}})
matchesReturn = rule.matches({'average': {'exam': 6}})
filterReturn = rule.filter([{'average': {'exam': 7, 'name': 'Examen 1'}}, {'average': {'exam': 7, 'name': 'Examen 2'}}])
isValid = True
isEmpty = True
for result in filterReturn:
    isEmpty = False
    currentResult = result
isTrue = isValid and not isEmpty
isValid = True """