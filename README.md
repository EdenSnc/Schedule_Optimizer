Student Schedule Optimizer
An automated, math-driven timetable generator built with Python and the PuLP Linear Programming library.

This project solves the classic student scheduling dilemma by taking a list of available course sessions (with their respective times, rooms, and notes) and calculating the absolute most efficient schedule based on custom lifestyle weights.

✨ Key Features
This script evaluates thousands of potential scheduling combinations to optimize for three main priorities:

📅 Day Minimization (The Ultimate Goal): Heavily penalizes adding extra days to the schedule. It will try to pack your classes into as few days as possible to give you full days off.

🛌 Sleep Prioritization: Not a morning person? The algorithm assigns steep penalties to 08:00 AM classes and gradually decreases the penalty throughout the day (15:30 classes have zero penalty).

🚫 Gap Reduction: Nobody likes waiting 3 hours for their next lecture. The model calculates the start and end of your day and minimizes the number of empty slots (gaps) in between.

📍 Metadata Tracking: Seamlessly carries over Room numbers and specific group notes (e.g., "ING4 DS") so your final output is ready to use.

🛠️ How It Works
The script treats scheduling as a mathematical optimization problem. It uses Binary Decision Variables to represent whether a specific session happens on a specific day and time.

The Objective Function Weighting
The "cost" of a schedule is calculated using these penalties:

+ 1,000,000,000,000,000 for every day you have to commute to campus.

+ 2,000 for an 08:00 AM class (decreasing down to 0 for afternoon classes).

+ 100 for every empty gap between your first and last class of the day.

The solver (PULP_CBC_CMD) finds the single valid configuration that results in the lowest possible score.

🚀 Getting Started
Prerequisites
You will need Python installed along with the pulp library.

Bash
pip install pulp
Usage
Open the script and modify the availability dictionary with your own modules, available timeslots, rooms, and notes.

Ensure your days and slots arrays match your university's scheduling format.

Run the script!

Bash
python schedule_optimizer.py
Example Output
The script will output an easy-to-read, chronological schedule grouped by day, clearly labeling any unavoidable gaps:

Plaintext
Status: Optimal

[Lun]:
  - 09:30: TD_MOD3D (Room: F)
  - 11:00: TD_ASMA (Room: 2104) | Note: SID
  - 12:30: TP_TIM (Room: A31) | Note: ING4 IA
[Mer]:
  - 14:00: TD_TALN (Room: C)
  - 15:30: [ GAP ]
  - 17:00: TD_GA (Room: 2220)
🧠 Technologies Used
Python 3

PuLP: An LP modeler written in Python to generate mathematical programs and solve them using solvers like CBC.
