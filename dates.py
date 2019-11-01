"""
This file exists just to explain how the date system works, and how the program selects when the cards will be viewed.

The date starts with the installation of the database, using datetime.date.today().

The program picks up the first 20 elements of the list with a delta date of 0 or less,
and adds them to the current_cards list.

When the card is viewed:
A new level is assigned based on the chosen option. Minimum is 0
A new date is calculated based on the level and the current day. This future_date is inserted in the database.

When the app is opened:
The program chooses which cards to view based on the difference between future_date and datetime.date.today().
If the number is negative, the card gets added to the list.

"""

import datetime
x = datetime.date(2019, 10, 29)
y = datetime.date.today()
z = x - y
# print(z)
zero = datetime.date.today()-datetime.date.today()
# print(zero)

end_date = datetime.date.today() + datetime.timedelta(days=10)
print(end_date)


if z < zero:
    print("date negative")
else:
    print("date positive")

