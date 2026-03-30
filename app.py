import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="User", available_time_minutes=60)

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
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

st.subheader("Quick Demo Inputs")

owner_name = st.text_input("Owner name", value=st.session_state.owner.name)
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
pet_age = st.number_input("Pet age", min_value=0, max_value=50, value=2)

# keep owner name updated
st.session_state.owner.name = owner_name

# STEP 3: Add pet using backend logic
if st.button("Add pet"):
    if pet_name.strip():
        new_pet = Pet(name=pet_name.strip(), species=species, age=int(pet_age))
        st.session_state.owner.add_pet(new_pet)
        st.success(f"{pet_name} added successfully.")
    else:
        st.error("Please enter a pet name.")

# show current pets
if st.session_state.owner.pets:
    st.write("Current pets:")
    pet_table = [
        {"name": pet.name, "species": pet.species, "age": pet.age}
        for pet in st.session_state.owner.pets
    ]
    st.table(pet_table)
else:
    st.info("No pets added yet.")

st.divider()

st.markdown("### Tasks")
st.caption("Add tasks to one of your pets.")

if st.session_state.owner.pets:
    selected_pet_name = st.selectbox(
        "Choose a pet",
        [pet.name for pet in st.session_state.owner.pets]
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    # STEP 4: Add task using backend logic
    if st.button("Add task"):
        selected_pet = next(
            pet for pet in st.session_state.owner.pets if pet.name == selected_pet_name
        )

        # This matches the Task class from Phase 2
        new_task = Task(
            description=task_title,
            time_minutes=int(duration),
            frequency="daily"
        )

        selected_pet.add_task(new_task)
        st.success(f"Task '{task_title}' added to {selected_pet_name}.")

    # show tasks from real objects
    current_tasks = []
    for pet in st.session_state.owner.pets:
        for task in pet.get_tasks():
            current_tasks.append(
                {
                    "pet": pet.name,
                    "task": task.description,
                    "duration_minutes": task.time_minutes,
                    "completed": task.completed,
                }
            )

    if current_tasks:
        st.write("Current tasks:")
        st.table(current_tasks)
    else:
        st.info("No tasks yet. Add one above.")
else:
    st.info("Add a pet first before adding tasks.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button now calls your scheduling logic.")

# STEP 5: Generate schedule using Scheduler
if st.button("Generate schedule"):
    scheduler = Scheduler(st.session_state.owner)
    plan = scheduler.generate_plan()

    if plan:
        st.success("Schedule generated successfully.")
        st.write("### Today's Schedule")

        schedule_table = []
        for item in plan:
            schedule_table.append(
                {
                    "pet": item["pet_name"],
                    "task": item["task"].description,
                    "duration_minutes": item["task"].time_minutes,
                }
            )

        st.table(schedule_table)
        st.write(scheduler.explain_plan())
        st.write(f"Remaining time: {scheduler.get_remaining_time()} minutes")
    else:
        st.warning("No tasks available to schedule yet.")