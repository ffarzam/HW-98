--part 1
SELECT *
FROM film
WHERE release_year = 2006 and rental_rate >= 4;

--Part 2
SELECT *
FROM film
ORDER BY length ASC
LIMIT 10;