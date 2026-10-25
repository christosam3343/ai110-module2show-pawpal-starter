import streamlit as st

from pawpal_system import Owner, Pet, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Keep the owner and its pets and tasks available across Streamlit reruns.
if "owner" not in st.session_state:
    st.session_state["owner"] = Owner(name="Pet Owner", available_time=120)

owner = st.session_state["owner"]

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+. Add your pets and record their care tasks below.
Automatic daily scheduling will be added in a later phase.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You can now manage pets and their tasks here. Automatic planning will come later.
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
st.caption("Record daily care tasks for a pet. This does not calculate start times or a schedule.")

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
        else:
            selected_pet = owner.pets[pet_index]
            task = Task(name=task_title.strip(), duration=duration, priority=priority, frequency="daily")
            selected_pet.add_task(task)
            st.success(f"Added {task.name} for {selected_pet.name}.")

st.markdown("### Your pets and care tasks")
for pet in owner.pets:
    st.write(f"**{pet.name} ({pet.breed})** - Age: {pet.age} years")
    if pet.tasks:
        st.table(
            [
                {
                    "Task": task.name,
                    "Duration (minutes)": task.duration,
                    "Priority": task.priority,
                    "Status": "completed" if task.completed else "incomplete",
                }
                for task in pet.get_tasks()
            ]
        )
    else:
        st.info(f"No tasks yet for {pet.name}.")

st.divider()

st.subheader("Build Schedule")
st.caption("Automatic scheduling will be added in Phase 4. The lists above show recorded tasks only.")
st.button("Generate schedule", disabled=True)
