import os
import smtplib
import datetime as dt
import random as rd
import pandas as pd

today = dt.datetime.today()
today_tuple = (today.month, today.day)

birthdays_data = pd.read_csv("birthdays.csv")

birthdays_dict = {(data_row["month"],data_row["day"]): data_row for (index, data_row) in birthdays_data.iterrows()}


my_email = "aaache20@gmail.com"
password = "ocdn irlf usvm body"

if today_tuple in birthdays_dict:
    name = birthdays_dict[today_tuple]['name']
    email = birthdays_dict[today_tuple]['email']

    random_letter = rd.choice(os.listdir("./letter_templates"))
    file_path = os.path.join('letter_templates', random_letter )

    with open(file_path) as birthday_file:
        birthday_message = birthday_file.read()
        birthday_message = birthday_message.replace("[NAME]", name)

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=email,
            msg= f"Subject: It's your Birthday!\n\n{birthday_message}")
