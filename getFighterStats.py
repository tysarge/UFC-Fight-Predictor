from py_compile import main
import requests
from bs4 import BeautifulSoup
import csv
from datetime import date
currentYear = date.today().year


def getFighterStats(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        record = soup.find('span',class_='b-content__title-record').get_text().strip()
        
        win,loss,draw = record.split('-')

        win = win.split(' ')[1]

        winrate = float(win)/(float(win) + float(loss))



        table = soup.find('ul',class_='b-list__box-list')
        rows = table.find_all('li')

        rows[0].i.extract()
        height = rows[0].get_text().strip()
        if height == "-":
            height = 70
        else:
            height = convertHeight(height)
        
        rows[1].i.extract()
        weight = rows[1].get_text().strip()
        weight = weight.split(' ')[0]

        rows[2].i.extract()
        reach = rows[2].get_text().strip()
        if reach == "--":
            reach = 69
        else:
            reach = reach.replace('"','').strip()

        rows[4].i.extract()
        age = int(rows[4].get_text().strip().split(', ')[1])
        age = currentYear - age

        fighter_stats = {
            "Height": height,
            "Weight": weight,
            "Reach": reach,
            "Age": age,
            "Winrate": winrate
        }
        
        return fighter_stats

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []
    
def convertHeight(height_str):
    try:
        feet, inches = height_str.split("'")
        feet = int(feet.strip())
        inches = int(inches.replace('"', '').strip())
        total_inches = feet * 12 + inches
        return total_inches
    except ValueError:
        print("Invalid height format. Please use the format X'Y\" (e.g., 6'2\").")
        return None
    
