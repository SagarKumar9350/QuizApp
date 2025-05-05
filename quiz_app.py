import customtkinter as ctk
import tkinter.messagebox as msg
import requests
import random
import html

# Set theme and appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Create root window
root = ctk.CTk()
root.geometry("800x500")
root.title("Quiz App")

# Global variables
quiz_data = []
question_index = 0
score = 0

# Category mapping for OpenTDB
category_map = {
    "Any": None,
    "General Knowledge": 9,
    "Science: Computers": 18,
    "History": 23,
    "Sports": 21
}

# Fetch quiz questions from API
def fetch_questions(amount, category, difficulty):
    url = "https://opentdb.com/api.php"
    params = {
        "amount": amount,
        "type": "multiple"
    }

    if category:
        params["category"] = category
    if difficulty != "Any":
        params["difficulty"] = difficulty.lower()

    try:
        response = requests.get(url, params=params)
        data = response.json()
        return data['results']
    except:
        msg.showerror("Error", "Failed to fetch quiz questions!")
        return []

# Start quiz on button click
def start_quiz():
    global quiz_data, question_index, score
    question_index = 0
    score = 0
    try:
        amount = int(entry_num.get())
    except ValueError:
        msg.showerror("Error", "Enter a valid number of questions!")
        return

    category_name = dropdown_category.get()
    category = category_map[category_name]
    difficulty = dropdown_difficulty.get()

    quiz_data = fetch_questions(amount, category, difficulty)

    if quiz_data:
        settings_frame.pack_forget()
        show_question()
    else:
        msg.showerror("Error", "No questions found. Try different settings.")

# Display current question and options
def show_question():
    global question_index, quiz_data, options

    current_question = quiz_data[question_index]
    question_text = html.unescape(current_question['question'])

    correct = html.unescape(current_question['correct_answer'])
    incorrect = [html.unescape(opt) for opt in current_question['incorrect_answers']]

    options = incorrect + [correct]
    random.shuffle(options)

    quiz_frame.pack(fill="both", expand=True)
    question_label.configure(text=f"Q{question_index + 1}: {question_text}")

    for i in range(4):
        buttons[i].configure(text=options[i], command=lambda opt=options[i]: check_answer(opt))

# Check user's selected answer
def check_answer(selected):
    global score, question_index

    correct_answer = html.unescape(quiz_data[question_index]['correct_answer'])

    if selected == correct_answer:
        score += 1

    question_index += 1

    if question_index < len(quiz_data):
        show_question()
    else:
        show_result()

# Show result screen
def show_result():
    quiz_frame.pack_forget()

    result_frame = ctk.CTkFrame(root)
    result_frame.pack(pady=20, padx=20, fill="both", expand=True)

    result_label = ctk.CTkLabel(result_frame, text="🎉 Quiz Completed!", font=("Arial", 30, "bold"))
    result_label.pack(pady=20)

    score_label = ctk.CTkLabel(result_frame, text=f"You scored {score} out of {len(quiz_data)}", font=("Arial", 24))
    score_label.pack(pady=10)

    retry_btn = ctk.CTkButton(result_frame, text="Take Another Quiz", command=lambda: restart_quiz(result_frame))
    retry_btn.pack(pady=20)

# Restart the quiz
def restart_quiz(frame_to_destroy):
    frame_to_destroy.destroy()
    settings_frame.pack(pady=20)

# ---------------- UI Layout ----------------

# Settings screen
settings_frame = ctk.CTkFrame(root)
settings_frame.pack(pady=20)

ctk.CTkLabel(settings_frame, text="🧠 QUIZ APP", font=("Arial", 24)).pack(pady=10)

entry_num = ctk.CTkEntry(settings_frame, placeholder_text="Number of Questions", width=200)
entry_num.pack(pady=5)

dropdown_category = ctk.CTkOptionMenu(settings_frame, values=list(category_map.keys()))
dropdown_category.set("Category")
dropdown_category.pack(pady=5)

dropdown_difficulty = ctk.CTkOptionMenu(settings_frame, values=["Any", "Easy", "Medium", "Hard"])
dropdown_difficulty.set("Difficulty")
dropdown_difficulty.pack(pady=5)

ctk.CTkButton(settings_frame, text="Start Quiz", command=start_quiz).pack(pady=10)

# Quiz screen
quiz_frame = ctk.CTkFrame(root)

question_label = ctk.CTkLabel(quiz_frame, text="", font=("Arial", 20), wraplength=600)
question_label.pack(pady=20)

buttons = []
for _ in range(4):
    btn = ctk.CTkButton(quiz_frame, text="", width=400)
    btn.pack(pady=5)
    buttons.append(btn)

# Run the app
root.mainloop()
