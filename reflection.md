# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**
The PawPal+ application is designed to help pet owners organize their daily pet care activities. My initial design focused on three main actions:

Add Pet Information: Users can enter basic information about themselves and their pets, including the pet's name, breed, and age.
Manage Pet Care Tasks: Users can create care tasks such as feeding, walking, grooming, and giving medication, then mark them complete. The backend also supports updating task information, although the current UI does not have task-editing controls.
Generate a Daily Schedule: This was the original goal. The current version lets users enter task times and review a sorted list with filters and overlap warnings. Automatically choosing tasks based on priorities, available time, and owner preferences is not implemented.

The design uses four classes:

- Owner stores the owner's name, available time, preferences, and list of pets.
- Pet stores a pet's name, breed, age, and list of care tasks.
- Task describes a care activity, including its name, description, duration, priority, frequency, optional time and due date, and completion status. It provides methods to update the information and retrieve details.
- Scheduler connects to an Owner and retrieves tasks from all of that owner's pets. It sorts and filters those tasks and reports overlaps. Its automatic schedule-generation method is still unimplemented.

Task durations and available time use minutes. Priorities are high, medium, or low, and provided clock times must use valid, zero-padded HH:MM values. The design keeps task management in the backend and uses Streamlit to collect inputs and display the results.

**b. Design changes**

After reviewing the design, I added a pets list to Owner because the class had an add_pet() method but no collection to store the pets. This also made the Python skeleton match the Owner-to-Pet relationship in the UML. I added optional name, duration, priority, and frequency parameters to Task.update_task() to make it clear which information could be changed later. A parameter left as None means that field stays unchanged.

During implementation, I added optional time and due-date fields after the existing Task constructor arguments so earlier code would still work. Recurring completion belongs to Pet because Pet owns the task list and can add the next occurrence to the correct pet. Scheduler reads current tasks through Owner.get_all_tasks() instead of keeping an old snapshot. Streamlit stores that Owner in session state so normal reruns preserve the same pets and tasks. The final UML reflects these changes, while the draft remains available for comparison.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

I focused on valid clock times, duration, due dates, completion status, and keeping each task associated with the correct pet. Scheduler.sort_by_time() orders tasks by clock time, keeps equal times stable, and puts untimed tasks last without changing the stored lists. It sorts across due dates rather than building a dated calendar. The filters can select a pet name, a completion status, or both; a shared name includes all pets with that name.

Pet.complete_task() preserves the completed original and creates at most one incomplete successor. Daily tasks are due one day after completion and weekly tasks seven days after completion, using date and timedelta. Other frequencies do not create successors. Conflict detection compares each pair of incomplete tasks with dates, times, and positive durations. Overlapping intervals on the same date produce warnings, while back-to-back tasks are allowed. Tasks missing dates or times are unscheduled and are not checked.

Priorities, owner preferences, and available minutes are stored, but they are not used to automatically select or rearrange tasks. I kept that distinction clear because implementing those constraints would require automatic plan generation, which is not part of the working version.

**b. Tradeoffs**

My conflict checker compares incomplete tasks that have a clock time and share the same due date. This catches same-day overlaps, but it can miss an overnight overlap, such as a task starting at 23:50 for 30 minutes and another starting at 00:10 the next day. I kept the nested loops and this simpler same-date rule for the assignment because they are easier to read and explain, rather than adding cross-date time calculations.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI to help brainstorm the UML diagram and the four classes: Owner, Pet, Task, and Scheduler. AI helped generate the initial Python class skeletons from the design. During the review, it identified that Owner had an add_pet() method and an ownership relationship in the UML but no pets collection to store those pets.

AI also helped implement the backend methods, create the multi-pet demonstration in main.py, and write the initial two pytest tests and later algorithm tests. It helped connect Streamlit forms to the backend, preserve the Owner in session state, and display sorting, filters, recurring occurrences, and conflict warnings. Useful suggestions included adding the pets collection, combining tasks through Owner.get_all_tasks(), and keeping task lists separate for each pet.

Reviewing the actual constructors and method names with AI helped catch compatibility issues, such as the test requirement using mark_complete() when the existing method was named mark_completed(). We added a compatible wrapper instead of replacing the original method. Giving clear prompts that limited work to one assignment step kept the changes focused and helped avoid implementing later phases too early.

**b. Judgment and verification**

I checked the proposed changes against the assignment requirements and existing design before accepting them. For example, I accepted adding a pets collection to Owner because it matched the UML relationship and supported multiple pets. I deferred sorting, recurrence, and conflict detection until Phase 4, then implemented and verified them there. Automatic schedule generation remains unimplemented and its UI button is disabled.

I considered grouping tasks by date and using itertools.combinations() for conflict detection, but I rejected that change for this assignment. I kept the existing nested loops because they were easier to read and explain for a small set of pet care tasks. A shorter or more Pythonic implementation was not automatically the best choice for this project.

We verified the work with py_compile, the CLI demonstration, pytest, and Streamlit AppTest. I reviewed the displayed output and the test results rather than assuming generated code was correct. Working in separate phases helped keep each request limited to the current requirement and preserve the parts that already worked. Testing AI-generated code matters because correct-looking code can still use the wrong method, miss a pet's tasks, or create duplicate recurring occurrences.

---

## 4. Testing and Verification

**a. What you tested**

The automated suite passes 49 test cases. It checks task addition and completion, valid and invalid times, chronological sorting, stable ties, untimed tasks, and pet/status filters. It also checks daily and weekly recurrence, copied task details, correct pet ownership, month/year and leap-year rollover, and prevention of duplicate successors. Conflict tests cover exact matches, partial and fully contained overlaps, different pets, back-to-back tasks, completed tasks, unscheduled tasks, and duplicate warnings.

The added regression tests verify that changing a task's time updates the next sorted result without changing stored order and that a Scheduler sees a pet added after its creation. These tests matter because the application must use the current Owner data rather than a stale task list.

Syntax checks cover app.py, pawpal_system.py, and main.py. The CLI demonstrates both pets, sorting, filtering, daily and weekly successors, and an overlap warning. Streamlit AppTest checked pet/task entry, optional dates and times, sorting, filters, conflict warnings, recurring completion, same-name pets, and persistence across reruns without duplicate successors. The conflict-warning and daily-recurrence interactions were also manually verified in the browser during Phase 6.

**b. Confidence**

I would give the tested backend a confidence level of 4/5 stars. The main behaviors have automated coverage, and the important UI flows were checked with AppTest and in the browser. This does not mean every possible input or interaction has been tested.

The current checker does not detect overnight overlaps across different due dates. Tasks without dates or times are excluded from conflict checks, sorting uses clock time rather than date and time together, and automatic plan generation is not implemented. Session state also does not provide permanent storage. With more time, I would test the default completion-date branch using a controlled clock and check more browser interactions before extending the scheduler.

---

## 5. Lead Architect Reflection

**a. What went well**

I am most satisfied with keeping the classes, UI, tests, and final UML connected to the same design. As the lead architect, I reviewed AI suggestions, chose which implementations to retain, and checked the outputs against the CodePath requirements. The multi-pet task collection and the readable conflict checker are examples of decisions I understood and could explain, rather than accepting every generated change.

**b. What you would improve**

I would improve handling of overnight tasks and add permanent storage so pet care records could survive a new session. Automatic planning would need clearer rules for priorities, available time, and preferences before I added it. I would extend the tests alongside those changes instead of presenting unfinished functionality as working.

**c. Key takeaway**

I learned that using AI does not remove my responsibility for the design. I still need to check relationships, choose the right scope, and verify that the behavior matches the requirements. Keeping the work in separate phases made it easier to review changes, preserve working features, and use test results and actual output as evidence that each step was complete.
