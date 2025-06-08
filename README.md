# Basic WhatsApp Chatbot

A simple WhatsApp chatbot built using **Twilio**, **Flask**, and **Firebase**.

---

## What It Does

- Responds to WhatsApp messages using basic **text commands**
- Example: Sending `1` selects a specific option
- Maintains conversational state using a **simple DFA (Deterministic Finite Automaton)**  
  → Transitions between message states based on user input
- Uses **Firebase** to store the **current state** of each user  
  → Each user is uniquely identified using their **phone number**

---

## Tech Stack

- **Flask** – lightweight backend framework  
- **Twilio API** – for sending and receiving WhatsApp messages  
- **Firebase** – for storing user state persistently  
- **Python** – for logic and state management

---

## How It Works

- Each incoming message is processed and checked for command input (like `1`, `2`, etc.)
- A small DFA structure determines what message or action to send next
- The current **state** of each user is saved in **Firebase**, keyed by their phone number
- This allows conversations to resume or continue based on prior interactions

---

## Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Flask server:
   ```bash
   python app.py
   ```

3. Set up a Twilio WhatsApp sandbox, Firebase Realtime database and configure the webhook to point to your local server (use [ngrok](https://ngrok.com/) or similar if needed).

4. Ensure Firebase and twilio credentials are set up properly in your project for authentication and read/write access.

---

## Notes

- This is a **basic prototype**, ideal for learning how to connect WhatsApp, persist state, and build interactive flows
- Can be extended with:
  - Richer state trees or hierarchical DFAs
  - NLP for smarter inputs
  - Authentication and user data tracking

