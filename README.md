# LUNA
**Language-based Universal Networked Assistant**

A hybrid chatbot that combines rule-based intent recognition with Claude AI as a fallback for anything outside its defined intents. Built with Python and Flask.

---

## Overview

LUNA is a chatbot that understands common queries: greetings, jokes, time, date, basic math, using a rule-based intent matching system. For anything she doesn't recognize, she can escalate to Claude AI (coming in v2) so she can hold a real conversation, not just respond to keywords.

---

## How It Works

```
User types a message
→ Text is lowercased, tokenized, and stemmed
→ Matched against known intent patterns
→ Best matching intent selected by score
→ Dynamic intents (time, date, math) computed live
→ Static intents return a random predefined response
→ No match found → fallback response (v1) or Claude AI (v2)
```

---

## Features

- **Intent Recognition** — keyword matching with stemming so phrasing doesn't have to be exact
- **Dynamic Responses** — live time, date, and basic math calculations
- **Rule-Based Foundation** — greetings, farewells, jokes, and general knowledge
- **Graceful Fallback** — handles unrecognized input without breaking the conversation
- *(Coming in v2)* **Claude AI Integration** — handles anything outside LUNA's rule-based knowledge

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| NLP | NLTK (tokenization, stemming) |
| Intent Data | JSON |
| Frontend | HTML, CSS, JavaScript |
| AI Fallback *(planned)* | Anthropic Claude API |

---

## Project Structure

```
Luna_Chatbot/
├── app.py                  # Flask server and chatbot logic
├── intents.json            # Intent definitions (patterns + responses)
├── requirements.txt        # Python dependencies
├── static/
│   ├── style.css           # Chat UI styles
│   └── script.js           # Frontend chat logic
├── templates/
│   └── index.html          # Chat interface
└── README.md
```

---

## Roadmap

- [x] Design intent system and architecture
- [x] Build intents.json with core intent categories
- [x] Build Flask backend with intent matching logic
- [x] Add dynamic responses (time, date, math)
- [ ] Build chat UI (HTML/CSS/JS)
- [ ] Deploy to Railway
- [ ] Integrate Claude API as fallback (v2)
- [ ] Add conversation memory across sessions
- [ ] Add more intent categories

---

## Author

**Chase Harding**  
Full Stack Developer 
[GitHub](https://github.com/ChaseHarding)