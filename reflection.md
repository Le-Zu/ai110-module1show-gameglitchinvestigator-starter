# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start
  (for example: "the secret number kept changing" or "the hints were backwards").

It's a number guesser game that gives me 7 attempts to guess the number between 1 and 100. I started with 5 and made it to 99 where all the prompts said "Go HIGHER!", I guess 100 and it said "Go LOWER!". So I tried decimal numbers and of course was all over the place, ultimately running out of guesses. It turns out the secret number was 16, and I got a score of -5 instead of what I am assuming should have been 0.

Looking back a week later, I noticed more bugs that I hadn't noticed the first week. I suppose I didn't do a well job finding bugs the first time around.
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used Claude within the terminal. I actually just asked Claude to open the reflection.md and it offered to help me fill the questions out, I then answered #1 with my own words of what the app was and bugs I noticed. Claude suggested some lines that could be related to my observation, also giving an explanation to what logically went wrong with my guess. So I went and verified these explanations with the provided line numbers and referenced functions. There were other issue I found along the way as I checked the previous issues, that I didn't find the first time.

"(check_guess, lines 37–39), (lines 158–161), "update_score (lines 57–63)". Also below I provided the full offered response block from Claude.

"● Now I can see exactly what caused your experience. Here's a draft for section 1:
   ---
  What was broken when you started:                                                                                      
  When I first ran the game on Normal difficulty, it appeared functional — I had 7 attempts to guess a number between 1  
  and 100. However, the hints were completely backwards: when my guess was too low, it told me "Go LOWER!", and when my  
  guess was too high, it told me "Go HIGHER!" — the opposite of what they should say (check_guess, lines 37–39). This
  sent me chasing the wrong direction from the very start.

  The second bug was even sneakier: on every even-numbered attempt, the secret number was secretly converted to a string 
  before being compared to my integer guess (lines 158–161). This broke numeric comparison entirely — when I guessed 100 
  at an even attempt, Python compared the strings "100" vs "16" alphabetically, and since "0" < "6", it concluded "100" <
   "16" and told me "Go LOWER!" — which was both wrong and backwards. This is why I got wildly contradictory hints and   
  ended up nowhere near 16. The final score of -5 (instead of 0) was a third issue: the scoring logic in update_score    
  (lines 57–63) deducted 5 points for "Too Low" guesses and inconsistently added or subtracted 5 on "Too High" guesses   
  depending on whether the attempt number was even or odd.

  ---
  Want me to paste this directly into reflection.md, or would you like to tweak the wording first?"
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

A bug was really fixed when the app no longer presented the initial break in logic. I was not aware before of pytest. I was manualling reruninng Streamlit and testing the app, which I guess is the slow way. I later had Claude generate a pytest to test the app.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
- This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

Using detailed prompt sometimes the reponse fell short and required additional prompts if I wasn't specific. I would stop trying to fix 1 bug at a time and try fixing the bugs all at once with a detailed prompt, the amounts of prompts I made increased depending on the specificity, and question decisions/suggestions made.