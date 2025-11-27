CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    gender VARCHAR(10),
    city VARCHAR(50),
    join_date DATE,
    loyalty_tier VARCHAR(20)
);

INSERT INTO customers VALUES
(1,'John','Doe','john@example.com','9876543210','Male','New York','2023-01-10','Silver'),
(2,'Emma','Stone','emma@example.com','9123456780','Female','Chicago','2022-11-15','Gold'),
(3,'Robert','Williams','rob@example.com','9988776655','Male','Dallas','2023-03-05','Platinum'),
(4,'Sophia','Brown','sophia@example.com','9776655443','Female','Houston','2022-09-20','Silver'),
(5,'Ava','Taylor','ava@example.com','9554433221','Female','Boston','2023-02-14','Gold');

-- i want you to get all the customers who joined in the year 2023

SELECT *
FROM customers
WHERE extract(year from join_date) = 2023;

-- i want all the customers who join in past 6 months

INSERT INTO customers VALUES 
	(6,'Prajwala','Reddy','dpr@example.com','9554433221','Female','India','2025-8-14','Gold');

SELECT *
FROM customers
WHERE join_date >= CURRENT_DATE - INTERVAL '6 months';

-- i want all the customers who join in the last 30 days 

INSERT INTO customers VALUES 
	(7,'Manasa','Kolkuri','manasa@example.com','9554933229','Female','India','2025-11-11','Gold');

SELECT *
FROM customers
WHERE join_date >= CURRENT_DATE - INTERVAL '30 days';

-- i want the customer details along with the number of days since they joined

SELECT *,
CURRENT_DATE - join_date AS days_since_joining
FROM customers;





