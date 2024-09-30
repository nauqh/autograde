"""
Exam Marker V2
"""

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
    def check_multiple(self, submission):
        pass

    @abstractmethod
    def display_summary(self, submission):
        pass


class M11Marker(ExamMarkerBase):
    def __init__(self):
        super().__init__()
        self.exam_name = "M1.1"
        self.conn = sqlite3.connect("northwind.db")

    def get_solutions(self):
        with open('solutions/M11.json', 'r') as file:
            solutions = json.load(file)
        return solutions

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

    def check_sql(self, submission):
        for i, answer in enumerate(submission, 6):
            solution = self.solutions.get(str(i))
            if not answer:
                self.summary['Not submitted'].append(i)
                continue

            if Utils.check_sql(answer, solution, self.conn):
                self.summary['Correct'].append(i)
            else:
                self.summary['Incorrect'].append(i)

        return self.summary

    def display_summary(self, summary):
        print(f"{self.exam_name} - EXAM SUMMARY")

        for key, value in summary.items():
            print(f"{key}: {len(value)}")
            for question in value:
                if 1 <= question <= 5:
                    score = '2/2' if key == 'Correct' else '0/2'
                elif 6 <= question <= 9:
                    score = '3/3' if key == 'Correct' else '0/3'
                elif 10 <= question <= 15:
                    score = '8/8' if key == 'Correct' else '0/8'
                elif 16 <= question <= 20:
                    score = '6/6' if key == 'Correct' else '0/6'
                else:
                    score = '0/0'
                print(f"  - Q{question} ({score})")

        final_score = sum([
            2 if 1 <= q <= 5 else
            3 if 6 <= q <= 9 else
            8 if 10 <= q <= 15 else
            6 if 16 <= q <= 20 else 0
            for q in summary.get('Correct', [])
        ])

        print(f"FINAL SCORE: {final_score}/100")


if __name__ == '__main__':
    import requests
    email = "hodominhquan.self@gmail.com"
    response = requests.get(
        f"https://cspyclient.up.railway.app/submission/{email}")
    submission = response.json()['answers']
    s = [question['answer'] for question in submission]

    marker = M11Marker()
    summary = marker.check_multiple(s[:5])
    summary = marker.check_sql(s[5:])
    marker.display_summary(summary)
