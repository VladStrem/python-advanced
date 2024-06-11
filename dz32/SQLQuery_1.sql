CREATE DATABASE Airportdb
GO

CREATE TABLE Flights (
	flight_id INT PRIMARY KEY,
	flight_number NVARCHAR(10),
	departure_time DATETIME,
	arrival_time DATETIME,
	origin NVARCHAR(50),
	destination NVARCHAR(50),
	airline NVARCHAR(50)
);
GO

INSERT INTO Flights (flight_id, flight_number, departure_time, arrival_time, origin, destination, airline)
VALUES
(1, 'UA101', '2024-06-12 08:00:00', '2024-06-12 11:00:00', 'Kyiv', 'London', 'Ukraine Airlines'),
(2, 'BA202', '2024-06-13 09:00:00', '2024-06-13 12:00:00', 'London', 'New York', 'British Airways'),
(3, 'AF303', '2024-06-14 10:00:00', '2024-06-14 14:00:00', 'Paris', 'Tokyo', 'Air France'),
(4, 'LH404', '2024-06-15 11:00:00', '2024-06-15 15:00:00', 'Berlin', 'Los Angeles', 'Lufthansa'),
(5, 'AA505', '2024-06-16 12:00:00', '2024-06-16 16:00:00', 'New York', 'Miami', 'American Airlines')
GO

CREATE TABLE Passengers (
    passenger_id INT PRIMARY KEY,
    first_name NVARCHAR(50) NOT NULL,
    last_name NVARCHAR(50) NOT NULL,
    passport_number NVARCHAR(20) NOT NULL,
    nationality NVARCHAR(50) NOT NULL
);
GO

INSERT INTO Passengers (passenger_id, first_name, last_name, passport_number, nationality)
VALUES
(1, 'John', 'Doe', 'AB123456', 'USA'),
(2, 'Jane', 'Smith', 'CD789012', 'UK'),
(3, 'Ivan', 'Petrenko', 'EF345678', 'Ukraine'),
(4, 'Anna', 'Muller', 'GH901234', 'Germany'),
(5, 'Yuki', 'Tanaka', 'IJ567890', 'Japan')
GO

CREATE TABLE Tickets (
    ticket_id INT PRIMARY KEY,
    flight_id INT NOT NULL,
    ticket_class NVARCHAR(20) NOT NULL,
    price MONEY NOT NULL,
    passenger_id INT,
    FOREIGN KEY (flight_id) REFERENCES Flights(flight_id),
    FOREIGN KEY (passenger_id) REFERENCES Passengers(passenger_id)
);
GO

INSERT INTO Tickets (ticket_id, flight_id, ticket_class, price, passenger_id)
VALUES
(1, 1, 'Economy', 200, 1),
(2, 1, 'Business', 500, 2),
(3, 2, 'Economy', 300, 3),
(4, 2, 'Business', 700, 4),
(5, 3, 'Economy', 400, 5),
(6, 3, 'Business', 900, 1);
GO

CREATE VIEW View_Flights_Duration AS
SELECT flight_id, flight_number, origin, destination,
    departure_time, arrival_time,
    DATEDIFF(HOUR, departure_time, arrival_time) AS duration_hours
FROM Flights

CREATE VIEW View_Today_Flights AS
SELECT *
FROM Flights
WHERE CONVERT(DATE, departure_time) = CONVERT(DATE, GETDATE())

CREATE TABLE Ticket_Log (
    log_id INT PRIMARY KEY IDENTITY(1, 1),
    ticket_id INT,
    flight_id INT,
    passenger_id INT,
    purchase_time DATETIME DEFAULT GETDATE()
);

CREATE TRIGGER trg_AfterInsertTicket
ON Tickets
AFTER INSERT
AS
BEGIN
    INSERT INTO Ticket_Log (ticket_id, flight_id, passenger_id)
    SELECT ticket_id, flight_id, passenger_id
    FROM inserted
END;
