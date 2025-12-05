create table employee (
    id int,
    name varchar(10),
    salary int,
    department varchar(20)
);

insert into employee (id, name, salary, department) values
(1, 'a', 10, 'IT'),
(2, 'b', 20, 'HR'),
(3, 'c', 30, 'Finance'),
(4, 'd', 40, 'IT'),
(5, 'e', 50, 'HR'),
(6, 'f', 60, 'Marketing');

--  give me the departments having employees more than HR department count 

select department from employee group by department
having count(department) > (select count(*) from employee where department='HR');

-- Find  Departments whose salary is more than 25

select distinct department from employee where salary>25;

-- give me all employees who are having highest salary in a company 

select * from employee where salary = (select max(salary) from employee);

-- employees who are having salary more than average salary of their department

select * from employee e1 where salary > (select avg(salary) from employee e2 where e1.department=e2.department);

-- employees who earn same salary as others

insert into employee values (7,'g',30,'Finance');
insert into employee values (8,'h',10,'Marketing');
select * from employee e1 where salary in (select salary from employee e2 where e1.id!=e2.id);

-- list of employees from departments with more than 2 employees

insert into employee values (9,'i',70,'IT');
select distinct department from employee e1 
where (select count(department) from employee e2 where e1.department=e2.department) > 2;

-- find the second highest salary from employee table

select salary from employee order by salary desc limit 1 offset 1;

-- find the departmetns where total slaary > total salary of HR department

select department from employee group by department having sum(salary)>(select sum(salary) from employee where department='HR');
