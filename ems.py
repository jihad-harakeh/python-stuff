#Employee Management System for a Mid-Sized Tech Company.

import sqlite3

conn=sqlite3.connect('ems.db')
cur=conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Employees;
DROP TABLE IF EXISTS Departments;
DROP TABLE IF EXISTS Performance_Reviews;
DROP TABLE IF EXISTS Salary_History
''')

cur.execute('''CREATE TABLE Employees(
            emp_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            salary INTEGER,
            dept_id INTEGER,
            FOREIGN KEY (dept_id) REFERENCES Departments(dept_id))
            ''')

cur.execute('''CREATE TABLE Departments(
            dept_id INTEGER PRIMARY KEY AUTOINCREMENT,
            dept_name TEXT NOT NULL)
            ''')

cur.execute('''CREATE TABLE Performance_Reviews(
            review_id INTEGER PRIMARY KEY AUTOINCREMENT,
            emp_id INTEGER,
            review_date Date DEFAULT (Date('now')),
            score INTEGER CHECK(1<=score<=10),
            comments,
            FOREIGN KEY (emp_id) REFERENCES Employees(emp_id))
            ''')

cur.execute('''CREATE TABLE Salary_History(
            history_id INTEGER PRIMARY KEY AUTOINCREMENT,
            emp_id INTEGER NOT NULL,
            old_salary INTEGER,
            new_salary INTEGER,
            change_date Date DEFAULT (Date('now')),
            reason TEXT)
            ''')
conn.commit()

cur.executemany('INSERT INTO Departments(dept_name) VALUES(?)',
[('Engineering',),('Human Resources',),('Marketing',),('Sales',),('Finance',),('Customer Support',),('Legal',),
('Operations',),('Management',),('Research and Development',),('Product',)])
cur.execute('SELECT * FROM Departments')

cur.executemany('INSERT INTO Employees(first_name,last_name,salary,dept_id) VALUES(?,?,?,?)',
[('Lama', 'Saliba',25000,1),('Sarah','Masri',25000,1),('Ali','Qassem',25000,1),('Nour','Farhat',22000,1),
('Mohammad','Yassine',22000,1),('Rami','Jawhari',20000,1),('Samer','Rizk',20000,1),('Zeina','Abdallah',20000,1),
('John','Kareh',16000,1),('Farah','Hariri',16000,1),('Ali','Fawaz',15000,1),('Sarah','Abou Farhat',18000,1),
('Rana','Khalaf',20000,4),('Mariam','Saad',18000,4),('Walid','Jaber',18000,4),('Lara','Rizk',18000,4),
('Hala','Dagher',17000,4),('Stephanie','Karam',17000,4),('Ahmad','Falha',17000,4),('Hassan','Hamieh',17000,4),
('George','Karam',13000,6),('Roula','Fakih',13000,6),('Lana','Khabbaz',12000,6),('Reem','Asmar',12000,6),
('Karim','Shamieh',18000,3),('Tony','Yammine',17500,3),('Nader','Farhat',17000,3),('Rama','Nasser',17000,3),
('Sara','Khatib',25500,11),('Tala','Haddad',25000,11),('Hadi','Chahine',24000,11),('Nagham','Jaber',20000,11),
('Mireille','Achkar',15000,2),('Marwa','Daher',13000,2),('Lamis','Dagher',13500,2),('Fouad','Rahme',20000,5),
('Ronald','Choubasi',19500,5),('Marwan','Nader',18000,5),('Michelle','Khoury',24000,7),('Ralph','Achkar',15000,8),
('Raghida','Farhat',54000,9),('Wared','Farhat',51000,9),('Elie','Khazen',18000,10)])

conn.commit()

reviews=[(1,8),(2,7),(3,9),(4,6),(5,8),(6,7),(7,5),(8,6),
(9,9),(10,4),(11,7),(12,8),(13,6),(14,7),(15,10), (16,8),(17,7),(18,6),(19,5),
(20,8),(21,10),(22,7),(23,5),(24,4),(25,9),(26,6),(27,7),(28,8),(29,9),(30,7),
(31,6),(32,5),(33,7),(34,8),(35,6),(36,9),(37,7),(38,6),(39,5),(40,8),(41,9),
(42,6),(43,10)]

cur.executemany('INSERT INTO Performance_Reviews(emp_id,score) VALUES(?,?)',reviews)
cur.execute('SELECT emp_id,salary FROM Employees')
info=[tup for tup in cur.fetchall()]
cur.executemany('INSERT INTO Salary_History(emp_id,old_salary) VALUES(?,?)',info)

conn.commit()

#all employees in the Engineering department
cur.execute('''SELECT emp_id,first_name,last_name,salary,dept_name FROM Employees JOIN Departments
ON Departments.dept_id=Employees.dept_id WHERE dept_name="Engineering"''')

#employees with a salary higher than 25,000
cur.execute('SELECT first_name,last_name,salary FROM Employees WHERE salary>25000')

#full name and department of each employee
cur.execute('''SELECT emp_id,first_name,last_name,salary,dept_name FROM Employees JOIN Departments
ON Departments.dept_id=Employees.dept_id''')

#employees whose first names start with ‘S’
cur.execute('SELECT emp_id,first_name,last_name FROM Employees WHERE first_name LIKE "S%"')

#all employees whose last name ends with “hat”
cur.execute('SELECT emp_id,first_name,last_name FROM Employees WHERE last_name LIKE "%hat"')

#all departments that have at least one employee with a salary below 15,000
cur.execute('''SELECT dept_name from Departments d
WHERE EXISTS (SELECT 1 from Employees e WHERE d.dept_id=e.dept_id and salary<15000)''')

#average salary per department
cur.execute('''SELECT dept_name, num FROM (SELECT dept_id,AVG(salary) AS NUM FROM Employees GROUP BY dept_id)
AS Newtable JOIN Departments ON Departments.dept_id=Newtable.dept_id''')

#department with the highest average performance score
cur.execute('''SELECT dept_name,MAX(av_sc)
FROM (SELECT ftb.dept_id,dept_name,AVG(SCORE) AS av_sc
FROM (SELECT Employees.dept_id,Employees.emp_id,score,dept_name
from Departments JOIN Employees ON Departments.dept_id=Employees.dept_id
JOIN Performance_Reviews on Employees.emp_id=Performance_Reviews.emp_id) as ftb
GROUP BY ftb.dept_id)''')

#how many employees each department has
cur.execute('''SELECT dept_name,total_emp FROM
(SELECT dept_id,COUNT(*) AS total_emp FROM Employees GROUP BY dept_id) AS ftb JOIN Departments ON
ftb.dept_id=Departments.dept_id ORDER BY total_emp DESC''')

cur.executescript('''UPDATE Employees SET salary=18000 WHERE first_name="Tony" AND last_name="Yammine";
UPDATE Employees SET salary=13500 WHERE first_name="Marwa" AND last_name="Daher";
UPDATE Employees SET salary=17500 WHERE first_name="John" AND last_name="Kareh"
''')
cur.executescript('''UPDATE Salary_History SET new_salary=18000 WHERE emp_id=26;
UPDATE Salary_History SET new_salary=13500 WHERE emp_id=34;
UPDATE Salary_History SET new_salary=17500 WHERE emp_id=9
''')
conn.commit()

#employees that got a raise
cur.execute('''SELECT * FROM Salary_History WHERE new_salary IS NOT NULL''')


#employees that have a performance review less than or equal 6
cur.execute('''SELECT Employees.emp_id, first_name,last_name,score,dept_name FROM
(SELECT emp_id,score FROM Performance_Reviews WHERE score<=6) AS Newtable JOIN Employees ON
Newtable.emp_id=Employees.emp_id JOIN Departments ON Departments.dept_id=Employees.dept_id order by dept_name''')

#departments with less than 2 employees
cur.execute('''SELECT dept_name,total_emp FROM
(SELECT dept_id,COUNT(*) AS total_emp FROM Employees GROUP BY dept_id) AS Newtable JOIN Departments
ON Newtable.dept_id=Departments.dept_id WHERE total_emp<2''')

#a view showing employee name, salary, and department name for those earning above the department average
cur.execute('DROP VIEW IF EXISTS salary_above_dept_avg')
cur.execute('''CREATE VIEW salary_above_dept_avg AS SELECT first_name,last_name,salary,dept_name FROM Employees JOIN
(SELECT dept_id,AVG(salary) AS avg_sal FROM Employees GROUP BY dept_id) AS Newtable
ON Newtable.dept_id=Employees.dept_id JOIN Departments ON Newtable.dept_id=Departments.dept_id WHERE salary>avg_sal''')
cur.execute('SELECT * FROM salary_above_dept_avg')

#an index on review_date and run a query using it
cur.execute('CREATE INDEX IF NOT EXISTS idx_review_date on Performance_Reviews(review_date)')
cur.execute('''SELECT * FROM Performance_Reviews WHERE review_date=Date("now")''')


#a transaction that gives all Sales employees a $1,000 raise. Roll back if any update fails
conn.execute('BEGIN')
try:
    cur.execute('UPDATE Employees SET salary=salary+1000 WHERE dept_id=4')
    sales_emp=list(cur.execute('SELECT * FROM Employees WHERE dept_id=4'))
    for tup in sales_emp:
        cur.execute('''SELECT new_salary FROM Salary_History sh1 WHERE emp_id=? AND
        change_date=(SELECT MAX(change_date) FROM Salary_History sh2 WHERE sh1.emp_id=sh2.emp_id)''',(tup[0],))
        old=cur.fetchone()
        if old is None:
            cur.execute('''SELECT old_salary FROM Salary_History sh1 WHERE emp_id=? AND
            change_date=(SELECT MAX(change_date) FROM Salary_History sh2 WHERE sh1.emp_id=sh2.emp_id)''',(tup[0],))
            old=cur.fetchone()
        cur.execute('INSERT INTO Salary_History(emp_id,old_salary,new_salary) VALUES(?,?,?)',(tup[0],old[0],tup[3]))
    conn.commit()
except:
    print('Transaction failed')
    conn.rollback()


#Update the salary of all employees who scored below 5 in their last performance review, reducing it by 10%
cur.execute('''UPDATE Employees SET salary=salary*0.9 WHERE emp_id IN
(SELECT emp_id FROM Performance_Reviews PR1 WHERE SCORE<5 AND review_date=
(SELECT MAX(review_date) FROM Performance_Reviews PR2 WHERE PR1.emp_id=PR2.emp_id))''')

conn.commit()

#For each employee, list their full name, department, and whether their salary is above or below the
#department average
cur.execute('''SELECT emp_id,first_name,last_name,dept_name,
               CASE
                   WHEN salary>num THEN "Above"
                   ELSE "Below"
               End AS salary_level
FROM Employees JOIN (SELECT Newtable.dept_id,dept_name, num FROM
(SELECT Employees.dept_id,AVG(salary) AS NUM FROM Employees GROUP BY dept_id)
AS Newtable JOIN Departments ON Departments.dept_id=Newtable.dept_id) AS NT ON Employees.dept_id=NT.dept_id''')

#Rank employees within their department by salary
cur.execute('''SELECT dept_id, emp_id, first_name, last_name, salary
FROM Employees ORDER BY dept_id ASC,salary DESC''')


#a summary report showing total number of employees, average salary, and total payroll per department
cur.execute('''SELECT dept_id, emp_num,avg_sal,tot_payroll FROM
(SELECT dept_id, COUNT(*) AS emp_num,AVG(salary) AS avg_sal,SUM(salary) AS tot_payroll FROM Employees GROUP BY dept_id)
AS Newtable''')
