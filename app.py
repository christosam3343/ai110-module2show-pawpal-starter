import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Keep the owner and its pets and tasks available across Streamlit reruns.
if "owner" not in st.session_state:
    st.session_state["owner"] = Owner(name="Pet Owner", available_time=120)

owner = st.session_state["owner"]
scheduler = Scheduler(owner)


def task_rows(owner: Owner, tasks: list[Task]) -> list[dict]:
    """Build display rows from the owner's current pets and task objects."""
    rows = []
    for task in tasks:
        for pet_index, pet in enumerate(owner.pets):
            if any(task is pet_task for pet_task in pet.tasks):
                rows.append(
                    {
                        "Pet": f"{pet_index + 1}. {pet.name} ({pet.breed})",
                        "Task": task.name,
                        "Description": task.description,
                        "Due date": task.due_date.isoformat() if task.due_date else "Unscheduled",
                        "Time": task.time if task.time is not None else "Unscheduled",
                        "Duration (minutes)": task.duration,
                        "Priority": task.priority,
                        "Frequency": task.frequency,
                        "Status": "completed" if task.completed else "incomplete",
                    }
                )
    return rows


def completion_label(option: tuple[int, int]) -> str:
    """Identify the exact pet and task, including same-name pets or tasks."""
    pet_index, task_index = option
    pet = owner.pets[pet_index]
    task = pet.tasks[task_index]
    due = task.due_date.isoformat() if task.due_date else "No date"
    return (
        f"{pet_index + 1}. {pet.name} ({pet.breed}) / "
        f"{task_index + 1}. {task.name} / {due} {task.time or 'No time'}"
    )

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+. Add pets and care tasks, review them by time, and check for overlaps.
Completing a daily or weekly task creates its next occurrence.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You can manage pets, review tasks, and complete recurring care here.
Automatic plan generation is not implemented.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner and pets")
owner_name = st.text_input("Owner name", value=owner.name, key="owner_name")
if owner_name.strip():
    owner.name = owner_name.strip()
else:
    st.warning("Enter an owner name. Your saved owner name has not changed.")

with st.form("add_pet_form"):
    st.markdown("### Add a pet")
    pet_name = st.text_input("Pet name", key="pet_name")
    pet_breed = st.text_input("Breed", key="pet_breed")
    pet_age = st.number_input("Age (years)", min_value=0, value=0, step=1, key="pet_age")
    add_pet = st.form_submit_button("Add pet", key="add_pet")

if add_pet:
    if not pet_name.strip() or not pet_breed.strip():
        st.error("Enter a pet name and breed.")
    elif pet_age < 0:
        st.error("Pet age cannot be negative.")
    else:
        pet = Pet(name=pet_name.strip(), breed=pet_breed.strip(), age=int(pet_age))
        owner.add_pet(pet)
        st.success(f"Added {pet.name}.")

st.markdown("### Tasks")
st.caption("Record a task for a pet. Dates and times are optional, but both are needed for conflict checks.")

if not owner.pets:
    st.info("Add a pet before adding a task.")
else:
    with st.form("add_task_form"):
        # Use positions so pets with the same name can be selected separately.
        pet_index = st.selectbox(
            "Pet",
            options=list(range(len(owner.pets))),
            format_func=lambda index: f"{index + 1}. {owner.pets[index].name} ({owner.pets[index].breed})",
            key="task_pet_index",
        )
        col1, col2, col3 = st.columns(3)
        with col1:
            task_title = st.text_input("Task title", key="task_title")
        with col2:
            duration = st.number_input(
                "Duration (minutes)", min_value=1, max_value=240, value=20, key="task_duration"
            )
        with col3:
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=2, key="task_priority")
        description = st.text_input("Description (optional)", key="task_description")
        col1, col2, col3 = st.columns(3)
        with col1:
            due_date = st.date_input("Due date (optional)", value=None, key="task_due_date")
        with col2:
            clock_time = st.time_input("Start time (optional)", value=None, step=60, key="task_time")
        with col3:
            frequency = st.selectbox("Frequency", ["daily", "weekly", "once"], key="task_frequency")
        add_task = st.form_submit_button("Add task", key="add_task")

    if add_task:
        if not task_title.strip():
            st.error("Enter a task title.")
        elif duration <= 0:
            st.error("Task duration must be greater than zero minutes.")
        elif priority not in ("high", "medium", "low"):
            st.error("Choose a high, medium, or low priority.")
        elif pet_index not in range(len(owner.pets)):
            st.error("Select a pet for this task.")
        elif frequency not in ("daily", "weekly", "once"):
            st.error("Choose a daily, weekly, or once frequency.")
        else:
            selected_pet = owner.pets[pet_index]
            task = Task(
                name=task_title.strip(),
                duration=duration,
                priority=priority,
                frequency=frequency,
                description=description.strip(),
                time=clock_time.strftime("%H:%M") if clock_time is not None else None,
                due_date=due_date,
            )
            selected_pet.add_task(task)
            st.success(f"Added {task.name} for {selected_pet.name}.")

st.markdown("### Your pets")
for pet_index, pet in enumerate(owner.pets):
    st.write(f"**{pet_index + 1}. {pet.name} ({pet.breed})** - Age: {pet.age} years")
    if not pet.tasks:
        st.info(f"No tasks yet for {pet.name}.")

st.markdown("### Complete a task")
pending_options = []
for pet_index, pet in enumerate(owner.pets):
    for task_index, task in enumerate(pet.tasks):
        if not task.completed:
            pending_options.append((pet_index, task_index))

if pending_options:
    with st.form("complete_task_form"):
        completion_option = st.selectbox(
            "Task to complete", options=pending_options,
            format_func=completion_label, key="completion_task",
        )
        completion_date = st.date_input("Completion date", key="completion_date")
        complete_task = st.form_submit_button("Mark complete", key="complete_task_submit")
    if complete_task:
        if completion_date is None:
            st.error("Choose a completion date.")
        else:
            pet_index, task_index = completion_option
            selected_pet = owner.pets[pet_index]
            completed_task = selected_pet.tasks[task_index]
            next_task = selected_pet.complete_task(completed_task, completion_date=completion_date)
            st.success(f"Completed {completed_task.name} for {selected_pet.name}.")
            completion_result = [completed_task]
            if next_task is not None:
                st.success(f"Created the next incomplete occurrence, due {next_task.due_date.isoformat()}.")
                completion_result.append(next_task)
            st.table(task_rows(owner, completion_result))
else:
    st.info("There are no incomplete tasks to complete.")

st.markdown("### Care task overview")
pet_names = []
for pet in owner.pets:
    if pet.name not in pet_names:
        pet_names.append(pet.name)

col1, col2 = st.columns(2)
with col1:
    pet_filter = st.selectbox(
        "Pet name filter", options=[None] + pet_names,
        format_func=lambda name: "All pets" if name is None else name,
        key="pet_filter",
    )
with col2:
    status_values = {"All tasks": None, "Incomplete": False, "Completed": True}
    status_filter = st.selectbox("Status filter", list(status_values), key="status_filter")

st.caption("Pet filters match names exactly and include every pet with that name. Pet numbers identify individual pets.")
st.caption("Tasks are sorted by clock time across all dates; untimed tasks appear last. This does not build a daily plan.")

filtered_tasks = scheduler.filter_tasks(pet_name=pet_filter, completed=status_values[status_filter])
ordered_tasks = [
    task for task in scheduler.sort_by_time()
    if any(task is filtered_task for filtered_task in filtered_tasks)
]

st.caption("Conflict warnings check all pets' scheduled incomplete tasks, regardless of the filters above. Overnight overlaps are not detected.")
unscheduled_count = sum(
    1 for task in scheduler.get_tasks()
    if not task.completed and (task.due_date is None or task.time is None)
)
if unscheduled_count:
    st.info(f"{unscheduled_count} incomplete task(s) are missing a date or time and cannot be checked for time conflicts.")
warnings = scheduler.detect_conflicts()
for warning in warnings:
    st.warning(warning)
if not warnings:
    st.caption("No overlaps found among the scheduled incomplete tasks checked.")

if ordered_tasks:
    st.table(task_rows(owner, ordered_tasks))
else:
    if scheduler.get_tasks():
        st.info("No tasks match these filters.")
    else:
        st.info("No tasks yet. Add a pet and a care task above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Automatic plan generation is not implemented. Sorting and warnings do not move your tasks.")
st.button("Generate schedule", disabled=True, key="generate_schedule")
