# Understanding Algorithms

- fun fact: `use the "-i" command when running python scripts to activate the interactive shell with all the code loaded from the script already.`
- ex: `python -i code.py`

## Definition and Characteristics
An algorithm is a set of sequential instructions executed to perform a specific task. Its key characteristics include:
- **Ordered Steps**: Crucial sequence of operations.
- **Clarity**: Unambiguous steps.
- **Finite Outcome**: Result in a finite time frame.
- **Termination**: Must not run indefinitely.

**Note**: Leverage established methods for common problems to optimize problem-solving.

## Comparing Algorithms

### Importance of Assessment
- Evaluate both the best and worst-case scenarios.
- Consider time and space complexities.
---
## Order of Growth and Big O Notation

### Overview
- Rates the increase in runtime or space as input size grows.
- Expressed using Big O notation.

### Common Time Complexities
- **O(1)**: Constant Time
- **O(log n)**: Logarithmic Time
- **O(n)**: Linear Time
- **O(n log n)**: Linearithmic Time
- **O(n^2)**: Quadratic Time
- **O(n^3)**: Cubic Time
- **O(2^n)**: Exponential Time
- **O(n!)**: Factorial Time

---
## Space Complexity

### Understanding Space Complexity
- Measures the memory required as the algorithm scales.

### Types of Space Complexity
- **Constant Space (O(1))**
- **Linear Space (O(n))**
- **Non-Linear Space (e.g., O(n^2))**

### Importance in Design
- Critical for systems with memory constraints.
- Balancing space with time complexity.
- Relevance in embedded systems, mobile apps, and large data.

---
## Search Algorithms
### Types of Searches

1. **Linear Search**
   - Iterates through each element.
   - For unsorted data.
   - Time Complexity: O(n)
   - Space Complexity: O(1)

2. **Binary Search**
   - Splits sorted data in half each iteration.
   - Time Complexity: O(log n)
   - Space Complexity: O(1) in iterative implementation, O(log n) in recursive implementation.

3. **Depth-First Search (DFS)**
   - Explores branches deeply before backtracking.
   - Time Complexity: O(V + E) for graphs, O(n) for trees (V = number of vertices, E = number of edges, n = number of nodes).
   - Space Complexity: O(V) for graphs, O(h) for trees (h = height of the tree).

4. **Breadth-First Search (BFS)**
   - Explores neighbors at each depth level.
   - Time Complexity: O(V + E) for graphs, O(n) for trees.
   - Space Complexity: O(V) for graphs, O(w) for trees (w = maximum width of the tree).


---

## Sort Algorithms
### Types of Sort Algos

1. **....**
   - ....




---


# DATA STRUCTURES

## Array
- **Fixed size and contiguous memory allocation.**
- **Fast read access (O(1)).**
- **Expensive resizing and element insertion/deletion (O(n)).**

## Linked List
- **Elements linked using pointers, allowing dynamic resizing.**
- **Efficient insertion/deletion (O(1) if node is known).**
- **Slower element access (O(n)).**

## Map (Dictionary)
- **Key-value pairs, optimized for fast retrieval.**
- **Hash tables (average O(1) access) or binary search trees (O(log n) access).**
- **Unique keys prevent duplicates.**
- **Hash tables require efficient hashing; trees need balancing.**




--- 
# Array Operations
- Insert: Index value injection (moves all subsequent items to the right)
- Append: Add to the end of the list
- Extend: Appending a new list to a previous one
- Delete: Shifts every element to the left with a removed index item 




