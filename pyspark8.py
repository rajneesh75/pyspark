import random
import csv

random.seed(42)

cities = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Hyderabad"]

rows = 20000

with open("data_large.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["age", "income", "city", "bought"])

    for _ in range(rows):
        age = random.randint(18, 65)
        income = random.randint(25000, 150000)
        city = random.choice(cities)

        # Simple buying logic (to make data meaningful)
        bought = 1 if (income > 60000 and age > 25) else 0

        writer.writerow([age, income, city, bought])

print("Generated data_large.csv with", rows, "rows")