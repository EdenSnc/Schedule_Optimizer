from pulp import *

# 1. Initialize the Problem
model = LpProblem("Schedule_With_Notes", LpMinimize)

# 2. Data Definition with Rooms and Notes
# Structure: (Day, Time, Room, Note)
availability ={
    "TP_MOD3D": [
        ("Dim", "14:00", "A33","")
    ],

    "TD_MOD3D": [
        ("Lun", "08:00", "1205",""),
        ("Lun", "09:30", "F",""),
        ("Jov", "09:30", "1205","")
    ],

    "TD_ASMA": [
        ("Lun", "09:30", "1207",""),
        ("Lun", "12:30", "1103",""),
        ("Dim", "08:00", "1219","RSID"),
        ("Lun", "11:00", "2104","SID")
    ],

    "TP_TIM": [
        ("Dim", "14:00", "A31",""),
        ("Lun", "09:30", "A43","ING4 DS"),
        ("Lun", "12:30", "A31","ING4 IA")
    ],

    "TD_GA": [
        ("Mar", "15:30", "2220","")
    ],

    "TD_TALN": [
        ("Mer", "14:00", "C",""),
        ("Mer", "15:30", "C","")
    ],

    "TP_TP": [
        ("Mer", "14:00", "A42",""),
        ("Jov", "11:00", "A41",""),
        ("Jov", "09:30", "A41","")
    ]
}


days = ["Dim", "Lun", "Mar", "Mer", "Jov", "Ven", "Sab"]
slots = ["08:00", "09:30", "11:00", "12:30", "14:00", "15:30"]

# Sleep Penalties
time_penalties = {"08:00": 2000, "09:30": 100, "11:00": 50, "12:30": 20, "14:00": 10, "15:30": 0}

# 3. Decision Variables
x = LpVariable.dicts("x", (availability.keys(), days, slots), cat='Binary')
y = LpVariable.dicts("y", days, cat='Binary')
z = LpVariable.dicts("z", (days, slots), cat='Binary')
has_started = LpVariable.dicts("has_started", (days, slots), cat='Binary')
has_ended = LpVariable.dicts("has_ended", (days, slots), cat='Binary')
is_gap = LpVariable.dicts("is_gap", (days, slots), cat='Binary')

# 4. Objective Function (Sleep > Gaps)
model += (
    lpSum([y[d] * 1000000000000000 for d in days]) + 
    lpSum([is_gap[d][t] * 100 for d in days for t in slots]) +
    lpSum([x[s][d][t] * time_penalties[t] for s in availability.keys() for d in days for t in slots])
)

# 5. Constraints
for session_name, options in availability.items():
    model += lpSum([x[session_name][d][t] for d in days for t in slots]) == 1
    
    # Updated stripping logic: valid_coords only takes first two elements (day, time)
    valid_coords = [(opt[0], opt[1]) for opt in options]
    for d in days:
        for t in slots:
            if (d, t) not in valid_coords:
                model += x[session_name][d][t] == 0

for d in days:
    for i, t in enumerate(slots):
        model += lpSum([x[s][d][t] for s in availability.keys()]) == z[d][t]
        model += z[d][t] <= y[d]
        model += has_started[d][t] >= z[d][t]
        if i > 0: model += has_started[d][t] >= has_started[d][slots[i-1]]
        model += has_ended[d][t] >= z[d][t]
        if i < len(slots) - 1: model += has_ended[d][t] >= has_ended[d][slots[i+1]]
        model += is_gap[d][t] >= has_started[d][t] + has_ended[d][t] + (1 - z[d][t]) - 2

# 6. Solve
model.solve(PULP_CBC_CMD(msg=0))

# 7. Optimized Result Output
# Dictionary to store (Room, Note) based on (Session, Day, Time)
metadata_lookup = {}
for session, opts in availability.items():
    for d, t, room, note in opts:
        metadata_lookup[(session, d, t)] = {"room": room, "note": note}

print(f"Status: {LpStatus[model.status]}\n")
for d in days:
    if value(y[d]) == 1:
        print(f"[{d}]:")
        for t in slots:
            session_found = False
            for s in availability.keys():
                if value(x[s][d][t]) == 1:
                    meta = metadata_lookup.get((s, d, t), {"room": "N/A", "note": ""})
                    note_str = f" | Note: {meta['note']}" if meta['note'] else ""
                    print(f"  - {t}: {s} (Room: {meta['room']}){note_str}")
                    session_found = True
            if not session_found and value(is_gap[d][t]) == 1:
                print(f"  - {t}: [ GAP ]")