-- (I) SELECT:

-- select some fields:
SELECT first_name, last_name FROM table_name;

-- select all fields:
SELECT * FROM table_name;

-- string concatenation with || operator:
SELECT first_name || ' ' || last_name AS full_name, email FROM table_name;

-- perform calculation:
SELECT 5 * 3 AS result;


-- (1.1) ORDER BY clause:

-- order ascending:
SELECT first_name, last_name FROM customer ORDER BY first_name ASC;
-- this finding result and order them ascending.

-- select descending:
SELECT first_name, last_name FROM customer ORDER BY last_name DESC;

-- order first_name first, then order last_name in descending order:
SELECT first_name, last_name FROM customer ORDER BY first_name ASC, last_name DESC;
-- NOTE: ORDER BY allows sort based on column specified in SELECT caluse only:

-- (1.2) SELECT DISTINCT:

SELECT DISTINCT first_name FROM customer ORDER BY first_name;

SELECT DISTINCT first_name, last_name FROM customer ORDER BY first_name;
-- if there are some rows that have 'first_name' and 'last_name' are the same:
-- it keeps only one rows and filter out the others

-- (II). WHERE:

-- WHERE comes after FROM statement:
--  operators: = > < >= <= <> != AND OR LIKE BETWEEN

-- e.g: select some fields based on a condition:
SELECT first_name, last_name FROM customer WHERE first_name = 'Minh';
-- in combination with AND operator:
SELECT first_name, last_name FROM customer WHERE first_name = 'Minh' AND last_name = 'Son';
-- in combination with OR:
SELECT first_name, last_name FROM customer WHERE first_name = 'Minh' OR last_name = 'Le';

-- with IN:
SELECT first_name, last_name FROM customer WHERE first_name IN ('Ann', 'Anne', 'Annie');

-- with "LIKE":
SELECT first_name FROM customer WHERE first_name LIKE 'A%';

-- with BETWEEN:
SELECT  
    first_name, 
    LENGTH(first_name) name_length 
FROM 
    customer 
WHERE 
    first_name LIKE 'A%' AND 
    LENGTH(first_name) BETWEEN 3 AND 5 
ORDER BY 
    name_length;

-- with not euqal <>, !=

SELECT first_name, LENGTH(first_name) AS name_length FROM customer WHERE LENGTH(first_name) < 5;

-- LIMIT:
SELECT film_id, title, release_year FROM film ORDER BY film_id LIMIT 5;

-- FETCH:
SELECT film_id, title FROM film ORDER BY title FETCH FIRST 5 ROW ONLY;
SELECT film_id, title FROM film ORDER BY title OFFSET 5 ROWS FETCH FIRST 5 ROW ONLY;

-- IN
SELECT customer_id, rental_id, return_date FROM rental WHERE customer_id IN (1, 2) ORDER BY return_date DESC;

-- other way:
SELECT customer_id, rental_id, return_date FROM rental WHERE customer_id = 1 OR customer_id = 2 ORDER BY return_data DESC;

-- INT with subquery:
SELECT customer_id FROM rental WHERE CAST (return_date AS DATE) = '2005-05-27';
-- return_date has format of '2005-06-07 12:34:35'. CAST takes the first block

SELECT first_name, last_name FROM customer WHERE customer_id IN (SELECT customer_id FROM rental WHERE CAST(return_date as DATE) = '2005-05-27');

-- BETWEEN

SELECT customer_id, payment_id, amount FROM payment WHERE amount BETWEEN 8 AND 9;
SELECT customer_id, payment_id FROM payment WHERE amount NOT BETWEEN 8 AND 9;
SELECT customer_id, payment_id from payment WHERE payment_date BETWEEN '2007-02-07' AND '2007-02-15';

-- LIKE
SELECT first_name, last_name FROM customer WHERE first_name LIKE 'Jen%';

-- ALIAS
SELECT first_name || ' ' || last_name AS full_name FROM customer ORDER BY full_name;

-- (III) - JOIN:

-- 3.1: inner join:
-- Example: we have two tables 'basket_a' and 'basket_b':
CREATE TABLE basket_a (
    id INT PRIMARY KEY,
    fruit VARCHAR (100) NOT NULL
);

CREATE TABLE basket_b (
    id INT PRIMARY KEY,
    fruit VARCHAR (100) NOT NULL
);

INSERT INTO basket_a (id, fruit)
VALUES 
    (1, 'Apple'),
    (2, 'Orange'),
    (3, 'Banana'),
    (4, 'Cucumber');

INSERT INTO basket_b (id, fruit)
VALUES 
    (1, 'Orange'),
    (2, 'Apple'),
    (3, 'Watermelon'),
    (4, 'Pear');

-- inner join basket_a and basket_b:
-- inner join finds the common between tables.
SELECT 
    a.id AS id_a,
    a.fruit AS fruit_a,
    b.id AS id_b,
    b.fruit AS fruit_b
FROM
    basket_a AS a
INNER JOIN basket_b AS b ON a.fruit = b.fruit;

-- left join(left outer join):
-- left join finds all fields in left table, then find in right tables fields that exists in left table.
SELECT 
    a.id AS id_a,
    a.fruit AS fruit_a,
    b.id AS id_b,
    b.fruit as fruit_b
FROM
    basket_a AS a
LEFT JOIN basket_b AS b ON a.fruit = b.fruit;

-- get values in left but not in right table:
SELECT
    a.id as id_a,
    a.fruit as fruit_a,
    b.id as id_b,
    b.fruit as fruit_b
FROM 
    basket_a as a
LEFT JOIN basket_b as b ON a.fruit = b.fruit
WHERE b.id IS NULL;

-- right join:
SELECT
    a.id as id_a,
    a.fruit as fruit_a,
    b.id as id_b,
    b.fruit as fruit_b
FROM basket_a as a
RIGHT JOIN basket_b AS b ON a.fruit = b.fruit;

-- full outer join:
-- this join find all the columns values in left table
-- then finds all values in right table, then display all
SELECT
    a.id AS id_a,
    a.fruit AS fruit_a,
    b.id AS id_b,
    b.fruit AS fruit_b
FROM basket_a AS a
FULL OUTER JOIN basket_b AS b ON a.fruit = b.fruit;

-- find unique values of each tables, use full outer join like following:
SELECT
    a.id as id_a,
    a.fruit as fruit_a,
    b.id as id_b,
    b.fruit as fruit_b
FROM basket_a as a
FULL OUTER JOIN basket_b as b ON a.fruit = b.fruit
WHERE a.id IS NULL OR b.id IS NULL;

-- inner join:
SELECT
    customer.customer_id,
    first_name,
    last_name,
    email,
    amount,
    payment_date
FROM
    customer
INNER JOIN payment ON payment.customer_id = customer.customer_id
ORDER BY customer.customer_id ASC
FETCH FIRST 5 ROW ONLY;
