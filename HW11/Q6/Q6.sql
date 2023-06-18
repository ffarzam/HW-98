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
FROM (SELECT customer.customer_id, customer.first_name, customer.last_name, country.country
      FROM customer
      INNER JOIN address on customer.address_id=address.address_id
      INNER JOIN city ON city.city_id=address.address_id
      INNER JOIN country ON country.country_id=city.country_id) AS customer_country
GROUP BY country
ORDER BY country ASC;

--part 4
SELECT title,rental_duration,avg(rental_rate) FROM film Group by title,rental_duration ORDER BY title;

--SELECT title,rental_duration, rental_rate FROM film ORDER BY title