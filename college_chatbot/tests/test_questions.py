"""Held-out test: questions that are NOT in intents.json.

Run:  python tests/test_questions.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chatbot_engine import ChatBot  # noqa: E402

TESTS = [
    ("hello friend", "greeting"), ("good evening bot", "greeting"),
    ("ok bye then", "goodbye"), ("thank you for your help", "thanks"),
    ("what is your job", "about_bot"),
    ("when was this college started", "about_college"),
    ("which branches can i choose", "courses"),
    ("does the college have mechanical engineering", "courses"),
    ("tell me about the computer science department", "cse_course"),
    ("what is the procedure to get admission", "admission_process"),
    ("how do i register for counselling", "admission_process"),
    ("what percentage in 12th is needed", "eligibility"),
    ("which certificates do i need to submit", "documents"),
    ("how much is the yearly tuition fee", "fees"),
    ("can i pay my fees using upi", "fee_payment"),
    ("is there any scholarship for obc students", "scholarship"),
    ("do you provide hostel for girls", "hostel"),
    ("what is the average package offered", "placements"),
    ("which companies hire from your college", "placements"),
    ("is internship part of the course", "internship"),
    ("when does the library close", "library"),
    ("is there a bus from the city", "transport"),
    ("do you have a canteen and gym", "campus_facilities"),
    ("what clubs are there for students", "events_clubs"),
    ("what are the lecture timings", "timings"),
    ("when will semester exams happen", "academic_calendar"),
    ("what is the phone number of the admission office", "contact"),
    ("is ragging punished here", "anti_ragging"),
    ("what is the minimum attendance for exams", "attendance"),
    ("how many seats are in cse", "cse_course"),
    ("fees structre please", "fees"),          # typo
    ("hostl facilty", "hostel"),               # typo
    ("placment details", "placements"),        # typo
    ("what is the capital of france", "fallback"),
    ("tell me a joke", "fallback"),
    ("asdfgh qwerty", "fallback"),
]

bot = ChatBot()
correct = 0
for text, expected in TESTS:
    out = bot.reply(text)
    ok = out["intent"] == expected
    correct += ok
    print(f"[{'PASS' if ok else 'FAIL'}] {text!r:55} -> {out['intent']} ({out['confidence']})" + ("" if ok else f"   expected {expected}"))
print(f"\nScore: {correct}/{len(TESTS)} = {correct / len(TESTS) * 100:.1f}%")
