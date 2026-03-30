# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- My initial UML design included four main classes: Owner, Pet, Task, and Scheduler.

- The Owner class represents the user of the app and is responsible for storing basic information such as name, available time, preferences, and the list of pets.

- The Pet class represents each pet and stores attributes like name, species, age, and associated care tasks.

- The Task class represents individual activities such as feeding, walking, or grooming. It stores details like duration, due time, frequency, and completion status.

- The Scheduler class acts as the core logic layer. It collects tasks from all pets, sorts and filters them, builds a daily plan based on constraints, and provides explanations for scheduling decisions.

---

**b. Design changes**

- Yes, my design evolved during implementation.

- One key change was adding attributes like `due_time` and `due_date` to the Task class to support sorting and recurring tasks. Initially, tasks only had duration, but this was not sufficient for scheduling.

- Another change was extending the Scheduler class to include additional methods such as sorting, filtering, conflict detection, and recurrence handling. This made the system more modular and aligned with real-world scheduling needs.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- My scheduler considers the following constraints:
  - Available time of the owner
  - Task completion status (only incomplete tasks are scheduled)
  - Task due time (used for sorting)
  - Task duration

- I prioritized these constraints because they directly impact a pet owner’s daily planning. The goal was to ensure tasks are realistic, manageable within available time, and ordered logically.

---

**b. Tradeoffs**

- One tradeoff my scheduler makes is that conflict detection only checks for exact matching times (e.g., two tasks at 09:00) rather than detecting overlapping durations.

- This tradeoff is reasonable because it keeps the implementation simple, readable, and easy to test. While it does not capture all real-world conflicts, it still provides useful warnings without adding unnecessary complexity to the system.

---

## 3. AI Collaboration

**a. How you used AI**

- I used AI tools, especially VS Code Copilot, for multiple stages of development:
  - Designing the system structure and UML
  - Generating class skeletons
  - Implementing methods such as sorting, filtering, and scheduling
  - Writing and improving test cases
  - Debugging errors and refining logic

- The most helpful prompts were specific and context-based, such as:
  - “How should Scheduler retrieve tasks from Owner?”
  - “How can I sort tasks by time using Python?”
  - “Why is this test failing?”

---

**b. Judgment and verification**

- One instance where I modified an AI suggestion was when it proposed a more complex scheduling or conflict detection logic than needed. I simplified the solution to keep the system readable and aligned with project requirements.

- I verified AI suggestions by:
  - Running the code and checking outputs in `main.py`
  - Writing and executing pytest test cases
  - Reviewing whether the solution matched the project’s goals and constraints

---

## 4. Testing and Verification

**a. What you tested**

- I tested several key behaviors:
  - Task completion updates status correctly
  - Adding tasks to a pet increases the task list
  - Sorting tasks by due time works correctly
  - Recurring tasks are generated when a task is completed
  - Conflict detection identifies tasks with the same time
  - Filtering tasks by pet name returns correct results

- These tests were important because they validate the core logic of the scheduler and ensure that the system behaves as expected under normal and edge conditions.

---

**b. Confidence**

- I am confident in the system at a level of 4 out of 5.

- The core features such as scheduling, sorting, filtering, and recurrence are well tested and functioning correctly.

- If I had more time, I would test additional edge cases such as:
  - Overlapping task durations (not just exact time matches)
  - Invalid time formats
  - Very large numbers of tasks
  - UI-level interactions in Streamlit

---

## 5. Reflection

**a. What went well**

- The part I am most satisfied with is successfully building a complete system from design to implementation, including backend logic, UI integration, and automated testing.

- The separation of concerns between classes (especially keeping Scheduler independent) worked well and made the system easier to manage.

---

**b. What you would improve**

- If I had another iteration, I would:
  - Implement more advanced conflict detection using time ranges
  - Improve the UI with better input validation and visualization
  - Add persistence (saving data instead of using session state only)

---

**c. Key takeaway**

- The most important thing I learned is how to act as the “lead architect” when working with AI tools.

- AI can generate code quickly, but it is my responsibility to decide what to use, what to simplify, and how to maintain a clean and understandable design.

- I also learned that breaking work into phases and using AI strategically (for design, coding, and testing separately) makes development more efficient and organized.