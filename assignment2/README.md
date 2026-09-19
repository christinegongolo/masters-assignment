# Assignment 2 — Total 100 marks

Solutions to the 5 Python programming questions, one file per question.

| File | Question | Marks |
|---|---|---|
| `q1_get_post.py` | GET vs POST explanation + POST request using `requests` | 20 |
| `q2_sqlite.py` | SQLite connection steps: `connect()`, cursor, `commit()` | 20 |
| `q3_list_comprehension.py` | List comprehensions + odd numbers 1–50 divisible by 3 | 20 |
| `q4_chunked_file_reader.py` | Memory-efficient chunked file reader generator | 20 |
| `q5_car_electric_car.py` | `Car` / `ElectricCar` class hierarchy | 20 |

## Running

Each file is self-contained and can be run directly:

```bash
pip install requests   # only needed for q1
python3 q1_get_post.py
python3 q2_sqlite.py
python3 q3_list_comprehension.py
python3 q4_chunked_file_reader.py
python3 q5_car_electric_car.py
```

Q1 requires internet access (it calls a public test API,
`jsonplaceholder.typicode.com`). Q2 creates a local `students.db`
SQLite file when run. Q4 creates and deletes a temporary sample file
as part of its demo.
