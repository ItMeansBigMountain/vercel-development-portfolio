export type Lesson = {
  id: string;
  title: string;
  module: string;
  description: string;
  starterCode: string;
  rubric: string[];
  prerequisites: string[];
  ageBand: string;
  exercise: string;
  teacherNotes: string;
  assessment: string[];
  project: string;
  progressFields: string[];
};

export const lessons: Lesson[] = [
  {
    "id": "teacher-t0",
    "title": "Platform and safety onboarding",
    "module": "Teacher Mastery Track",
    "description": "Teacher-only; not visible in learner module surfaces.",
    "starterCode": "",
    "rubric": [
      "Submit evidence",
      "Receive reviewer approval",
      "Write parent-safe reflection"
    ],
    "prerequisites": [],
    "ageBand": "adult teacher/coaches",
    "exercise": "teacher-only",
    "teacherNotes": "Teacher uses demo data safely with minors and writes parent-safe notes.",
    "assessment": [
      "teacher-observation",
      "reflection"
    ],
    "project": "Create a reusable coaching artifact for this level.",
    "progressFields": [
      "attempted",
      "completed",
      "teacher-reviewed",
      "mastered"
    ]
  },
  {
    "id": "teacher-t1",
    "title": "Basic 13 coaching mastery",
    "module": "Teacher Mastery Track",
    "description": "Teacher-only; not visible in learner module surfaces.",
    "starterCode": "",
    "rubric": [
      "Submit evidence",
      "Receive reviewer approval",
      "Write parent-safe reflection"
    ],
    "prerequisites": [
      "teacher-t0"
    ],
    "ageBand": "adult teacher/coaches",
    "exercise": "teacher-only",
    "teacherNotes": "Teacher explains loops, counters, arrays/lists, aggregation, mutation, edge tests, and index/value distinction.",
    "assessment": [
      "teacher-observation",
      "reflection"
    ],
    "project": "Create a reusable coaching artifact for this level.",
    "progressFields": [
      "attempted",
      "completed",
      "teacher-reviewed",
      "mastered"
    ]
  },
  {
    "id": "teacher-t2",
    "title": "Algorithm Academy coaching mastery",
    "module": "Teacher Mastery Track",
    "description": "Teacher-only; not visible in learner module surfaces.",
    "starterCode": "",
    "rubric": [
      "Submit evidence",
      "Receive reviewer approval",
      "Write parent-safe reflection"
    ],
    "prerequisites": [
      "teacher-t1"
    ],
    "ageBand": "adult teacher/coaches",
    "exercise": "teacher-only",
    "teacherNotes": "Teacher facilitates search/sort strategy lessons without turning them into memorization.",
    "assessment": [
      "teacher-observation",
      "reflection"
    ],
    "project": "Create a reusable coaching artifact for this level.",
    "progressFields": [
      "attempted",
      "completed",
      "teacher-reviewed",
      "mastered"
    ]
  },
  {
    "id": "teacher-t3",
    "title": "Debugging coaching mastery",
    "module": "Teacher Mastery Track",
    "description": "Teacher-only; not visible in learner module surfaces.",
    "starterCode": "",
    "rubric": [
      "Submit evidence",
      "Receive reviewer approval",
      "Write parent-safe reflection"
    ],
    "prerequisites": [
      "teacher-t2"
    ],
    "ageBand": "adult teacher/coaches",
    "exercise": "teacher-only",
    "teacherNotes": "Teacher coaches reproduce-read-isolate-change-rerun-reflect debugging.",
    "assessment": [
      "teacher-observation",
      "reflection"
    ],
    "project": "Create a reusable coaching artifact for this level.",
    "progressFields": [
      "attempted",
      "completed",
      "teacher-reviewed",
      "mastered"
    ]
  },
  {
    "id": "teacher-t4",
    "title": "Child-safe AI coding mastery",
    "module": "Teacher Mastery Track",
    "description": "Teacher-only; not visible in learner module surfaces.",
    "starterCode": "",
    "rubric": [
      "Submit evidence",
      "Receive reviewer approval",
      "Write parent-safe reflection"
    ],
    "prerequisites": [
      "teacher-t3"
    ],
    "ageBand": "adult teacher/coaches",
    "exercise": "teacher-only",
    "teacherNotes": "Teacher uses AI for hints, examples, and tests while protecting student thinking and private data.",
    "assessment": [
      "teacher-observation",
      "reflection"
    ],
    "project": "Create a reusable coaching artifact for this level.",
    "progressFields": [
      "attempted",
      "completed",
      "teacher-reviewed",
      "mastered"
    ]
  },
  {
    "id": "teacher-t5",
    "title": "Portfolio coaching mastery",
    "module": "Teacher Mastery Track",
    "description": "Teacher-only; not visible in learner module surfaces.",
    "starterCode": "",
    "rubric": [
      "Submit evidence",
      "Receive reviewer approval",
      "Write parent-safe reflection"
    ],
    "prerequisites": [
      "teacher-t4"
    ],
    "ageBand": "adult teacher/coaches",
    "exercise": "teacher-only",
    "teacherNotes": "Teacher helps students scope, ship, demo, and iterate on small runnable projects.",
    "assessment": [
      "teacher-observation",
      "reflection"
    ],
    "project": "Create a reusable coaching artifact for this level.",
    "progressFields": [
      "attempted",
      "completed",
      "teacher-reviewed",
      "mastered"
    ]
  },
  {
    "id": "student-basic-01",
    "title": "Print 1-255",
    "module": "Basic 13",
    "description": "Print every number from 1 through 255.",
    "starterCode": "// Print 1-255\nconst nums = [3, -1, 8, 4];\n// understand \u2192 inputs/outputs \u2192 hand examples \u2192 pseudocode \u2192 implement \u2192 edge tests \u2192 debug \u2192 improve \u2192 explain\n",
    "rubric": [
      "Understand",
      "Inputs/outputs",
      "Hand example",
      "Pseudocode",
      "Implement",
      "Edge tests",
      "Debug",
      "Improve",
      "Explain"
    ],
    "prerequisites": [],
    "ageBand": "10-14 JavaScript Core",
    "exercise": "Understand the goal, name inputs/outputs, do a hand example, write pseudocode, implement, test edges, debug, improve, and explain.",
    "teacherNotes": "Use hints before answers; teacher solution/debugging notes remain private and separate from learner surfaces.",
    "assessment": [
      "worksheet-response",
      "runnable-code",
      "edge-test",
      "bug-fix",
      "reflection"
    ],
    "project": "Turn this into a tiny number-list helper for a game score, classroom tally, or treasure inventory.",
    "progressFields": [
      "attempted",
      "completed",
      "teacher-reviewed",
      "mastered"
    ]
  },
  {
    "id": "student-basic-02",
    "title": "Odd numbers",
    "module": "Basic 13",
    "description": "Print only the odd numbers from 1 through 255.",
    "starterCode": "// Odd numbers\nconst nums = [3, -1, 8, 4];\n// understand \u2192 inputs/outputs \u2192 hand examples \u2192 pseudocode \u2192 implement \u2192 edge tests \u2192 debug \u2192 improve \u2192 explain\n",
    "rubric": [
      "Understand",
      "Inputs/outputs",
      "Hand example",
      "Pseudocode",
      "Implement",
      "Edge tests",
      "Debug",
      "Improve",
      "Explain"
    ],
    "prerequisites": [
      "student-basic-01"
    ],
    "ageBand": "10-14 JavaScript Core",
    "exercise": "Understand the goal, name inputs/outputs, do a hand example, write pseudocode, implement, test edges, debug, improve, and explain.",
    "teacherNotes": "Use hints before answers; teacher solution/debugging notes remain private and separate from learner surfaces.",
    "assessment": [
      "worksheet-response",
      "runnable-code",
      "edge-test",
      "bug-fix",
      "reflection"
    ],
    "project": "Turn this into a tiny number-list helper for a game score, classroom tally, or treasure inventory.",
    "progressFields": [
      "attempted",
      "completed",
      "teacher-reviewed",
      "mastered"
    ]
  },
  {
    "id": "student-basic-03",
    "title": "Running sum",
    "module": "Basic 13",
    "description": "Add every number from 1 through 255 and report the running total.",
    "starterCode": "// Running sum\nconst nums = [3, -1, 8, 4];\n// understand \u2192 inputs/outputs \u2192 hand examples \u2192 pseudocode \u2192 implement \u2192 edge tests \u2192 debug \u2192 improve \u2192 explain\n",
    "rubric": [
      "Understand",
      "Inputs/outputs",
      "Hand example",
      "Pseudocode",
      "Implement",
      "Edge tests",
      "Debug",
      "Improve",
      "Explain"
    ],
    "prerequisites": [
      "student-basic-02"
    ],
    "ageBand": "10-14 JavaScript Core",
    "exercise": "Understand the goal, name inputs/outputs, do a hand example, write pseudocode, implement, test edges, debug, improve, and explain.",
    "teacherNotes": "Use hints before answers; teacher solution/debugging notes remain private and separate from learner surfaces.",
    "assessment": [
      "worksheet-response",
      "runnable-code",
      "edge-test",
      "bug-fix",
      "reflection"
    ],
    "project": "Turn this into a tiny number-list helper for a game score, classroom tally, or treasure inventory.",
    "progressFields": [
      "attempted",
      "completed",
      "teacher-reviewed",
      "mastered"
    ]
  },
  {
    "id": "student-basic-04",
    "title": "Traverse array",
    "module": "Basic 13",
    "description": "Visit each array/list item and print the value.",
    "starterCode": "// Traverse array\nconst nums = [3, -1, 8, 4];\n// understand \u2192 inputs/outputs \u2192 hand examples \u2192 pseudocode \u2192 implement \u2192 edge tests \u2192 debug \u2192 improve \u2192 explain\n",
    "rubric": [
      "Understand",
      "Inputs/outputs",
      "Hand example",
      "Pseudocode",
      "Implement",
      "Edge tests",
      "Debug",
      "Improve",
      "Explain"
    ],
    "prerequisites": [
      "student-basic-03"
    ],
    "ageBand": "10-14 JavaScript Core",
    "exercise": "Understand the goal, name inputs/outputs, do a hand example, write pseudocode, implement, test edges, debug, improve, and explain.",
    "teacherNotes": "Use hints before answers; teacher solution/debugging notes remain private and separate from learner surfaces.",
    "assessment": [
      "worksheet-response",
      "runnable-code",
      "edge-test",
      "bug-fix",
      "reflection"
    ],
    "project": "Turn this into a tiny number-list helper for a game score, classroom tally, or treasure inventory.",
    "progressFields": [
      "attempted",
      "completed",
      "teacher-reviewed",
      "mastered"
    ]
  },
  {
    "id": "student-basic-05",
    "title": "Max",
    "module": "Basic 13",
    "description": "Track the largest value seen in an array/list.",
    "starterCode": "// Max\nconst nums = [3, -1, 8, 4];\n// understand \u2192 inputs/outputs \u2192 hand examples \u2192 pseudocode \u2192 implement \u2192 edge tests \u2192 debug \u2192 improve \u2192 explain\n",
    "rubric": [
      "Understand",
      "Inputs/outputs",
      "Hand example",
      "Pseudocode",
      "Implement",
      "Edge tests",
      "Debug",
      "Improve",
      "Explain"
    ],
    "prerequisites": [
      "student-basic-04"
    ],
    "ageBand": "10-14 JavaScript Core",
    "exercise": "Understand the goal, name inputs/outputs, do a hand example, write pseudocode, implement, test edges, debug, improve, and explain.",
    "teacherNotes": "Use hints before answers; teacher solution/debugging notes remain private and separate from learner surfaces.",
    "assessment": [
      "worksheet-response",
      "runnable-code",
      "edge-test",
      "bug-fix",
      "reflection"
    ],
    "project": "Turn this into a tiny number-list helper for a game score, classroom tally, or treasure inventory.",
    "progressFields": [
      "attempted",
      "completed",
      "teacher-reviewed",
      "mastered"
    ]
  },
  {
    "id": "student-basic-06",
    "title": "Average",
    "module": "Basic 13",
    "description": "Combine sum and count to find the average.",
    "starterCode": "// Average\nconst nums = [3, -1, 8, 4];\n// understand \u2192 inputs/outputs \u2192 hand examples \u2192 pseudocode \u2192 implement \u2192 edge tests \u2192 debug \u2192 improve \u2192 explain\n",
    "rubric": [
      "Understand",
      "Inputs/outputs",
      "Hand example",
      "Pseudocode",
      "Implement",
      "Edge tests",
      "Debug",
      "Improve",
      "Explain"
    ],
    "prerequisites": [
      "student-basic-05"
    ],
    "ageBand": "10-14 JavaScript Core",
    "exercise": "Understand the goal, name inputs/outputs, do a hand example, write pseudocode, implement, test edges, debug, improve, and explain.",
    "teacherNotes": "Use hints before answers; teacher solution/debugging notes remain private and separate from learner surfaces.",
    "assessment": [
      "worksheet-response",
      "runnable-code",
      "edge-test",
      "bug-fix",
      "reflection"
    ],
    "project": "Turn this into a tiny number-list helper for a game score, classroom tally, or treasure inventory.",
    "progressFields": [
      "attempted",
      "completed",
      "teacher-reviewed",
      "mastered"
    ]
  },
  {
    "id": "student-basic-07",
    "title": "Odd-number array",
    "module": "Basic 13",
    "description": "Build a new array/list containing only odd values.",
    "starterCode": "// Odd-number array\nconst nums = [3, -1, 8, 4];\n// understand \u2192 inputs/outputs \u2192 hand examples \u2192 pseudocode \u2192 implement \u2192 edge tests \u2192 debug \u2192 improve \u2192 explain\n",
    "rubric": [
      "Understand",
      "Inputs/outputs",
      "Hand example",
      "Pseudocode",
      "Implement",
      "Edge tests",
      "Debug",
      "Improve",
      "Explain"
    ],
    "prerequisites": [
      "student-basic-06"
    ],
    "ageBand": "10-14 JavaScript Core",
    "exercise": "Understand the goal, name inputs/outputs, do a hand example, write pseudocode, implement, test edges, debug, improve, and explain.",
    "teacherNotes": "Use hints before answers; teacher solution/debugging notes remain private and separate from learner surfaces.",
    "assessment": [
      "worksheet-response",
      "runnable-code",
      "edge-test",
      "bug-fix",
      "reflection"
    ],
    "project": "Turn this into a tiny number-list helper for a game score, classroom tally, or treasure inventory.",
    "progressFields": [
      "attempted",
      "completed",
      "teacher-reviewed",
      "mastered"
    ]
  },
  {
    "id": "student-basic-08",
    "title": "Count above Y",
    "module": "Basic 13",
    "description": "Count values greater than a chosen Y threshold.",
    "starterCode": "// Count above Y\nconst nums = [3, -1, 8, 4];\n// understand \u2192 inputs/outputs \u2192 hand examples \u2192 pseudocode \u2192 implement \u2192 edge tests \u2192 debug \u2192 improve \u2192 explain\n",
    "rubric": [
      "Understand",
      "Inputs/outputs",
      "Hand example",
      "Pseudocode",
      "Implement",
      "Edge tests",
      "Debug",
      "Improve",
      "Explain"
    ],
    "prerequisites": [
      "student-basic-07"
    ],
    "ageBand": "10-14 JavaScript Core",
    "exercise": "Understand the goal, name inputs/outputs, do a hand example, write pseudocode, implement, test edges, debug, improve, and explain.",
    "teacherNotes": "Use hints before answers; teacher solution/debugging notes remain private and separate from learner surfaces.",
    "assessment": [
      "worksheet-response",
      "runnable-code",
      "edge-test",
      "bug-fix",
      "reflection"
    ],
    "project": "Turn this into a tiny number-list helper for a game score, classroom tally, or treasure inventory.",
    "progressFields": [
      "attempted",
      "completed",
      "teacher-reviewed",
      "mastered"
    ]
  },
  {
    "id": "student-basic-09",
    "title": "Square values",
    "module": "Basic 13",
    "description": "Square each value and store the result.",
    "starterCode": "// Square values\nconst nums = [3, -1, 8, 4];\n// understand \u2192 inputs/outputs \u2192 hand examples \u2192 pseudocode \u2192 implement \u2192 edge tests \u2192 debug \u2192 improve \u2192 explain\n",
    "rubric": [
      "Understand",
      "Inputs/outputs",
      "Hand example",
      "Pseudocode",
      "Implement",
      "Edge tests",
      "Debug",
      "Improve",
      "Explain"
    ],
    "prerequisites": [
      "student-basic-08"
    ],
    "ageBand": "10-14 JavaScript Core",
    "exercise": "Understand the goal, name inputs/outputs, do a hand example, write pseudocode, implement, test edges, debug, improve, and explain.",
    "teacherNotes": "Use hints before answers; teacher solution/debugging notes remain private and separate from learner surfaces.",
    "assessment": [
      "worksheet-response",
      "runnable-code",
      "edge-test",
      "bug-fix",
      "reflection"
    ],
    "project": "Turn this into a tiny number-list helper for a game score, classroom tally, or treasure inventory.",
    "progressFields": [
      "attempted",
      "completed",
      "teacher-reviewed",
      "mastered"
    ]
  },
  {
    "id": "student-basic-10",
    "title": "Replace negatives",
    "module": "Basic 13",
    "description": "Replace negative values with a safe placeholder.",
    "starterCode": "// Replace negatives\nconst nums = [3, -1, 8, 4];\n// understand \u2192 inputs/outputs \u2192 hand examples \u2192 pseudocode \u2192 implement \u2192 edge tests \u2192 debug \u2192 improve \u2192 explain\n",
    "rubric": [
      "Understand",
      "Inputs/outputs",
      "Hand example",
      "Pseudocode",
      "Implement",
      "Edge tests",
      "Debug",
      "Improve",
      "Explain"
    ],
    "prerequisites": [
      "student-basic-09"
    ],
    "ageBand": "10-14 JavaScript Core",
    "exercise": "Understand the goal, name inputs/outputs, do a hand example, write pseudocode, implement, test edges, debug, improve, and explain.",
    "teacherNotes": "Use hints before answers; teacher solution/debugging notes remain private and separate from learner surfaces.",
    "assessment": [
      "worksheet-response",
      "runnable-code",
      "edge-test",
      "bug-fix",
      "reflection"
    ],
    "project": "Turn this into a tiny number-list helper for a game score, classroom tally, or treasure inventory.",
    "progressFields": [
      "attempted",
      "completed",
      "teacher-reviewed",
      "mastered"
    ]
  },
  {
    "id": "student-basic-11",
    "title": "Min/max/avg",
    "module": "Basic 13",
    "description": "Report the smallest, largest, and average values.",
    "starterCode": "// Min/max/avg\nconst nums = [3, -1, 8, 4];\n// understand \u2192 inputs/outputs \u2192 hand examples \u2192 pseudocode \u2192 implement \u2192 edge tests \u2192 debug \u2192 improve \u2192 explain\n",
    "rubric": [
      "Understand",
      "Inputs/outputs",
      "Hand example",
      "Pseudocode",
      "Implement",
      "Edge tests",
      "Debug",
      "Improve",
      "Explain"
    ],
    "prerequisites": [
      "student-basic-10"
    ],
    "ageBand": "10-14 JavaScript Core",
    "exercise": "Understand the goal, name inputs/outputs, do a hand example, write pseudocode, implement, test edges, debug, improve, and explain.",
    "teacherNotes": "Use hints before answers; teacher solution/debugging notes remain private and separate from learner surfaces.",
    "assessment": [
      "worksheet-response",
      "runnable-code",
      "edge-test",
      "bug-fix",
      "reflection"
    ],
    "project": "Turn this into a tiny number-list helper for a game score, classroom tally, or treasure inventory.",
    "progressFields": [
      "attempted",
      "completed",
      "teacher-reviewed",
      "mastered"
    ]
  },
  {
    "id": "student-basic-12",
    "title": "Shift values",
    "module": "Basic 13",
    "description": "Move values left and fill the final slot safely.",
    "starterCode": "// Shift values\nconst nums = [3, -1, 8, 4];\n// understand \u2192 inputs/outputs \u2192 hand examples \u2192 pseudocode \u2192 implement \u2192 edge tests \u2192 debug \u2192 improve \u2192 explain\n",
    "rubric": [
      "Understand",
      "Inputs/outputs",
      "Hand example",
      "Pseudocode",
      "Implement",
      "Edge tests",
      "Debug",
      "Improve",
      "Explain"
    ],
    "prerequisites": [
      "student-basic-11"
    ],
    "ageBand": "10-14 JavaScript Core",
    "exercise": "Understand the goal, name inputs/outputs, do a hand example, write pseudocode, implement, test edges, debug, improve, and explain.",
    "teacherNotes": "Use hints before answers; teacher solution/debugging notes remain private and separate from learner surfaces.",
    "assessment": [
      "worksheet-response",
      "runnable-code",
      "edge-test",
      "bug-fix",
      "reflection"
    ],
    "project": "Turn this into a tiny number-list helper for a game score, classroom tally, or treasure inventory.",
    "progressFields": [
      "attempted",
      "completed",
      "teacher-reviewed",
      "mastered"
    ]
  },
  {
    "id": "student-basic-13",
    "title": "Replace negatives with Dojo",
    "module": "Basic 13",
    "description": "Replace negative values with the string Dojo.",
    "starterCode": "// Replace negatives with Dojo\nconst nums = [3, -1, 8, 4];\n// understand \u2192 inputs/outputs \u2192 hand examples \u2192 pseudocode \u2192 implement \u2192 edge tests \u2192 debug \u2192 improve \u2192 explain\n",
    "rubric": [
      "Understand",
      "Inputs/outputs",
      "Hand example",
      "Pseudocode",
      "Implement",
      "Edge tests",
      "Debug",
      "Improve",
      "Explain"
    ],
    "prerequisites": [
      "student-basic-12"
    ],
    "ageBand": "10-14 JavaScript Core",
    "exercise": "Understand the goal, name inputs/outputs, do a hand example, write pseudocode, implement, test edges, debug, improve, and explain.",
    "teacherNotes": "Use hints before answers; teacher solution/debugging notes remain private and separate from learner surfaces.",
    "assessment": [
      "worksheet-response",
      "runnable-code",
      "edge-test",
      "bug-fix",
      "reflection"
    ],
    "project": "Turn this into a tiny number-list helper for a game score, classroom tally, or treasure inventory.",
    "progressFields": [
      "attempted",
      "completed",
      "teacher-reviewed",
      "mastered"
    ]
  },
  {
    "id": "student-js-objects-01",
    "title": "Object Detective",
    "module": "Data Objects and Arrays",
    "description": "Read an object and explain key/value pairs.",
    "starterCode": "const learner = { name: \"Demo Learner\", badges: [\"loop-builder\"] };\n// Read, change one field, and explain the shape.\n",
    "rubric": [
      "Identify keys and values",
      "Predict output",
      "Make one safe update",
      "Explain the data shape"
    ],
    "prerequisites": [
      "student-basic-13"
    ],
    "ageBand": "10-14 JavaScript Core",
    "exercise": "Inspect fixture data, predict output, make one safe change, and explain the data shape.",
    "teacherNotes": "Use fixture-only profiles; no real student information. Keep answer keys private.",
    "assessment": [
      "runnable-code",
      "worksheet-response",
      "reflection"
    ],
    "project": "Build a safe demo profile, inventory, or scoreboard card from fixture data.",
    "progressFields": [
      "attempted",
      "completed",
      "teacher-reviewed",
      "mastered"
    ]
  },
  {
    "id": "student-js-objects-02",
    "title": "Profile Card Builder",
    "module": "Data Objects and Arrays",
    "description": "Create and update a fixture-only profile object without private data.",
    "starterCode": "const learner = { name: \"Demo Learner\", badges: [\"loop-builder\"] };\n// Read, change one field, and explain the shape.\n",
    "rubric": [
      "Identify keys and values",
      "Predict output",
      "Make one safe update",
      "Explain the data shape"
    ],
    "prerequisites": [
      "student-js-objects-01"
    ],
    "ageBand": "10-14 JavaScript Core",
    "exercise": "Inspect fixture data, predict output, make one safe change, and explain the data shape.",
    "teacherNotes": "Use fixture-only profiles; no real student information. Keep answer keys private.",
    "assessment": [
      "runnable-code",
      "worksheet-response",
      "reflection"
    ],
    "project": "Build a safe demo profile, inventory, or scoreboard card from fixture data.",
    "progressFields": [
      "attempted",
      "completed",
      "teacher-reviewed",
      "mastered"
    ]
  },
  {
    "id": "student-js-arrays-01",
    "title": "Array Explorer",
    "module": "Data Objects and Arrays",
    "description": "Use arrays as ordered collections and practice map/filter/reduce thinking.",
    "starterCode": "const learner = { name: \"Demo Learner\", badges: [\"loop-builder\"] };\n// Read, change one field, and explain the shape.\n",
    "rubric": [
      "Identify keys and values",
      "Predict output",
      "Make one safe update",
      "Explain the data shape"
    ],
    "prerequisites": [
      "student-js-objects-02"
    ],
    "ageBand": "10-14 JavaScript Core",
    "exercise": "Inspect fixture data, predict output, make one safe change, and explain the data shape.",
    "teacherNotes": "Use fixture-only profiles; no real student information. Keep answer keys private.",
    "assessment": [
      "runnable-code",
      "worksheet-response",
      "reflection"
    ],
    "project": "Build a safe demo profile, inventory, or scoreboard card from fixture data.",
    "progressFields": [
      "attempted",
      "completed",
      "teacher-reviewed",
      "mastered"
    ]
  },
  {
    "id": "student-js-arrays-02",
    "title": "Inventory Organizer",
    "module": "Data Objects and Arrays",
    "description": "Add, remove, filter, and sort items in an array of objects.",
    "starterCode": "const learner = { name: \"Demo Learner\", badges: [\"loop-builder\"] };\n// Read, change one field, and explain the shape.\n",
    "rubric": [
      "Identify keys and values",
      "Predict output",
      "Make one safe update",
      "Explain the data shape"
    ],
    "prerequisites": [
      "student-js-arrays-01"
    ],
    "ageBand": "10-14 JavaScript Core",
    "exercise": "Inspect fixture data, predict output, make one safe change, and explain the data shape.",
    "teacherNotes": "Use fixture-only profiles; no real student information. Keep answer keys private.",
    "assessment": [
      "runnable-code",
      "worksheet-response",
      "reflection"
    ],
    "project": "Build a safe demo profile, inventory, or scoreboard card from fixture data.",
    "progressFields": [
      "attempted",
      "completed",
      "teacher-reviewed",
      "mastered"
    ]
  },
  {
    "id": "student-js-manipulation-01",
    "title": "Scoreboard Refactor",
    "module": "Data Objects and Arrays",
    "description": "Combine arrays and objects to update a small scoreboard.",
    "starterCode": "const learner = { name: \"Demo Learner\", badges: [\"loop-builder\"] };\n// Read, change one field, and explain the shape.\n",
    "rubric": [
      "Identify keys and values",
      "Predict output",
      "Make one safe update",
      "Explain the data shape"
    ],
    "prerequisites": [
      "student-js-arrays-02"
    ],
    "ageBand": "10-14 JavaScript Core",
    "exercise": "Inspect fixture data, predict output, make one safe change, and explain the data shape.",
    "teacherNotes": "Use fixture-only profiles; no real student information. Keep answer keys private.",
    "assessment": [
      "runnable-code",
      "worksheet-response",
      "reflection"
    ],
    "project": "Build a safe demo profile, inventory, or scoreboard card from fixture data.",
    "progressFields": [
      "attempted",
      "completed",
      "teacher-reviewed",
      "mastered"
    ]
  },
  {
    "id": "student-api-json-01",
    "title": "JSON Message Decoder",
    "module": "APIs, JSON, Fetch, and Errors",
    "description": "Parse JSON and identify shape, fields, and missing data.",
    "starterCode": "async function loadDemoData() {\n  const response = await fetch(\"https://example.com/demo.json\");\n  if (!response.ok) throw new Error(\"Could not load demo data\");\n  return response.json();\n}\n",
    "rubric": [
      "Read JSON shape",
      "Handle loading state",
      "Handle error state",
      "Explain fetch/result"
    ],
    "prerequisites": [
      "student-js-manipulation-01"
    ],
    "ageBand": "10-14 JavaScript Core",
    "exercise": "Read sample JSON, predict fields, fetch/load fixture data, handle one friendly error, and explain what happened.",
    "teacherNotes": "Use mock/public sample data first. No private data, tokens, addresses, or school details in API calls.",
    "assessment": [
      "runnable-code",
      "screenshot",
      "bug-fix",
      "reflection"
    ],
    "project": "Build a tiny safe data card with fixture or approved public API data and clear error messages.",
    "progressFields": [
      "attempted",
      "completed",
      "teacher-reviewed",
      "mastered"
    ]
  },
  {
    "id": "student-api-fetch-01",
    "title": "Fetch Weather Card",
    "module": "APIs, JSON, Fetch, and Errors",
    "description": "Trace fetch flow from request to response to rendered summary.",
    "starterCode": "async function loadDemoData() {\n  const response = await fetch(\"https://example.com/demo.json\");\n  if (!response.ok) throw new Error(\"Could not load demo data\");\n  return response.json();\n}\n",
    "rubric": [
      "Read JSON shape",
      "Handle loading state",
      "Handle error state",
      "Explain fetch/result"
    ],
    "prerequisites": [
      "student-api-json-01"
    ],
    "ageBand": "10-14 JavaScript Core",
    "exercise": "Read sample JSON, predict fields, fetch/load fixture data, handle one friendly error, and explain what happened.",
    "teacherNotes": "Use mock/public sample data first. No private data, tokens, addresses, or school details in API calls.",
    "assessment": [
      "runnable-code",
      "screenshot",
      "bug-fix",
      "reflection"
    ],
    "project": "Build a tiny safe data card with fixture or approved public API data and clear error messages.",
    "progressFields": [
      "attempted",
      "completed",
      "teacher-reviewed",
      "mastered"
    ]
  },
  {
    "id": "student-api-errors-01",
    "title": "Friendly Error Handler",
    "module": "APIs, JSON, Fetch, and Errors",
    "description": "Handle loading, empty, not-found, and network error states kindly.",
    "starterCode": "async function loadDemoData() {\n  const response = await fetch(\"https://example.com/demo.json\");\n  if (!response.ok) throw new Error(\"Could not load demo data\");\n  return response.json();\n}\n",
    "rubric": [
      "Read JSON shape",
      "Handle loading state",
      "Handle error state",
      "Explain fetch/result"
    ],
    "prerequisites": [
      "student-api-fetch-01"
    ],
    "ageBand": "10-14 JavaScript Core",
    "exercise": "Read sample JSON, predict fields, fetch/load fixture data, handle one friendly error, and explain what happened.",
    "teacherNotes": "Use mock/public sample data first. No private data, tokens, addresses, or school details in API calls.",
    "assessment": [
      "runnable-code",
      "screenshot",
      "bug-fix",
      "reflection"
    ],
    "project": "Build a tiny safe data card with fixture or approved public API data and clear error messages.",
    "progressFields": [
      "attempted",
      "completed",
      "teacher-reviewed",
      "mastered"
    ]
  },
  {
    "id": "student-linear-search",
    "title": "Linear Search Treasure Hunt",
    "module": "Algorithm Academy",
    "description": "Trace a target, return its index, and handle a missing value.",
    "starterCode": "function linearSearch(nums, target) {\n  for (let index = 0; index < nums.length; index += 1) {\n    const value = nums[index];\n    // Your condition here\n  }\n  return -1;\n}\n",
    "rubric": [
      "Trace target",
      "Return index",
      "Handle not found",
      "Explain index vs value"
    ],
    "prerequisites": [
      "student-basic-13"
    ],
    "ageBand": "10-14 JavaScript Core",
    "exercise": "Trace target values, complete the condition, test found/not-found cases, then explain index vs value.",
    "teacherNotes": "Use the worksheet treasure-hunt analogy and require a trace table before code. Teacher solution stays separate.",
    "assessment": [
      "trace-table",
      "runnable-code",
      "bug-fix",
      "reflection"
    ],
    "project": "Build a treasure-finder helper for a tiny game inventory.",
    "progressFields": [
      "attempted",
      "completed",
      "teacher-reviewed",
      "mastered"
    ]
  }
];

export const safeHints = [
  'Trace one loop iteration at a time and write down index and value.',
  'Try the smallest useful input before adding more cases.',
  'Explain what you expect first; then compare it with what happened.',
  'Ask for a hint, not an answer, and keep private information out of prompts.',
];
