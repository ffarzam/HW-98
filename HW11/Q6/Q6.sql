--part 1
SELECT *
FROM film
WHERE release_year = 2006 and rental_rate >= 4;

--Part 2
SELECT *
FROM film
ORDER BY length ASC
LIMIT 10;

--Part 3
SELECT country, COUNT(customer_id)
FROM customer
INNER JOIN address on customer.address_id=address.address_id
INNER JOIN city ON city.city_id=address.address_id
INNER JOIN country ON country.country_id=city.country_id
GROUP BY country
ORDER BY country ASC;

--part 4
SELECT title,rental_duration,avg(rental_rate) FROM film Group by title,rental_duration ORDER BY title;

--SELECT title,rental_duration, rental_rate FROM film ORDER BY title

--part 5
SELECT customer_id,COUNT(rental_id) AS count
FROM rental
GROUP BY customer_id
ORDER BY count DESC
LIMIT 10;

--part 6
SELECT customer.customer_id, customer.first_name, country.country
FROM customer
INNER JOIN address on customer.address_id=address.address_id
INNER JOIN city ON city.city_id=address.city_id
INNER JOIN country ON country.country_id=city.country_id
WHERE first_name LIKE 'A%' AND country = 'United States';

--part 7
SELECT *
FROM film
WHERE rental_duration > 5 AND replacement_cost < 15;