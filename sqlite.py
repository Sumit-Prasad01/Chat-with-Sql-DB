import sqlite3

connection =  sqlite3.connect("student.db")
cursor = connection.cursor()

table_info = """
craete table STUDENT(NAME VARCHAR2(25),CLASS VARCHAR2(25),SECTION VARCHAR2(25),MARKS INT)      
"""
cursor.execute(table_info)

cursor.execute('''Insert Into STUDENT values('Krish','Data Science','A',90)''')
cursor.execute('''Insert Into STUDENT values('John','Data Science','B',100)''')
cursor.execute('''Insert Into STUDENT values('Mukesh','Data Science','A',86)''')
cursor.execute('''Insert Into STUDENT values('Jacob','DEVOPS','A',50)''')
cursor.execute('''Insert Into STUDENT values('Dipesh','DEVOPS','A',35)''')

students_data = [
    ('Ananya', 'Data Science', 'B', 78),
    ('Rohan', 'AI', 'A', 88),
    ('Meena', 'Cyber Security', 'C', 64),
    ('Suresh', 'AI', 'B', 72),
    ('Priya', 'Data Science', 'A', 93),
    ('Rahul', 'Cloud Computing', 'B', 81),
    ('Neha', 'DEVOPS', 'C', 59),
    ('Amit', 'Data Science', 'B', 76),
    ('Simran', 'AI', 'A', 91),
    ('Karan', 'Cyber Security', 'B', 70),
    ('Aisha', 'Cloud Computing', 'A', 89),
    ('Vikas', 'Data Science', 'C', 66),
    ('Sneha', 'DEVOPS', 'B', 74),
    ('Pankaj', 'AI', 'C', 61),
    ('Tina', 'Cyber Security', 'A', 90),
    ('Varun', 'Cloud Computing', 'B', 79),
    ('Divya', 'DEVOPS', 'C', 55),
    ('Arjun', 'Data Science', 'B', 80),
    ('Kriti', 'AI', 'A', 95),
    ('Suraj', 'Cyber Security', 'C', 60),
    ('Ishita', 'Cloud Computing', 'B', 83),
    ('Yash', 'DEVOPS', 'A', 87),
    ('Ritika', 'AI', 'B', 77),
    ('Nikhil', 'Data Science', 'A', 92),
    ('Aarav', 'Cloud Computing', 'C', 58),
    ('Sanya', 'Cyber Security', 'B', 69),
    ('Harsh', 'AI', 'C', 62),
    ('Mitali', 'DEVOPS', 'B', 75),
    ('Aditya', 'Data Science', 'A', 85),
    ('Komal', 'Cloud Computing', 'B', 84),
    ('Dhruv', 'Cyber Security', 'C', 57),
    ('Tanvi', 'AI', 'A', 94),
    ('Ravi', 'DEVOPS', 'B', 73),
    ('Preeti', 'Cloud Computing', 'C', 56),
    ('Gaurav', 'Cyber Security', 'B', 68),
    ('Bhavna', 'Data Science', 'A', 89),
    ('Manav', 'DEVOPS', 'C', 54),
    ('Rhea', 'AI', 'B', 79),
    ('Vivek', 'Cloud Computing', 'A', 90),
    ('Snehal', 'Data Science', 'C', 67),
    ('Nidhi', 'Cyber Security', 'A', 88),
    ('Laksh', 'AI', 'B', 71),
    ('Shreya', 'Cloud Computing', 'A', 91),
    ('Aryan', 'DEVOPS', 'C', 53),
    ('Naina', 'Cyber Security', 'B', 65),
    ('Ayan', 'Data Science', 'A', 96)
]

for student in students_data:
    cursor.execute("INSERT INTO STUDENT VALUES (?, ?, ?, ?)", student)

## Display all the records
print("The inserted records are")
data=cursor.execute('''Select * from STUDENT''')
for row in data:
    print(row)

## Commit your changes in the database
connection.commit()
connection.close()