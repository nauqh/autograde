from abc import ABC, abstractmethod
import json
import sqlite3
from autograde.utils import Utils


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
    def mark_submission(self, submission):
        pass

    @abstractmethod
    def display_summary(self, submission):
        pass

    def update_summary(self, question_number, correct):
        if correct is None:
            self.summary['Not submitted'].append(question_number)
        elif correct:
            self.summary['Correct'].append(question_number)
        else:
            self.summary['Incorrect'].append(question_number)


class M11Marker(ExamMarkerBase):
    QUESTION_SCORES = {
        range(1, 6): 2,
        range(6, 10): 3,
        range(10, 16): 8,
        range(16, 21): 6,
    }

    def __init__(self):
        super().__init__()
        self.exam_name = "M1.1"
        self.conn = sqlite3.connect("northwind.db")

    def get_solutions(self):
        with open('solutions/M11.json', 'r') as file:
            return json.load(file)

    def check_submission(self, submission, is_sql=False, start_index=1):
        for i, answer in enumerate(submission, start_index):
            solution = self.solutions.get(str(i))
            correct = None

            if answer:
                if is_sql:
                    correct = Utils.check_sql(answer, solution, self.conn)
                else:
                    correct = answer == solution

            self.update_summary(i, correct)

    def mark_submission(self, submission):
        self.check_submission(submission[:5], is_sql=False, start_index=1)
        self.check_submission(submission[5:], is_sql=True, start_index=6)
        return self.summary

    def calculate_score(self, question_number):
        for question_range, score in self.QUESTION_SCORES.items():
            if question_number in question_range:
                return score
        return 0

    def calculate_final_score(self):
        return sum(self.calculate_score(q) for q in self.summary['Correct'])

    def display_summary(self, summary):
        print(f"{self.exam_name} - EXAM SUMMARY")

        for key, value in summary.items():
            print(f"{key}: {len(value)}")
            for question in value:
                score = f"{self.calculate_score(question)}/{self.calculate_score(question)}" if key == 'Correct' else "0"
                print(f"  - Q{question} ({score})")

        final_score = self.calculate_final_score()
        print(f"FINAL SCORE: {final_score}/100")


if __name__ == '__main__':
    import requests
    email = "hodominhquan.self@gmail.com"
    response = requests.get(
        f"https://cspyclient.up.railway.app/submission/{email}")
    submission = response.json()['answers']
    s = [question['answer'] for question in submission]

    marker = M11Marker()
    marker.mark_submission(s)
    marker.display_summary(marker.summary)
