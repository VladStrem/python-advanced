--#1
SELECT *
FROM Flights
WHERE destination = 'New York' AND CONVERT(DATE, departure_time) = '2024-06-13'
ORDER BY departure_time
--#2
SELECT *, DATEDIFF(MINUTE, departure_time, arrival_time) AS duration
FROM Flights
ORDER BY DATEDIFF(MINUTE, departure_time, arrival_time) DESC
--#3
SELECT *
FROM Flights
WHERE DATEDIFF(HOUR, departure_time, arrival_time) > 2
--#4
SELECT destination, COUNT(*) AS flight_count
FROM Flights
GROUP BY destination
--#5
SELECT TOP 1 destination, COUNT(*) AS flight_count
FROM Flights
GROUP BY destination
ORDER BY COUNT(*) DESC
--#6
SELECT destination, COUNT(*) AS flight_count
FROM Flights
WHERE MONTH(departure_time) = 6 AND YEAR(departure_time) = 2024
GROUP BY destination

SELECT COUNT(*) AS total_flights
FROM Flights
WHERE MONTH(departure_time) = 6 AND YEAR(departure_time) = 2024
--#7
SELECT f.*
FROM Flights f
JOIN Tickets t ON f.flight_id = t.flight_id
WHERE t.ticket_class = 'Business'
    AND t.passenger_id IS NULL
    AND CONVERT(DATE, f.departure_time) = CONVERT(DATE, GETDATE())
--#8
SELECT f.flight_id, COUNT(t.ticket_id) AS tickets_sold, SUM(t.price) AS total_revenue
FROM Flights f
JOIN Tickets t ON f.flight_id = t.flight_id
WHERE CONVERT(DATE, f.departure_time) = '2024-06-12'
GROUP BY f.flight_id
--#9
SELECT f.flight_id, f.flight_number, COUNT(t.ticket_id) AS ticket_sold
FROM Flights f
JOIN Tickets t ON f.flight_id = t.flight_id
WHERE CONVERT(DATE, f.departure_time) = '2024-06-12'
GROUP BY f.flight_id, f.flight_number
--#10
SELECT flight_number, destination
FROM Flights