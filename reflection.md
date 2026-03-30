# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**
- My initial UML design included four main classes: Owner, Pet, Task, and Scheduler.

- The Owner class represents the person using the app. Its responsibility is to store owner information, available time, preferences, and the list of pets.

- The Pet class represents each pet and stores details such as name, species, age, breed, care notes, and the tasks associated with that pet.

- The Task class represents individual care activities like feeding, walking, medication, grooming, or playtime. It holds details such as duration, priority, frequency, category, and completion status.

- The Scheduler class is responsible for collecting tasks from all pets, selecting tasks based on constraints like available time and priority, and generating a daily care plan. It also explains why certain tasks were chosen.

- This design keeps responsibilities separate and makes it easier to implement, test, and extend later.

**b. Design changes**
- One design change I made was keeping the Scheduler separate from the Pet and Owner classes instead of placing scheduling logic inside Owner. I made this change because scheduling is a separate responsibility and deserves its own class. This makes the design cleaner and easier to test.

- I also used Python dataclasses for Pet and Task because they mainly store structured data. This reduced boilerplate code and made the class definitions easier to read.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- My scheduler considers several basic constraints: available time, task completion status, and task due time. It only includes incomplete tasks in the daily plan, sorts them by due time, and then adds tasks until the owner's available time limit is reached.

- How did you decide which constraints mattered most?
- I decided these constraints mattered most because they are the most practical for a pet care app. A pet owner first needs to know which tasks still need to be done, when they are due, and whether they fit into the time available for the day. I kept the logic simple so the schedule is easy to understand and test.


**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- One tradeoff my scheduler makes is that conflict detection only checks for exact matching times, such as two tasks both scheduled at 09:00. It does not yet detect overlapping durations, such as a 09:00–09:30 task conflicting with a 09:15–09:45 task.

- Why is that tradeoff reasonable for this scenario?
- This tradeoff is reasonable for this scenario because it keeps the logic lightweight, readable, and easy to debug while still providing useful warnings. For an early version of PawPal+, exact-time conflict detection is enough to show the idea of scheduling conflicts without making the system too complex.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
