# Student Record Management System Using Binary Search

**Subject:** Design and Analysis of Algorithms (DAA)  
**Language:** Python 3  
**GUI:** Tkinter  
**Storage:** JSON file (`students.json`)

## Features
- Add student records
- Search a student by ID using Binary Search
- Update and delete selected records
- Display all records in a table
- Automatically keep records sorted by Student ID
- Save records between runs in `students.json`

## Requirements
- Python 3.9 or later
- Tkinter (normally included with standard Python installations)

No third-party package is required.

## How to run
1. Extract the ZIP file.
2. Open the `Student_Record_Management_Binary_Search` folder in VS Code, PyCharm, or another Python editor.
3. Run `main.py`:
   ```bash
   python main.py
   ```
4. Add a few students, then search using a Student ID.

## How Binary Search is used
The list is sorted by Student ID. The `binary_search()` function checks the middle record:
- If the ID matches, it returns that record's index.
- If the target ID is greater, it searches the right half.
- If the target ID is smaller, it searches the left half.
- If no match is found, it returns `-1`.

## Complexity
For `n` student records:
- Best-case time: O(1)
- Average-case time: O(log n)
- Worst-case time: O(log n)
- Auxiliary space of the iterative search: O(1)

Note: Adding or updating a record may require sorting the records. The O(log n) search complexity applies to the Binary Search operation on an already sorted list.

## Project structure
```text
Student_Record_Management_Binary_Search/
    main.py
    README.md
    students.json
```
