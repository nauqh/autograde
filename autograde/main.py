from abc import ABC, abstractmethod


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

    def __evaluate_special_cases(self, i, answer, correct_answers):
        correct_parts = [part.upper() for part in correct_answers.split(',')]
        submitted_parts = [part.upper() for part in answer.split(',')]

        if set(submitted_parts) == set(correct_parts):
            self.summary['Correct'].append(i)
        elif set(submitted_parts) & set(correct_parts):
            self.summary['Partial'].append(i)
        else:
            self.summary['Incorrect'].append(i)

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
            if not answer:
                self.summary['Not submitted'].append(i)
                continue

            if i >= 10:
                i += 1

            if answer == solution:
                self.summary['Correct'].append(i)
            else:
                self.summary['Incorrect'].append(i)

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


if __name__ == "__main__":
    # marker_m21 = M21Marker()
    # submission_m21 = ['A', '', 'c,e', 'B', 'E', 'A,C', 'A,C,D', 'A']
    # summary_m21 = marker_m21.check_multiple(submission_m21)
    # print(summary_m21)
    # marker_m21.display_summary(summary_m21)

    marker_m31 = M31Marker()
    submission_m31 = ['D', 'A', 'A', 'B', 'B',
                      'A', 'C', 'A', 'D', 'C', 'A', 'C']
    summary_m31 = marker_m31.check_multiple(submission_m31)

    summary_m31['Incorrect'].append(10)
    summary_m31['Not submitted'].append(14)
    summary_m31['Not submitted'].append(15)
    summary_m31['Not submitted'].append(16)
    print(summary_m31)
    marker_m31.display_summary(summary_m31)

    # marker_m12 = M12Marker()
    # submission_m12 = ['B', 'B', 'D', 'C', 'D',
    #                   'B', 'C', 'B', 'C', 'B', 'A', 'A', '3', '200', 'B']
    # summary_m12 = marker_m12.check_multiple(submission_m12)
    # print(summary_m12)
    # marker_m12.display_summary(summary_m12)
