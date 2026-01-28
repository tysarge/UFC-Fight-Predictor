import requests
from bs4 import BeautifulSoup
import logreg as lr

fight_url = input("Enter fight url: ")



def getName(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    


def main():
    try:
        response = requests.get(fight_url)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.text, "html.parser")


        data = []

        date = soup.find('li',class_="b-list__box-list-item")
        date.i.extract()
        date = date.get_text().strip()

        fights = soup.find('tbody',class_="b-fight-details__table-body")
        
        fights = fights.find_all('tr')
        results = []
        for row in fights:
            list = row.find_all('a',limit=2)
            url1 = list[0]["href"].strip()
            url2 = list[1]["href"].strip()
            
            results.append(lr.predict_fight(url1,url2,date))
        
        for i in results:
            print(i)


       

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []

main()


