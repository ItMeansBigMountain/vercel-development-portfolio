# Short-Form Coding Tutorial Script Pack 001

- **Project:** Store Code Content Studio
- **Created:** 2026-05-03
- **Purpose:** Reusable 15-45 second coding tutorial scripts that can promote the coding school, store, or future products without requiring account access or public posting.

## Usage pattern

Each script follows:

```text
Hook -> Mini lesson -> Visual idea -> CTA
```

Keep delivery fast, visual, and practical. Record with screen capture plus face/voiceover if desired.

---

## Script 1: Variables Are Labeled Boxes

- **Topic:** Beginner variables
- **Audience:** kids / beginner coders
- **Length:** 20-30 seconds

### Hook

"If your kid understands a lunchbox, they can understand variables."

### 15-45 second explanation

"A variable is just a labeled box. The label tells the computer what kind of thing is inside. If I write `score = 10`, I made a box called `score` and put `10` inside it. Later, when the player earns points, I can update the box: `score = score + 1`. That one idea powers games, apps, and calculators."

### Visual idea

Show a simple animation or slide:

```python
score = 10
score = score + 1
print(score)
```

Then show a game score increasing from 10 to 11.

### Store / school CTA

"Want your kid to learn coding through games? Follow for daily mini-lessons and check out our beginner coding resources."

---

## Script 2: If Statements Are Computer Decisions

- **Topic:** Conditionals
- **Audience:** beginner coders
- **Length:** 25-35 seconds

### Hook

"This is how games decide if you win or lose."

### 15-45 second explanation

"An `if` statement lets the computer make a decision. If health is less than or equal to zero, the player loses. Otherwise, the game keeps going. That simple decision pattern shows up everywhere: login screens, games, shopping carts, and apps."

### Visual idea

Show code beside a health bar:

```python
health = 0

if health <= 0:
    print("Game over")
else:
    print("Keep playing")
```

Animate health dropping to zero, then display "Game over".

### Store / school CTA

"Save this if your child is learning Python. We teach coding by building things kids actually care about."

---

## Script 3: Loops Save You From Repeating Yourself

- **Topic:** Loops
- **Audience:** kids / absolute beginners
- **Length:** 20-40 seconds

### Hook

"If you copy-paste code five times, a loop is probably hiding nearby."

### 15-45 second explanation

"A loop tells the computer to repeat something for you. Instead of writing `print('Ninja')` five times, I can write one loop that runs five times. Less code, fewer mistakes, cleaner thinking. Loops are how games move enemies, timers count down, and apps process lists."

### Visual idea

Show bad version vs clean version:

```python
print("Ninja")
print("Ninja")
print("Ninja")
```

Then replace with:

```python
for i in range(3):
    print("Ninja")
```

### Store / school CTA

"Follow for simple coding lessons that make kids dangerous — in the good way."

---

## Script 4: Lists Are Inventories

- **Topic:** Lists / arrays
- **Audience:** young game builders
- **Length:** 25-40 seconds

### Hook

"Your backpack in a game is basically a list."

### 15-45 second explanation

"A list stores multiple things in one place. In a game, your inventory might hold a sword, potion, and shield. In Python, that looks like this: `inventory = ['sword', 'potion', 'shield']`. Now the game can check what you have, add new items, or remove items when you use them."

### Visual idea

Show a backpack UI and code side-by-side:

```python
inventory = ["sword", "potion", "shield"]
inventory.append("key")
print(inventory)
```

Animate a key appearing in the backpack.

### Store / school CTA

"Want more coding lessons with game examples? Follow and grab our beginner-friendly worksheets when they drop."

---

## Script 5: Functions Are Reusable Moves

- **Topic:** Functions
- **Audience:** beginner coders / parents
- **Length:** 30-45 seconds

### Hook

"A function is like teaching the computer a special move."

### 15-45 second explanation

"Instead of writing the same steps again and again, we package them into a function. If a ninja game needs a jump move, I can write `jump()` once, then use it every time the player presses the button. Functions keep code organized and make big projects easier to build."

### Visual idea

Show a ninja sprite and button press:

```python
def jump():
    print("Ninja jumps!")

jump()
jump()
```

Animate the same move running twice from one reusable function.

### Store / school CTA

"If your kid wants to build games instead of just play them, follow for coding lessons and beginner project drops."

---

## Batch filming checklist

- Record all 5 in one session.
- Use one consistent visual template.
- Keep captions large and high contrast.
- End every video with one clear CTA.
- Do not mention products that are not ready yet; use soft CTAs like follow/save/check resources.
