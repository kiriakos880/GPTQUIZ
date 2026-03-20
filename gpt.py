import openai
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk

client = openai.OpenAI(api_key="")

window = ThemedTk(theme="Adapta")
window.configure(themebg="#000F08")
window.geometry("600x650")
window.title("GPT Video Game Trivia")
window.resizable(False, False)

score = 0
total_asked = 0
current_answer = ""


def generate_question():
    global current_answer
    lbl.configure(text="Fetching next challenge...")
    window.update()

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a factual trivia bot. Generate a YES/NO question about video game history, "
                        "characters, or consoles. DO NOT use the word 'you' or ask about the player's history. "
                        "Keep it factual. Format: 'Question: <question> | Answer: <yes/no>'"
                    )
                },
                {"role": "user", "content": "Generate a factual video game question."}
            ]
        )

        result = response.choices[0].message.content.strip()

        question_part, answer_part = result.split("|")
        question_text = question_part.replace("Question:", "").strip()

        current_answer = answer_part.replace("Answer:", "").strip().lower().replace(".", "")

        lbl.configure(text=question_text)

    except Exception as e:
        lbl.configure(text="Error connecting to GPT.")


def check(user_choice):
    global score, total_asked

    if user_choice == current_answer:
        score += 1
        pb["value"] += 10

    total_asked += 1
    lblscore.configure(text=f"Score: {score} - Questions: {total_asked}")

    if total_asked >= 10:
        finish_game()
    else:
        generate_question()


def finish_game():
    framebuttons.pack_forget()
    pb.pack_forget()
    lbl.configure(text=f"Quiz Complete!\nFinal Score: {score} out of 10", font=("Arial", 18, "bold"))

    reset_btn = ttk.Button(window, text="Exit", command=lambda: window.destroy())
    reset_btn.pack(pady=20)


lbl = ttk.Label(window, text="", font=("Arial", 14), wraplength=500, justify="center")
lbl.pack(pady=80)

framebuttons = ttk.Frame(window)
framebuttons.pack()

yesbtn = ttk.Button(framebuttons, text="YES", command=lambda: check("yes"))
yesbtn.pack(side="left", padx=10)

nobtn = ttk.Button(framebuttons, text="NO", command=lambda: check("no"))
nobtn.pack(side="left", padx=10)

lblscore = ttk.Label(window, text="Score: 0 - Questions: 0")
lblscore.pack(pady=40)

pb = ttk.Progressbar(window, length=400, mode='determinate')
pb.pack()

generate_question()

window.mainloop()
