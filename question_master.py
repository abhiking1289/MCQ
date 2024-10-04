import csv
import logging

# Configure logging
logging.basicConfig(filename='question_master.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Question:
    def __init__(self, num, question, options, correct_option, category, difficulty):
        self.num = num
        self.question = question
        self.options = options
        self.correct_option = correct_option
        self.category = category
        self.difficulty = difficulty

class QuestionMaster:
    def __init__(self):
        self.questions = self.load_questions()

    def load_questions(self):
        questions = []
        try:
            with open('questions.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    options = {
                        'op1': row['option1'],
                        'op2': row['option2'],
                        'op3': row['option3'],
                        'op4': row['option4']
                    }
                    questions.append(Question(
                        int(row['num']),
                        row['question'],
                        options,
                        row['correctoption'],
                        row['category'],
                        row['difficulty']
                    ))
            logging.info("Questions loaded successfully.")
        except Exception as e:
            logging.error("Error loading questions: %s", e)
        return questions

    def add_question(self, question, options, correct_option, category, difficulty):
        if correct_option not in options.keys():
            print("Invalid correct option specified. Must be one of: op1, op2, op3, op4.")
            logging.warning("Invalid correct option: %s", correct_option)
            return

        num = len(self.questions) + 1
        self.questions.append(Question(num, question, options, correct_option, category, difficulty))
        logging.info("Added question: %s", question)

    def edit_question_options(self, num, options):
        for q in self.questions:
            if q.num == num:
                q.options.update(options)
                logging.info("Edited options for question number: %d", num)
                return
        logging.warning("Question %d not found for editing options.", num)

    def display_questions(self):
        if not self.questions:
            print("No questions available.")
            return

        print("\nAvailable Questions:")
        for q in self.questions:
            options_str = ', '.join(f"{k}) {v}" for k, v in q.options.items())
            print(f"{q.num}. {q.question} ({options_str}) - Category: {q.category} - Difficulty: {q.difficulty}")
        logging.info("Displayed all questions.")

    def search_questions_by_category(self, category):
        print(f"\nQuestions in category '{category}':")
        for q in self.questions:
            if q.category.lower() == category.lower():
                options_str = ', '.join(f"{k}) {v}" for k, v in q.options.items())
                print(f"{q.num}. {q.question} ({options_str})")
        logging.info("Searched questions by category: %s", category)

    def save_questions(self):
        with open('questions.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['num', 'question', 'option1', 'option2', 'option3', 'option4', 'correctoption', 'category', 'difficulty'])
            for q in self.questions:
                writer.writerow([q.num, q.question, q.options['op1'], q.options['op2'], q.options['op3'], q.options['op4'], q.correct_option, q.category, q.difficulty])
        logging.info("Questions saved to CSV.")

def main():
    qm = QuestionMaster()
    while True:
        print("\n1) Add a question")
        print("2) Edit question options")
        print("3) Search questions by category")
        print("4) Display all questions")
        print("5) Exit menu")
        choice = input("Select an option: ")

        if choice == '1':
            question = input("Enter question: ")
            options = {
                'op1': input("Enter option 1: "),
                'op2': input("Enter option 2: "),
                'op3': input("Enter option 3: "),
                'op4': input("Enter option 4: ")
            }
            correct_option = input("Enter correct option (op1/op2/op3/op4): ")
            category = input("Enter question category: ")
            difficulty = input("Enter question difficulty (Easy/Medium/Hard): ")
            qm.add_question(question, options, correct_option, category, difficulty)
            qm.save_questions()
        elif choice == '2':
            num = int(input("Enter question number to edit options: "))
            options = {
                'op1': input("Enter new option 1 (leave blank to keep current): ") or None,
                'op2': input("Enter new option 2 (leave blank to keep current): ") or None,
                'op3': input("Enter new option 3 (leave blank to keep current): ") or None,
                'op4': input("Enter new option 4 (leave blank to keep current): ") or None,
            }
            options = {k: v for k, v in options.items() if v}  # Keep only non-empty values
            qm.edit_question_options(num, options)
            qm.save_questions()
        elif choice == '3':
            category = input("Enter category to search for questions: ")
            qm.search_questions_by_category(category)
        elif choice == '4':
            qm.display_questions()
        elif choice == '5':
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
