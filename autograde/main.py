from abc import ABC, abstractmethod
import pandas as pd
import re

"""
Issues:
    - Missing submission -> Must complete exam in one session
    - Irrelevant submission of functions -> Marked as incorrect
    - Wrong function name -> Marked as incorrect
"""


class ExamMarkerBase(ABC):
    def __init__(self):
        self.solutions = self.get_solutions()
        self.summary = self.initialize_summary()

    def initialize_summary(self):
        return {
            'Not submitted': [],
            'Incorrect': [],
            'Partial': [],
            'Correct': [],
        }

    @abstractmethod
    def get_solutions(self):
        pass

    @abstractmethod
    def check_multiple(self, submission):
        pass

    @abstractmethod
    def display_summary(self, submission):
        pass


class M21Marker(ExamMarkerBase):
    def __init__(self):
        super().__init__()
        self.exam_name = "M2.1"

    def get_solutions(self):
        return {
            "1": "A",
            "2": "B",
            "3": "c,e",
            "4": "B",
            "5": "E",
            "6": "A,C",
            "7": "C,D",
            "8": "C"
        }

    def check_multiple(self, submission):

        for i, answer in enumerate(submission, 1):
            solution = self.solutions.get(str(i))
            if not answer:
                self.summary['Not submitted'].append(i)
                continue

            if i in {3, 6, 7}:
                self.__evaluate_special_cases(i, answer, solution)
            else:
                if answer == solution:
                    self.summary['Correct'].append(i)
                else:
                    self.summary['Incorrect'].append(i)

        return self.summary

    def check_functions(self, s):
        self.test_q9(s)
        self.test_q10(s)
        self.test_q11(s)
        self.test_q12(s)
        self.test_q13(s)
        self.test_q14(s)

    def __evaluate_special_cases(self, i, answer, correct_answers):
        correct_parts = [part.upper() for part in correct_answers.split(',')]
        submitted_parts = [part.upper() for part in answer.split(',')]

        if set(submitted_parts) == set(correct_parts):
            self.summary['Correct'].append(i)
        elif set(submitted_parts) & set(correct_parts):
            self.summary['Partial'].append(i)
        else:
            self.summary['Incorrect'].append(i)

    def test_q9(self, s):
        if s[8] == '':
            self.summary['Not submitted'].append(9)
            return
        func_string = re.sub(r'^\s*def\s+(\w+)\s*\(',
                             rf'def count_min(', s[8], count=1)
        my_list_1 = [0, 1, 3, 2, 8, 0, 9, 10, 0, 5]
        my_list_2 = [-3, 0, 3, 4, 2, -1, 9, 6]

        local_vars = {}
        try:
            exec(func_string, globals(), local_vars)
        except Exception as e:
            print(
                f"Q9: Error occurred while executing function count_min - {e}")
        try:
            count_min = local_vars['count_min']
        except KeyError:
            print("Q9: function count_min not found")
            self.summary['Incorrect'].append(9)
            return

        if count_min(my_list_1) == 3 and count_min(my_list_2) == 1:
            self.summary['Correct'].append(9)
        else:
            self.summary['Incorrect'].append(9)

    def test_q10(self, s):
        if s[9] == '':
            self.summary['Not submitted'].append(10)
            return

        func_string = re.sub(r'^\s*def\s+(\w+)\s*\(',
                             rf'def calculate_range(', s[9], count=1)
        my_tuple_1 = (0, 1, 3, 2, 8, 0, 9, 10, 0, 5)
        my_tuple_2 = (-3, 0, 3, 4, 2, -1, 9, 6)

        local_vars = {}
        try:
            exec(func_string, globals(), local_vars)
        except Exception as e:
            print(
                f"Q10: Error occurred while executing function calculate_range - {e}")
        try:
            calculate_range = local_vars['calculate_range']
        except KeyError:
            print("Q10: function calculate_range not found")
            self.summary['Incorrect'].append(10)
            return

        if calculate_range(my_tuple_1) == 10 and calculate_range(my_tuple_2) == 12:
            self.summary['Correct'].append(10)
        else:
            self.summary['Incorrect'].append(10)

    def test_q11(self, s):
        if s[10] == '':
            self.summary['Not submitted'].append(11)
            return

        func_string = re.sub(r'^\s*def\s+(\w+)\s*\(',
                             rf'def extract_email(', s[10], count=1)
        local_vars = {}

        try:
            exec(func_string, globals(), local_vars)
        except Exception as e:
            print(
                f"Q11: Error occurred while executing function extract_email - {e}")
        try:
            extract_email = local_vars['extract_email']
        except KeyError:
            print("Q11: function extract_email not found")
            self.summary['Incorrect'].append(11)
            return

        correct_count = 0
        try:
            if extract_email('chinh.nguyen@coderschool.vn', True) == 'chinh.nguyen':
                correct_count += 1
            if extract_email('alexa1234@gmail.com', False) == 'gmail.com':
                correct_count += 1
            if extract_email('Joh*_D03+14/12@obviousscam.com', True) == 'Joh*_D03+14/12':
                correct_count += 1
        except Exception:
            if correct_count > 0:
                self.summary['Partial'].append(11)
            else:
                self.summary['Incorrect'].append(11)
            return

        if correct_count == 3:
            self.summary['Correct'].append(11)
        elif correct_count > 0:
            self.summary['Partial'].append(11)
        else:
            self.summary['Incorrect'].append(11)

    def test_q12(self, s):
        if s[11] == '':
            self.summary['Not submitted'].append(12)
            return

        func_string = re.sub(r'^\s*def\s+(\w+)\s*\(',
                             rf'def item_calculator(', s[11], count=1)
        item_1 = {'unit_weight': 1.5, 'unit_price': 2, 'number_of_units': 5}
        item_2 = {'unit_weight': 2.3, 'unit_price': 0.4, 'number_of_units': 3}

        local_vars = {}

        try:
            exec(func_string, globals(), local_vars)
        except Exception as e:
            print(
                f"Q12: Error occurred while executing function item_calculator - {e}")
        try:
            item_calculator = local_vars['item_calculator']
        except KeyError:
            print("Q12: function item_calculator not found")
            self.summary['Incorrect'].append(12)
            return

        if item_calculator(item_1, True) == 7.5 and item_calculator(item_1, False) == 10:
            self.summary['Correct'].append(12)
        else:
            self.summary['Incorrect'].append(12)

    def test_q13(self, s):
        receipt_1 = {
            'milk':   {'unit_weight': 1, 'unit_price': 10, 'number_of_units': 3},
            'rice':   {'unit_weight': 2, 'unit_price': 5, 'number_of_units': 4},
            'cookie': {'unit_weight': 0.2, 'unit_price': 2, 'number_of_units': 10},
            'sugar':  {'unit_weight': 0.5, 'unit_price': 7, 'number_of_units': 2},
        }

        receipt_2 = {
            'chair': {'unit_weight': 4.5, 'unit_price': 15, 'number_of_units': 2},
            'desk':  {'unit_weight': 10, 'unit_price': 22.5,  'number_of_units': 1}
        }
        if s[12] == '':
            self.summary['Not submitted'].append(13)
            return

        func_string = re.sub(r'^\s*def\s+(\w+)\s*\(',
                             rf'def heaviest_item(', s[12], count=1)
        local_vars = {}

        try:
            exec(func_string, globals(), local_vars)
        except Exception as e:
            print(
                f"Q13: Error occurred while executing function heaviest_item - {e}")
        try:
            heaviest_item = local_vars['heaviest_item']
        except KeyError:
            print("Q13: function heaviest_item not found")
            self.summary['Incorrect'].append(13)
            return

        if heaviest_item(receipt_1) == 'rice' and heaviest_item(receipt_2) == 'desk':
            self.summary['Correct'].append(13)
        else:
            self.summary['Incorrect'].append(13)

    def test_q14(self, s):
        receipt_1 = {
            'milk':   {'unit_weight': 1, 'unit_price': 10, 'number_of_units': 3},
            'rice':   {'unit_weight': 2, 'unit_price': 5, 'number_of_units': 4},
            'cookie': {'unit_weight': 0.2, 'unit_price': 2, 'number_of_units': 10},
            'sugar':  {'unit_weight': 0.5, 'unit_price': 7, 'number_of_units': 2},
        }

        receipt_2 = {
            'chair': {'unit_weight': 4.5, 'unit_price': 15, 'number_of_units': 2},
            'desk':  {'unit_weight': 10, 'unit_price': 22.5,  'number_of_units': 1}
        }
        if s[13] == '':
            self.summary['Not submitted'].append(14)
            return

        func_string = re.sub(r'^\s*def\s+(\w+)\s*\(',
                             rf'def priciest_item(', s[13], count=1)
        local_vars = {}
        try:
            exec(func_string, globals(), local_vars)
        except Exception as e:
            print(
                f"Q14: Error occurred while executing function priciest_item - {e}")

        try:
            priciest_item = local_vars['priciest_item']
        except KeyError:
            print("Q14: function priciest_item not found")
            self.summary['Incorrect'].append(14)
            return
        if priciest_item(receipt_1) == 'milk' and priciest_item(receipt_2) == 'chair':
            self.summary['Correct'].append(14)
        else:
            self.summary['Incorrect'].append(14)

    def mark_exam(self, submission):
        self.check_multiple(submission[:8])
        self.check_functions(submission)
        return self.summary

    def display_summary(self, summary):
        print(f"{self.exam_name} - EXAM SUMMARY")

        score_mapping = {
            'Correct': {range(1, 9): (4, '4/4'), range(9, 13): (12, '12/12'), range(13, 16): (10, '10/10')},
            'Partial': {range(1, 9): (2, '2/4'), range(9, 13): (6, '6/12'), range(13, 16): (5, '5/10')},
            'Incorrect': {range(1, 9): (0, '0/4'), range(9, 13): (0, '0/12'), range(13, 16): (0, '0/10')},
            'Not submitted': {range(1, 9): (0, '0/4'), range(9, 13): (0, '0/12'), range(13, 16): (0, '0/10')}
        }

        final_score = 0

        for status, questions in summary.items():
            print(f"{status}: {len(questions)}")
            for question in questions:
                score, max_score = next(
                    (v for k, v in score_mapping[status].items() if question in k), (0, '0/0'))
                print(f"  - Q{question} ({score}/{max_score.split('/')[1]})")
                final_score += score

        print(f"FINAL SCORE: {final_score}/100")


class M31Marker(ExamMarkerBase):
    def __init__(self):
        super().__init__()
        self.exam_name = "M3.1"
        self.__load_dataframe()

    def __load_dataframe(self):

        self.df = pd.read_csv(
            'https://raw.githubusercontent.com/anhquan0412/dataset/main/Salaries.csv')
        self.df.drop(columns=['Notes', 'Status', 'Agency'], inplace=True)
        self.df['JobTitle'] = self.df['JobTitle'].str.title()

    def get_solutions(self):
        return {
            "1": "D",
            "2": "A",
            "3": "A",
            "4": "B",
            "5": "B",
            "6": "A",
            "7": "C",
            "8": "A",
            "9": "D",
            "10": "C",
            "11": "A",
            "12": "C"
        }

    def check_multiple(self, submission):
        for i, answer in enumerate(submission, 1):
            solution = self.solutions.get(str(i))
            if i >= 10:
                i += 1

            if not answer:
                self.summary['Not submitted'].append(i)
                continue

            if answer == solution:
                self.summary['Correct'].append(i)
            else:
                self.summary['Incorrect'].append(i)

    def check_expression(self, s):
        self.test_q10(s)
        self.test_q14(s)
        self.test_q15(s)
        self.test_q16(s)

    def __exec_with_locals(self, index, df, s):
        string = "result = " + s[index]

        # Create a dictionary for local variables
        local_vars = {'df': df}

        # Execute the code with the local variables dictionary
        exec(string, globals(), local_vars)
        return local_vars['result']

    def test_q10(self, s):
        if s[9] == "":
            self.summary['Not submitted'].append(10)
            return
        result = self.__exec_with_locals(9, self.df, s)
        if self.df[self.df['TotalPay'] > self.df['TotalPay'].mean()].equals(result):
            self.summary['Correct'].append(10)
        else:
            self.summary['Incorrect'].append(10)

    def test_q14(self, s):
        if s[13] == "":
            self.summary['Not submitted'].append(14)
            return
        result = self.__exec_with_locals(13, self.df, s)
        if self.df['JobTitle'].value_counts().head().equals(result):
            self.summary['Correct'].append(14)
        else:
            self.summary['Incorrect'].append(14)

    def test_q15(self, s):
        if s[14] == "":
            self.summary['Not submitted'].append(15)
            return
        result = self.__exec_with_locals(14, self.df, s)
        df_top5 = self.df['JobTitle'].value_counts().head().index
        if len(self.df[self.df['JobTitle'].isin(df_top5)][['Year', 'JobTitle', 'BasePay', 'OvertimePay', 'TotalPay']]) == len(result):
            self.summary['Correct'].append(15)
        else:
            self.summary['Incorrect'].append(15)

    def test_q16(self, s):
        if s[15] == "":
            self.summary['Not submitted'].append(16)
            return
        result = self.__exec_with_locals(15, self.df, s)
        df_top5 = self.df['JobTitle'].value_counts().head().index
        sample = pd.pivot_table(data=self.df[self.df['JobTitle'].isin(df_top5)],
                                index=['JobTitle'],
                                columns=['Year'],
                                values=['BasePay', 'OvertimePay', 'TotalPay'])
        if len(sample) == len(result):
            self.summary['Correct'].append(16)
        else:
            self.summary['Incorrect'].append(16)

    def mark_exam(self, submission):
        self.check_multiple(submission[:9] + submission[10:13])
        self.check_expression(submission)
        return self.summary

    def display_summary(self, summary):
        print(f"{self.exam_name} - EXAM SUMMARY")

        score_mapping = {
            'Correct': {range(1, 10): (4, '4/4'), range(11, 14): (4, '4/4'),
                        (10, 14, 15): (14, '14/14'), range(16, 18): (10, '10/10')},
            'Incorrect': {range(1, 10): (0, '0/4'), range(11, 14): (0, '0/4'),
                          (10, 14, 15): (0, '0/14'), range(16, 18): (0, '0/10')},
            'Not submitted': {range(1, 10): (0, '0/4'), range(11, 14): (0, '0/4'),
                              (10, 14, 15): (0, '0/14'), range(16, 18): (0, '0/10')},
        }

        final_score = 0

        for status, questions in summary.items():
            print(f"{status}: {len(questions)}")
            for question in questions:
                score, max_score = next(
                    (v for k, v in score_mapping[status].items() if question in k), (0, '0/0'))
                print(f"  - Q{question} ({score}/{max_score.split('/')[1]})")
                final_score += score

        print(f"FINAL SCORE: {final_score}/100")


class M12Marker(ExamMarkerBase):
    def __init__(self):
        super().__init__()
        self.exam_name = "M1.2"

    def get_solutions(self):
        return {
            "1": "B",
            "2": "B",
            "3": "D",
            "4": ["A", "B"],
            "5": "D",
            "6": ["B", "D"],
            "7": "C",
            "8": "B",
            "9": ["C", "D"],
            "10": "B",
            "11": ["A", "B"],
            "12": ["A", "D"],
            "13": "3",
            "14": "200",
            "15": "B"
        }

    def check_multiple(self, submission):
        for i, answer in enumerate(submission, 1):
            solution = self.solutions.get(str(i))
            if not answer:
                self.summary['Not submitted'].append(i)
                continue

            if (i in {4, 6, 9, 11, 12} and answer in solution) or (answer == solution):
                self.summary['Correct'].append(i)
            else:
                self.summary['Incorrect'].append(i)

        return self.summary

    def display_summary(self, summary):
        print(f"{self.exam_name} - EXAM SUMMARY")

        for key, value in summary.items():
            print(f"{key}: {len(value)}")
            for question in value:
                if key == 'Correct':
                    score = '10/10' if question in (6, 8, 9, 13, 14) else "5/5"
                else:
                    score = '0/10' if question in (6, 8, 9, 13, 14) else "0/5"
                print(f"  - Q{question} ({score})")

        final_score = sum([10 if q in (6, 8, 9, 13, 14)
                          else 5 for q in summary.get('Correct', [])])
        print(f"FINAL SCORE: {final_score}/100")


class M11Marker(ExamMarkerBase):
    def __init__(self):
        super().__init__()
        self.exam_name = "M1.1"

    def get_solutions(self):
        return {
            "1": "A",
            "2": "B",
            "3": "A",
            "4": "B",
            "5": "B",
            "6": ["B", "D"],
            "7": "C",
            "8": "B",
            "9": ["C", "D"],
            "10": "B",
            "11": ["A", "B"],
            "12": ["A", "D"],
            "13": "3",
            "14": "200",
            "15": "B"
        }

    def check_multiple(self, submission):
        for i, answer in enumerate(submission, 1):
            solution = self.solutions.get(str(i))
            if not answer:
                self.summary['Not submitted'].append(i)
                continue

            if answer == solution:
                self.summary['Correct'].append(i)
            else:
                self.summary['Incorrect'].append(i)

        return self.summary

    def display_summary(self, summary):
        print(f"{self.exam_name} - EXAM SUMMARY")

        for key, value in summary.items():
            print(f"{key}: {len(value)}")
            for question in value:
                if key == 'Correct':
                    score = '2/2'
                else:
                    score = '0/2'
                print(f"  - Q{question} ({score})")

        final_score = sum([10 if q in (6, 8, 9, 13, 14)
                          else 2 for q in summary.get('Correct', [])])
        print(f"FINAL SCORE: {final_score}/100")


if __name__ == "__main__":
    marker_m21 = M21Marker()
    submission_m21 = ['A',
                      'C',
                      'c,e',
                      'B',
                      'E',
                      'A,C',
                      'C,D',
                      'C',
                      'def count_min(l):\n    i = 0\n    m = min(l)\n    for j in l:\n        if j == m:\n            i = i + 1\n    return(i)',
                      'def calculate_range(tup):\n    mn = min(tup)\n    mx = max(tup)\n    return(mx - mn)',
                      'def extract_email(emilz = "", snd_arg = True):\n    stri = str(emilz)\n    pattern = r"^([\\w\\d.]+)@([\\w\\d.]+)$"\n    match_obj = re.search(pattern, emilz)\n    if snd_arg == True:\n        return(match_obj.group(1))\n    else:\n        return(match_obj.group(2))',
                      "def item_calculator(item, arg):\n    if arg == True:\n        return(item['unit_weight']*item['number_of_units'])\n    else:\n        return(item['unit_price']*item['number_of_units'])",
                      "def heaviest_item(receipt):\n    mx_w = 0\n    k = ''\n    for x, obj in receipt.items():\n        #print(x)\n        for y in obj:\n            iw = obj['unit_weight']*obj['number_of_units']\n            if mx_w < iw:\n                mx_w = iw\n                k = x\n    return(k)",
                      "def priciest_item(receipt):\n    mx_p = 0\n    k = ''\n    for x, obj in receipt.items():\n        #print(x)\n        for y in obj:\n            ip = obj['unit_price']*obj['number_of_units']\n            if mx_p < ip:\n                mx_p = ip\n                k = x\n    # print(mx_p)\n    return(k)"]
    summary_m21 = marker_m21.mark_exam(submission_m21)
    marker_m21.display_summary(summary_m21)

    # marker_m31 = M31Marker()
    # s = ['D',
    #      'A',
    #      'A',
    #      'B',
    #      'B',
    #      'A',
    #      'C',
    #      'A',
    #      'D',
    #      "df[df['TotalPay'] > df['TotalPay'].mean()]",
    #      'C',
    #      'A',
    #      '',
    #      "df['JobTitle'].value_counts().head(5)",
    #      "df[df['JobTitle'].isin(df['JobTitle'].value_counts().head(5).index)][['Year', 'JobTitle', 'BasePay', 'OvertimePay', 'TotalPay']]",
    #      '']

    # summary_m31 = marker_m31.mark_exam(s)

    # print(summary_m31)
    # marker_m31.display_summary(summary_m31)

    # marker_m12 = M12Marker()
    # submission_m12 = ['B', 'B', 'D', 'C', 'D',
    #                   'B', 'C', 'B', 'C', 'B', 'A', 'A', '3', '200', 'B']
    # summary_m12 = marker_m12.check_multiple(submission_m12)
    # print(summary_m12)
    # marker_m12.display_summary(summary_m12)
