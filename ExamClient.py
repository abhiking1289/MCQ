import csv
import os
import json
from datetime import datetime
import time

class ExamClient:
    def __init__(self, csv_file='questions.csv'):
        self.csv_file = csv_file
        self.questions = []
        self.load_questions()
        self.categories = set(q['category'] for q in self.questions)

    def load_questions(self):
        """ Load questions from the CSV file """
        if os.path.exists(self.csv_file):
            with open(self.csv_file, mode='r') as file:
                reader = csv.DictReader(file)
                self.questions = [row for row in reader]

    def conduct_exam(self):
        """ Conduct the exam by asking questions to the user """
        if not self.questions:
            print("No questions available for the exam.")
            return

        student_name = input("Enter student name: ")
        university = input("Enter university: ")
        score = 0
        answers = []

        print(f"\nExam started: {datetime.now().strftime('%d/%b/%Y %H:%M:%S')}")
        print(f"Student: {student_name}, University: {university}\n")

        exam_duration = int(input("Enter exam duration in seconds: "))
        start_time = time.time()

        for q in self.questions:
            if time.time() - start_time >= exam_duration:
                print("Time is up!")
                break

            print(f"Q{q['num']}: {q['question']}")
            print(f"1) {q['option1']}  2) {q['option2']}  3) {q['option3']}  4) {q['option4']}")
            user_choice = input("Enter your choice (1-4): ")
            answers.append((q['num'], user_choice))

            if user_choice in ['1', '2', '3', '4'] and f'op{user_choice}' == q['correctoption']:
                score += 1

        self.save_results(student_name, university, score, answers)

    def save_results(self, student_name, university, score, answers):
        """ Save exam results to a file """
        results = {
            "date": datetime.now().strftime('%d/%b/%Y %H:%M:%S'),
            "student": student_name,
            "university": university,
            "score": score,
            "total_questions": len(self.questions),
            "answers": answers
        }
        
        results_file = 'exam_results.json'
        with open(results_file, 'a') as f:
            json.dump(results, f)
            f.write("\n")
        
        print(f"Exam Completed! Marks scored: {score} out of {len(self.questions)}")
        print(f"Results saved to {results_file}")

    def review_answers(self, answers):
        print("\nReview Your Answers:")
        for num, answer in answers:
            print(f"Q{num}: Your answer: {answer}")

if __name__ == "__main__":
    ec = ExamClient()
    ec.conduct_exam()
