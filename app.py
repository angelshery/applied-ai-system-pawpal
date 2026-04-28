import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

# --- Emoji maps for labels ---
TYPE_EMOJI = {
    "feeding":     "🍖 feeding",
    "walking":     "🦮 walking",
    "medication":  "💊 medication",
    "grooming":    "✂️ grooming",
    "enrichment":  "🧸 enrichment",
}

PRIORITY_LABEL = {
    1: "⭐⭐⭐ High",
    2: "⭐⭐ Medium-High",
    3: "⭐ Medium",
    4: "Low",
    5: "Lowest",
}

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal AI")
st.caption("A smart daily pet care planner.")

with st.expander("About PawPal AI"):
    st.markdown(
        """
**PawPal AI** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

st.divider()

# Initialize a default Owner if one does not already exist
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_time=60, preferences=[])

# --- Owner ---
st.subheader("👤 Owner")
with st.form("owner_form"):
    owner_name = st.text_input("Owner name", value=st.session_state.owner.name)
    available_time = st.number_input("Available time (minutes)", min_value=1, max_value=480, value=st.session_state.owner.available_time)
    owner_submitted = st.form_submit_button("Set Owner")

if owner_submitted:
    pets = st.session_state.owner.pets
    st.session_state.owner = Owner(name=owner_name, available_time=available_time, preferences=[])
    st.session_state.owner.pets = pets
    st.success(f"Owner set to **{owner_name}** with **{available_time} min** available.")

st.divider()

# --- Pets ---
st.subheader("🐾 Add a Pet")
with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    breed = st.text_input("Breed", value="Unknown")
    age = st.number_input("Age", min_value=0, max_value=30, value=1)
    submitted = st.form_submit_button("Add Pet")

if submitted:
    new_pet = Pet(name=pet_name, species=species, age=age, breed=breed)
    st.session_state.owner.add_pet(new_pet)
    st.success(f"**{pet_name}** added to {st.session_state.owner.name}'s pets.")

if st.session_state.owner.pets:
    st.write("**Current pets:**")
    st.table([{
        "🐾 name": p.name,
        "species": p.species,
        "breed": p.breed,
        "age": p.age,
    } for p in st.session_state.owner.pets])

st.divider()

# --- Tasks ---
st.subheader("📋 Add a Task")
if not st.session_state.owner.pets:
    st.info("Add a pet first before adding tasks.")
else:
    with st.form("add_task_form"):
        pet_options = [p.name for p in st.session_state.owner.pets]
        selected_pet = st.selectbox("Assign to pet", pet_options)
        task_title = st.text_input("Task name", value="Morning Walk")
        task_type = st.selectbox("Task type", list(TYPE_EMOJI.keys()))
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        priority = st.number_input("Priority (1 = highest)", min_value=1, max_value=5, value=1)
        start_time = st.text_input("Start time (HH:MM)", value="08:00")
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
        task_submitted = st.form_submit_button("Add Task")

    if task_submitted:
        new_task = Task(
            name=task_title,
            type=task_type,
            duration=int(duration),
            priority=int(priority),
            start_time=start_time,
            frequency=frequency,
        )
        for pet in st.session_state.owner.pets:
            if pet.name == selected_pet:
                pet.add_task(new_task)
        st.success(f"Task **'{task_title}'** added to **{selected_pet}**.")

    all_tasks = st.session_state.owner.get_all_tasks()
    if all_tasks:
        st.write("**Current tasks:**")
        st.table([{
            "task": t.name,
            "type": TYPE_EMOJI.get(t.type, t.type),
            "duration (min)": t.duration,
            "priority": PRIORITY_LABEL.get(t.priority, str(t.priority)),
            "start time": t.start_time,
            "frequency": t.frequency,
        } for t in all_tasks])
    else:
        st.info("No tasks yet. Add one above.")

st.divider()

# --- Schedule ---
st.subheader("📅 Build Schedule")

if st.button("Generate schedule"):
    owner = st.session_state.owner
    if not owner.get_all_tasks():
        st.warning("Add at least one task before generating a schedule.")
    else:
        scheduler = Scheduler()
        scheduler.generate_plan(owner)
        sorted_tasks = scheduler.sort_by_time()

        st.success(f"Schedule generated for **{owner.name}**.")
        st.write("**Today's Schedule** (sorted by start time):")
        st.table([{
            "⏰ start": t.start_time,
            "task": t.name,
            "type": TYPE_EMOJI.get(t.type, t.type),
            "duration (min)": t.duration,
            "priority": PRIORITY_LABEL.get(t.priority, str(t.priority)),
        } for t in sorted_tasks])

        total = sum(t.duration for t in sorted_tasks)
        remaining = owner.get_available_time() - total
        st.caption(f"⏱ **{total} min** scheduled — **{remaining} min** remaining of {owner.get_available_time()} min available.")

        # Conflict warnings
        conflicts = scheduler.detect_conflicts()
        if conflicts:
            st.write("**⚠️ Conflicts detected:**")
            for warning in conflicts:
                st.warning(warning)
        else:
            st.success("✅ No scheduling conflicts detected.")

        # Guardrail warnings
        if scheduler.guardrail_warnings:
            st.write("**⚠️ Task validation warnings:**")
            for warning in scheduler.guardrail_warnings:
                st.warning(warning)

        # Explain plan
        st.write("**📋 Schedule Explanation:**")
        st.code(scheduler.explain_plan(), language="text")

        # Guardrail warnings
        if scheduler.guardrail_warnings:
            for warning in scheduler.guardrail_warnings:
                st.warning(warning)

        # AI Decision Log
        with st.expander("AI Decision Log"):
            for entry in scheduler.decision_log:
                st.write(entry)
