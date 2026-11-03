# College FAQ Chatbot (Smart AI Chatbot mini project)

A web chatbot that answers college questions (admissions, fees, courses, hostel,
placements, scholarships, library, transport, contact) using machine learning.

**Tech:** Python, Flask, scikit-learn (TF-IDF + Logistic Regression), HTML, CSS, JavaScript.

## Run it (4 steps)

```bash
# 1. (optional but recommended) create a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac / Linux

# 2. install packages
pip install -r requirements.txt

# 3. train the model (prints accuracy, creates model.pkl)
python train.py

# 4. start the website
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

## Folder structure

```
college_chatbot/
├── app.py               Flask server: serves the page and the /chat API
├── chatbot_engine.py    Text cleaning, model training, prediction, fallback
├── train.py             Trains the model and prints cross-validation accuracy
├── intents.json         Training data + replies (EDIT THIS for your college)
├── templates/index.html Chat page
├── static/style.css     Design
├── static/script.js     Sends messages to /chat, shows replies, clear chat
├── tests/test_questions.py  36 unseen questions to measure accuracy
└── requirements.txt
```

## Make it your own college (do this before the viva)

1. Open `intents.json`, change `college_name` and replace every placeholder
   answer (fees, phone, address, placement numbers) with real details.
2. Run `python train.py` again.
3. Run `python tests/test_questions.py` to check nothing broke.

To add a topic: add a new block with a `tag`, 15+ example `patterns`, and `responses`.

## How it works

1. User types a message in the browser.
2. `script.js` sends it to `POST /chat` as JSON: `{"message": "..."}`.
3. `app.py` passes it to `chatbot_engine.py`.
4. The text is cleaned (lowercase, no punctuation).
5. TF-IDF turns it into numbers (word pairs plus 2-4 letter chunks, so small spelling mistakes still work).
6. Logistic Regression predicts the intent and a confidence score.
7. If confidence is 0.30 or higher, a reply for that intent is returned; otherwise a polite fallback.
8. The reply is shown in the chat window.

## Accuracy (be honest in your viva)

- Cross-validation (train on 75% of sentences, test on unseen 25%): about 83%.
- `tests/test_questions.py` (36 hand-written questions): 100% at the time of writing,
  but some phrases were added to training after the first run, so treat ~83% as the realistic figure.
- Adding more example sentences per intent is the best way to improve it.

## Viva cheat sheet

**What is TF-IDF?** It scores how important a word is in a sentence: words that are
frequent in the sentence but rare across all sentences get a higher score.

**Why Logistic Regression?** It is fast, works well on small text datasets, and
gives probabilities, which we use as a confidence score.

**What is an intent?** The purpose behind a question, such as "fees" or "hostel".

**What if the bot doesn't know?** If confidence is below 0.30 it shows a fallback
message instead of a wrong answer.

**Why not ChatGPT / an LLM API?** An LLM needs internet, an API key and has usage
limits. This project is offline, free, and every step is ours to explain.

**Limitations:** it only knows topics in `intents.json`, has no memory of earlier
messages, and cannot do arithmetic or open-ended chat.

**Future scope:** multi-language replies (Marathi/Hindi), voice input, a database
for facts, admin page to edit intents, an LLM fallback for unknown questions.

## Notes

- `app.run(debug=True)` is for development. Do not use it for a public deployment.
- If you see "model.pkl" errors after upgrading scikit-learn, delete `model.pkl` and run `python train.py`.
