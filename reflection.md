# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML design included four main classes: Owner, Pet, Task, and Scheduler.

The Owner class stores user information such as name, available time, and preferences.

The Pet class stores pet details such as name, species, age, and breed.

The Task class represents pet care activities such as feeding, walking, medication, grooming, or enrichment. It includes important attributes like duration and priority.

The Scheduler class is responsible for generating a daily plan based on the owner's available time and the priority of tasks. It can also explain why certain tasks were selected for the plan.


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

During implementation, I made a few small changes based on feedback from Claude.

One change was simplifying the Task class. Claude initially suggested adding validation logic and strict task type checking, but I removed this to keep the design beginner-friendly and focused on the core requirements of the project.

I also improved the relationships between classes by ensuring that the Owner class properly stores pets using the add_pet() method, and that the Scheduler class keeps track of the current owner and pet when generating a plan. This will help later when explaining the scheduling decisions.

I did not apply all suggestions from the AI review, such as adding advanced validation or redesigning the system for multiple pets, because I wanted to keep the system simple and aligned with the project scope.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

My scheduler detects conflicts by checking whether two tasks share the exact same start time. For example, if Morning Walk and Medication are both scheduled at 08:00, the scheduler will flag it as a conflict.

The tradeoff is that this rule does not catch overlapping durations. For example, a 30-minute task starting at 08:00 and a 10-minute task starting at 08:15 would technically overlap, but my scheduler would not flag it because their start times are different.

This is a reasonable tradeoff for this project because the app is designed for a single owner managing a small number of daily pet tasks. Exact time conflicts are the most common and obvious problem to catch. Checking for full duration overlaps would require calculating end times and comparing time ranges, which adds complexity that is not needed at this stage.

If the app were expanded to handle many pets or precise scheduling (for example, a vet clinic), upgrading to duration-based conflict detection would be the right next step.

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
