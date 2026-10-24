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

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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
