"""Exercise library: 10 muscle groups x 10 exercises = 100 exercises.

Each entry: (name, equipment, sets_x_reps, tip)
IDs are generated automatically, e.g. "chest-1", "back-4".
"""

RAW = {
    "Chest": [
        ("Barbell Bench Press", "Barbell", "4 x 6-8", "Keep shoulder blades pinched and feet planted."),
        ("Incline Dumbbell Press", "Dumbbells", "3 x 8-10", "Set the bench at 30 degrees to hit the upper chest."),
        ("Push-Up", "Bodyweight", "3 x 15-20", "Keep your body in one straight line."),
        ("Dumbbell Fly", "Dumbbells", "3 x 10-12", "Slight bend in elbows; stretch, don't drop."),
        ("Cable Crossover", "Cable", "3 x 12-15", "Squeeze hands together at the bottom."),
        ("Decline Push-Up", "Bodyweight", "3 x 12-15", "Feet elevated to shift load to upper chest."),
        ("Chest Dip", "Parallel bars", "3 x 8-12", "Lean forward to bias the chest."),
        ("Machine Chest Press", "Machine", "3 x 10-12", "Adjust the seat so handles line up with mid-chest."),
        ("Pec Deck", "Machine", "3 x 12-15", "Control the stretch; do not let the weight slam."),
        ("Svend Press", "Weight plate", "3 x 12-15", "Press the plate together hard through the whole rep."),
    ],
    "Back": [
        ("Pull-Up", "Pull-up bar", "4 x 6-10", "Drive elbows down toward your hips."),
        ("Barbell Row", "Barbell", "4 x 6-8", "Hinge at the hips, keep your back flat."),
        ("Lat Pulldown", "Cable", "3 x 10-12", "Pull to the upper chest, not behind the neck."),
        ("Seated Cable Row", "Cable", "3 x 10-12", "Squeeze shoulder blades together at the end."),
        ("One-Arm Dumbbell Row", "Dumbbell", "3 x 10 each", "Pull the elbow back, not the hand."),
        ("Deadlift", "Barbell", "3 x 5", "Bar stays close to your legs the entire lift."),
        ("T-Bar Row", "T-bar", "3 x 8-10", "Chest up, drive elbows back."),
        ("Face Pull", "Cable", "3 x 15", "Great for rear delts and posture."),
        ("Inverted Row", "Bar / Smith machine", "3 x 10-15", "Body straight, pull chest to the bar."),
        ("Back Extension", "Hyper bench", "3 x 12-15", "Move with control; do not over-arch at the top."),
    ],
    "Shoulders": [
        ("Overhead Press", "Barbell", "4 x 6-8", "Squeeze glutes and brace your core."),
        ("Dumbbell Shoulder Press", "Dumbbells", "3 x 8-10", "Press slightly in front of your body."),
        ("Lateral Raise", "Dumbbells", "3 x 12-15", "Lead with the elbows, stop at shoulder height."),
        ("Front Raise", "Dumbbells", "3 x 12", "Light weight, no swinging."),
        ("Rear Delt Fly", "Dumbbells", "3 x 12-15", "Hinge forward and open the arms wide."),
        ("Arnold Press", "Dumbbells", "3 x 10", "Rotate palms from facing you to facing forward."),
        ("Upright Row", "Barbell / Cable", "3 x 10-12", "Pull to chest height only."),
        ("Pike Push-Up", "Bodyweight", "3 x 8-12", "Hips high, head moves between your hands."),
        ("Cable Lateral Raise", "Cable", "3 x 12-15", "Constant tension through the whole range."),
        ("Barbell Shrug", "Barbell", "3 x 12-15", "Straight up and down, no rolling."),
    ],
    "Biceps": [
        ("Barbell Curl", "Barbell", "3 x 8-10", "Keep elbows pinned to your sides."),
        ("Dumbbell Curl", "Dumbbells", "3 x 10-12", "Rotate the palm up as you curl."),
        ("Hammer Curl", "Dumbbells", "3 x 10-12", "Neutral grip also builds the forearm."),
        ("Incline Dumbbell Curl", "Dumbbells", "3 x 10-12", "Deep stretch at the bottom."),
        ("Preacher Curl", "EZ bar", "3 x 8-10", "Do not fully lock out at the bottom."),
        ("Concentration Curl", "Dumbbell", "3 x 10 each", "Elbow braced on the inner thigh."),
        ("Cable Curl", "Cable", "3 x 12-15", "Constant tension, slow negative."),
        ("Spider Curl", "EZ bar", "3 x 10-12", "Chest on an incline bench, arms hanging."),
        ("Chin-Up", "Pull-up bar", "3 x 6-10", "Underhand grip shifts focus to the biceps."),
        ("Zottman Curl", "Dumbbells", "3 x 10", "Curl up palms-up, lower palms-down."),
    ],
    "Triceps": [
        ("Close-Grip Bench Press", "Barbell", "4 x 6-8", "Hands shoulder-width, elbows tucked."),
        ("Triceps Pushdown", "Cable", "3 x 12-15", "Keep your upper arms still."),
        ("Overhead Triceps Extension", "Dumbbell", "3 x 10-12", "Elbows point forward, not flared."),
        ("Skull Crusher", "EZ bar", "3 x 8-10", "Lower to the forehead, press back up."),
        ("Bench Dip", "Bench", "3 x 12-15", "Keep your back close to the bench."),
        ("Diamond Push-Up", "Bodyweight", "3 x 10-15", "Hands form a diamond under your chest."),
        ("Rope Pushdown", "Cable", "3 x 12-15", "Spread the rope at the bottom."),
        ("Triceps Kickback", "Dumbbell", "3 x 12 each", "Upper arm parallel to the floor."),
        ("Parallel Bar Dip", "Dip bars", "3 x 8-12", "Stay upright to bias the triceps."),
        ("Single-Arm Cable Extension", "Cable", "3 x 12 each", "Slow, controlled lockout."),
    ],
    "Quads": [
        ("Barbell Back Squat", "Barbell", "4 x 6-8", "Knees track over toes, chest up."),
        ("Front Squat", "Barbell", "3 x 6-8", "Elbows high; very quad dominant."),
        ("Leg Press", "Machine", "3 x 10-12", "Feet shoulder width, do not lock knees."),
        ("Bulgarian Split Squat", "Dumbbells", "3 x 8-10 each", "Back foot on a bench, torso upright."),
        ("Walking Lunge", "Dumbbells", "3 x 12 each", "Long steps, knee kisses the floor lightly."),
        ("Leg Extension", "Machine", "3 x 12-15", "Pause for a second at the top."),
        ("Goblet Squat", "Dumbbell", "3 x 12", "Great for learning squat depth."),
        ("Hack Squat", "Machine", "3 x 8-10", "Feet low on the platform for more quad."),
        ("Step-Up", "Bench + dumbbells", "3 x 10 each", "Push through the heel of the top foot."),
        ("Sissy Squat", "Bodyweight", "3 x 10-12", "Lean back, keep hips forward."),
    ],
    "Hamstrings": [
        ("Romanian Deadlift", "Barbell", "4 x 8-10", "Push hips back, soft knees."),
        ("Lying Leg Curl", "Machine", "3 x 10-12", "Slow lowering phase."),
        ("Seated Leg Curl", "Machine", "3 x 10-12", "Hips pinned down, full contraction."),
        ("Stiff-Leg Deadlift", "Barbell", "3 x 8-10", "Feel the stretch behind your legs."),
        ("Good Morning", "Barbell", "3 x 10", "Light weight, flat back."),
        ("Nordic Curl", "Bodyweight", "3 x 5-8", "Lower as slowly as possible."),
        ("Single-Leg RDL", "Dumbbell", "3 x 8 each", "Square the hips to the floor."),
        ("Cable Pull-Through", "Cable", "3 x 12-15", "Hinge, then snap the hips forward."),
        ("Stability Ball Leg Curl", "Stability ball", "3 x 12", "Keep hips high throughout."),
        ("Dumbbell Sumo Deadlift", "Dumbbell", "3 x 10-12", "Wide stance, hips back."),
    ],
    "Glutes": [
        ("Barbell Hip Thrust", "Barbell", "4 x 8-10", "Chin tucked, squeeze hard at the top."),
        ("Glute Bridge", "Bodyweight", "3 x 15-20", "Drive through your heels."),
        ("Cable Kickback", "Cable", "3 x 12-15 each", "Do not arch your lower back."),
        ("Sumo Squat", "Dumbbell", "3 x 12", "Wide stance, toes out."),
        ("Reverse Lunge", "Dumbbells", "3 x 10 each", "Step back, lean slightly forward."),
        ("Banded Lateral Walk", "Resistance band", "3 x 15 steps", "Stay low, constant band tension."),
        ("Frog Pump", "Bodyweight", "3 x 20", "Soles together, knees wide."),
        ("Donkey Kick", "Bodyweight / band", "3 x 15 each", "Keep your hips square to the floor."),
        ("Single-Leg Hip Thrust", "Bench", "3 x 10 each", "Pause for a second at the top."),
        ("Curtsy Lunge", "Dumbbells", "3 x 10 each", "Cross behind and keep your front knee stable."),
    ],
    "Calves": [
        ("Standing Calf Raise", "Machine / Smith", "4 x 12-15", "Full stretch at the bottom, pause at the top."),
        ("Seated Calf Raise", "Machine", "3 x 15-20", "Targets the soleus muscle."),
        ("Donkey Calf Raise", "Machine / partner", "3 x 12-15", "Deep stretch, slow tempo."),
        ("Single-Leg Calf Raise", "Step", "3 x 12 each", "Hold on for balance only."),
        ("Leg Press Calf Raise", "Machine", "3 x 15", "Toes only on the platform."),
        ("Jump Rope", "Rope", "3 x 60 sec", "Stay light on the balls of your feet."),
        ("Box Jump", "Plyo box", "3 x 8", "Soft landing, step down."),
        ("Tibialis Raise", "Wall", "3 x 15-20", "Lean on the wall, lift your toes."),
        ("Farmer's Walk on Toes", "Dumbbells", "3 x 30 sec", "Stay tall on your toes."),
        ("Calf Raise Hold", "Bodyweight", "3 x 45 sec", "Hold the top position for time."),
    ],
    "Abs": [
        ("Plank", "Bodyweight", "3 x 45-60 sec", "Squeeze glutes, ribs down."),
        ("Hanging Leg Raise", "Pull-up bar", "3 x 10-12", "No swinging, curl your pelvis up."),
        ("Cable Crunch", "Cable", "3 x 12-15", "Round the spine, elbows toward knees."),
        ("Russian Twist", "Plate / bodyweight", "3 x 20", "Rotate your ribcage, not just your arms."),
        ("Bicycle Crunch", "Bodyweight", "3 x 20", "Slow and controlled."),
        ("Ab Wheel Rollout", "Ab wheel", "3 x 8-10", "Brace hard; stop before your back sags."),
        ("Dead Bug", "Bodyweight", "3 x 10 each", "Lower back stays glued to the floor."),
        ("Mountain Climber", "Bodyweight", "3 x 30 sec", "Hips low, drive knees quickly."),
        ("Side Plank", "Bodyweight", "3 x 30 sec each", "Stack your feet, lift your hips."),
        ("V-Up", "Bodyweight", "3 x 12-15", "Touch toes at the top of the movement."),
    ],
}

EXERCISES = []
for muscle, items in RAW.items():
    for i, (name, equipment, scheme, tip) in enumerate(items, start=1):
        EXERCISES.append({
            "id": f"{muscle.lower()}-{i}",
            "muscle": muscle,
            "name": name,
            "equipment": equipment,
            "scheme": scheme,
            "tip": tip,
        })

MUSCLES = list(RAW.keys())

# Default weekly plan (0 = Monday ... 6 = Sunday), using exercise IDs.
DEFAULT_PLAN = {
    "0": ["chest-1", "chest-2", "shoulders-3", "triceps-2", "triceps-4"],          # Push
    "1": ["back-1", "back-2", "back-4", "biceps-1", "biceps-3"],                    # Pull
    "2": ["quads-1", "hamstrings-1", "glutes-1", "calves-1", "abs-1"],              # Legs
    "3": ["shoulders-1", "chest-3", "shoulders-3", "triceps-1", "abs-3"],           # Push 2
    "4": ["back-3", "back-5", "back-8", "biceps-2", "biceps-5"],                    # Pull 2
    "5": ["quads-3", "glutes-2", "hamstrings-2", "calves-2", "abs-2"],              # Legs 2
    "6": [],                                                                         # Rest
}

DEFAULT_HABITS = [
    {"id": "h1", "name": "Drink 2L of water"},
    {"id": "h2", "name": "Sleep 7+ hours"},
    {"id": "h3", "name": "Eat enough protein"},
    {"id": "h4", "name": "10-minute stretch"},
    {"id": "h5", "name": "Read for 15 minutes"},
    {"id": "h6", "name": "No junk food"},
]
