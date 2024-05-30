USE ovochifryktudb
SELECT * FROM Products
SELECT * FROM Products
WHERE ProductType = 'Vegetable' AND CaloricContent < 50

SELECT * FROM Products
WHERE ProductType = 'Fruit' AND CaloricContent >= 50 AND CaloricContent <= 100

SELECT * FROM Products
WHERE ProductType = 'Vegetable' AND ProductName LIKE '%arr%'

SELECT * FROM Products
WHERE BriefDescription LIKE '%vitamins%'

SELECT * FROM Products
WHERE Color = 'Yellow' OR Color = 'Red'