# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**
The PawPal+ application is designed to help pet owners organize their daily pet care activities. The system will allow users to perform three main actions:

Add Pet Information: Users can enter basic information about themselves and their pets, including the pet's name, breed, and age.
Manage Pet Care Tasks: Users can create and edit tasks such as feeding, walking, grooming, and giving medication. Each task will include a duration and priority level.
Generate a Daily Schedule: Users can generate a daily schedule based on the available time and priority of each task. The application will organize tasks so that important activities are completed first while considering the owner's preferences.

The design uses four classes:

- Owner stores the owner's name, available time, preferences, and list of pets.
- Pet stores a pet's name, breed, age, and list of care tasks.
- Task describes a care activity, including its name, duration, priority, and frequency. It includes method stubs for updating its information and getting its details.
- Scheduler holds the tasks and available time. Its planned responsibility is to order tasks, check for conflicts, and generate a daily schedule.

Task durations and available time will use minutes. Task priorities will be high, medium, or low. These assumptions are documented, but validation and scheduling logic have not been implemented yet.

**b. Design changes**

After reviewing the design, I added a pets list to Owner because the class had an add_pet() method but no collection to store the pets. This also makes the Python skeleton match the Owner-to-Pet relationship in the UML. I added optional name, duration, priority, and frequency parameters to Task.update_task() to make it clear which information can be changed later. A parameter left as None will mean that field should stay unchanged. I updated the UML to match these changes and documented minutes and the three priority levels to keep the design consistent. The behavior methods remain empty stubs for a later phase.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

My conflict checker compares incomplete tasks that have a clock time and share the same due date. This catches same-day overlaps, but it can miss an overnight overlap, such as a task starting at 23:50 for 30 minutes and another starting at 00:10 the next day. I kept the nested loops and this simpler same-date rule for the assignment because they are easier to read and explain, rather than adding cross-date time calculations.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI to help brainstorm the UML diagram and the four classes: Owner, Pet, Task, and Scheduler. AI helped generate the initial Python class skeletons from the design. During the review, it identified that Owner had an add_pet() method and an ownership relationship in the UML but no pets collection to store those pets.

AI also helped implement the core class methods, create the multi-pet demonstration in main.py, and write the two pytest tests. Useful suggestions included adding the pets collection, combining tasks through Owner.get_all_tasks(), and keeping task lists separate for each pet. Giving clear prompts that limited the work to one assignment step helped keep the code simple and avoid implementing later phases too early.

**b. Judgment and verification**

I checked the proposed changes against the assignment requirements and existing design before accepting them. For example, I accepted adding a pets collection to Owner because it matched the UML relationship and supported multiple pets. I deferred advanced sorting, conflict detection, and recurring task logic until Phase 4. Those scheduling methods clearly raise NotImplementedError instead of claiming to generate a working schedule.

We checked Python syntax with py_compile, ran the CLI demo to confirm that both pets and all four tasks appeared, and ran pytest to verify task completion and task addition. Both tests passed. We also added mark_complete() to call the existing mark_completed() method when the test requirement used a different method name. Testing AI-generated code is important because code can look correct but still have missing methods or incorrect behavior. These checks support the features implemented so far; they do not verify the future scheduling algorithms.

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
