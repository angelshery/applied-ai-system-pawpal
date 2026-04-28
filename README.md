# 🐾 PawPal AI: Explainable Pet Care Scheduler

## 🔹 Original Project (Module 2)

This project is based on my original **PawPal+** system from Module 2. The original version allowed users to create pets, assign care tasks, and generate a daily schedule based on task priority and available time. It also supported sorting, filtering, recurring tasks, and conflict detection.

---

## 🔹 Title and Summary

PawPal AI is an explainable AI system that helps pet owners plan daily care tasks efficiently. The system evaluates tasks using priority, type, duration, and time constraints, then generates an optimized schedule. It also explains why each task was selected, detects conflicts, and provides guardrails for invalid inputs.

This project demonstrates how AI-style reasoning can be applied to real-world planning problems in a transparent and reliable way.

---

## 🔹 Architecture Overview

The system follows a structured AI pipeline:

- **User Input** → Owner, pet, and task details  
- **Guardrail Validation** → checks for invalid inputs  
- **AI Scoring Engine** → assigns scores based on task importance  
- **Scheduler** → selects tasks within available time  
- **Conflict Checker** → detects overlapping tasks  
- **Explanation Generator** → explains decisions  
- **Decision Log** → records reasoning steps  

📌 See system diagram in:  
`assets/system_architecture.png`
---


## 🔹 Setup Instructions
```bash
# Clone repository
git clone https://github.com/angelshery/applied-ai-system-pawpal.git

# Navigate into folder
cd applied-ai-system-pawpal

# Install dependencies
pip install -r requirements.txt

# Run the app
python -m streamlit run app.py

```

## 🔹 Sample Interactions

### Example 1: AI Scheduling

**Input:**
- Morning Walk (priority 1)
- Grooming (priority 5)

**Output:**
- Morning Walk scheduled first  

**Explanation:**
- Morning Walk has higher priority and score  

---

### Example 2: Conflict Detection

**Input:**
- Walk at 08:00  
- Medication at 08:00  

**Output:**
- ⚠ Conflict detected at 08:00  

---

### Example 3: Guardrail Warning

**Input:**
- Task with invalid priority  

**Output:**
- ⚠ Warning: task skipped due to invalid input  

---

## 🔹 Design Decisions

- Used a scoring system instead of simple priority sorting to improve decision-making  
- Chose rule-based AI instead of machine learning for transparency and simplicity  
- Focused on readability over complex optimization algorithms  
- Conflict detection is based on start time instead of duration overlap to reduce complexity  

---

## 🔹 Testing Summary

- All core scheduling behaviors passed pytest tests  
- Conflict detection and filtering work correctly  
- Guardrails successfully prevent invalid inputs  
- The system consistently produces valid schedules  

---

## 🔹 Reliability and Evaluation

The system’s reliability was evaluated using automated pytest tests and runtime validation.

- All core tests passed successfully, including scheduling, sorting, filtering, and conflict detection  
- Guardrails handle invalid inputs such as incorrect priority and invalid time formats  
- Decision logs record how tasks are selected or skipped  

**Summary:**  
All tests passed, and the system consistently generated valid schedules. Reliability improved after adding validation and guardrails.

### Stretch Feature: Evaluation Harness

I added a test harness script that runs PawPal AI on predefined scenarios and prints pass/fail results. This helps evaluate whether the system handles normal scheduling, conflict detection, guardrails, and priority-based scheduling correctly.

Run it with:

```bash
python tests/evaluation_harness.py
```

---

## 🔹 Reflection

This project taught me how to design an applied AI system that goes beyond simple logic by incorporating reasoning, validation, and explainability. I learned how scoring logic improves decision-making compared to basic sorting, and how guardrails and testing improve system reliability.

It also helped me understand the importance of balancing simplicity and functionality when building systems for real-world use. Small design choices, such as using scoring instead of sorting, had a significant impact on how the system behaves.

### AI Collaboration

AI tools helped me design the scoring system and improve the structure of the Scheduler class. One helpful suggestion was introducing task scoring instead of simple sorting, which improved decision-making.

However, some AI suggestions were overly complex, such as adding advanced validation or redesigning the system completely. I simplified these ideas to keep the system readable and aligned with the project requirements.
---
## 🔹 Loom Video
https://www.loom.com/share/0451a7b8991c4c85bcbd9381d2bbb341