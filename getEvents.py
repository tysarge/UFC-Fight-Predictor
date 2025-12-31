from py_compile import main
import requests
from bs4 import BeautifulSoup
import csv

global fightids
fightids = {}

global fightid
fightid = 1

global fighterids
fighterids = {}

global fighterid
fighterid = 1

global currentDate
currentDate = ""


def getEvents(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.text, "html.parser")

        data = []

        allInfo = soup.find_all("tr")

        name = link = date = ""

        for soup in allInfo:
            url = soup.find("a")
            date = soup.find("span")
            if url is not None:
                name = url.get_text()
                link = url["href"]

            if date is not None:
                date = date.get_text()
                currentDate = date.strip()

            if name == "" and link == "" and date == None:
                continue
            my_dict = {
                "Event Name": str(name).strip(),
                "Link": str(link).strip(),
                "Date": str(date).strip(),
            }
            data.append(my_dict)
        data.pop(0)  # Remove future event
        return data

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []


def getFights(url):

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        date = soup.find("li", class_="b-list__box-list-item")
        date.i.extract()
        date = date.get_text().strip()
        fights = []
        allFights = soup.find("tbody").find_all("tr")

        weightClass = link = round = time = ""

        for soup in allFights:
            link = soup["data-link"]

            cols = soup.find_all("td")
            weightClass = cols[6]
            round = cols[8]
            time = cols[9]
            my_dict = {
                "Date": date,
                "Weight": weightClass.getText().strip(),
                "Link": str(link).strip(),
                "Round": round.getText().strip(),
                "Time": time.getText().strip(),
            }
            fights.append(my_dict)
        return fights

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []


def getFightStats(url, date):
    global fightid
    global fighterid
    global fighterids
    global fightids
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        start = soup.find("div", class_="b-fight-details__person")
        result = start.find("i").get_text().strip() == "W"

        tbody = soup.find("tbody")
        cols = tbody.find("tr").find_all("td")

        fighters = cols[0].find_all("a")
        name0 = fighters[0].get_text().strip()
        name1 = fighters[1].get_text().strip()
        link0 = fighters[0]["href"].strip()
        link1 = fighters[1]["href"].strip()

        kd = cols[1].find_all("p")
        kd0 = kd[0].get_text().strip()
        kd1 = kd[1].get_text().strip()

        sStrike = cols[2].find_all("p")
        sStrike0 = sStrike[0].get_text().strip()
        sStrike1 = sStrike[1].get_text().strip()

        sStrikeAcc = cols[3].find_all("p")
        sStrikeAcc0 = sStrikeAcc[0].get_text().strip()
        sStrikeAcc1 = sStrikeAcc[1].get_text().strip()

        totalStrikes = cols[4].find_all("p")
        totalStrikes0 = totalStrikes[0].get_text().strip()
        totalStrikes1 = totalStrikes[1].get_text().strip()

        td = cols[5].find_all("p")
        td0 = td[0].get_text().strip()
        td1 = td[1].get_text().strip()

        tdAcc = cols[6].find_all("p")
        tdAcc0 = tdAcc[0].get_text().strip()
        tdAcc1 = tdAcc[1].get_text().strip()

        subAtts = cols[7].find_all("p")
        subAtts0 = subAtts[0].get_text().strip()
        subAtts1 = subAtts[1].get_text().strip()

        revs = cols[8].find_all("p")
        revs0 = revs[0].get_text().strip()
        revs1 = revs[1].get_text().strip()

        crtlTime = cols[9].find_all("p")
        crtlTime0 = crtlTime[0].get_text().strip()
        crtlTime1 = crtlTime[1].get_text().strip()

        if link0 not in fighterids:
            fighterids[link0] = fighterid
            fighterid += 1
        if link1 not in fighterids:
            fighterids[link1] = fighterid
            fighterid += 1

        all_stats = {
            "fightid": fightid,
            "date": date,
            "fighter1id": fighterids[link0],
            "fighter2id": fighterids[link1],
            "winner": result,
            "Fighter 1 Name": name0,
            "Fighter 1 Link": link0,
            "Fighter 2 Name": name1,
            "Fighter 2 Link": link1,
            "KD 1": kd0,
            "KD 2": kd1,
            "Sig Strike 1": sStrike0,
            "Sig Strike 2": sStrike1,
            "Sig Strike Acc 1": sStrikeAcc0,
            "Sig Strike Acc 2": sStrikeAcc1,
            "Total Strikes 1": totalStrikes0,
            "Total Strikes 2": totalStrikes1,
            "TD 1": td0,
            "TD 2": td1,
            "TD Acc 1": tdAcc0,
            "TD Acc 2": tdAcc1,
            "Sub Atts 1": subAtts0,
            "Sub Atts 2": subAtts1,
            "Revs 1": revs0,
            "Revs 2": revs1,
            "Ctrl Time 1": crtlTime0,
            "Ctrl Time 2": crtlTime1,
        }

        fightid += 1

        return all_stats

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []


def main():
    url = "http://ufcstats.com/statistics/events/completed?page=all"
    eventData = getEvents(url)

    with open("events.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Event Name", "Link", "Date"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(eventData)

    fights = []
    i = 1
    for event in eventData:
        fights.extend(getFights(event["Link"]))
        print(i)
        i += 1

    with open("fights.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Date", "Weight", "Link", "Round", "Time"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(fights)

    with open("fights.csv", "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        fightLinks = []
        fightDates = []
        for row in reader:
            fightLinks.append(row["Link"])
            fightDates.append(row["Date"])

    allFightData = []
    i = 0
    for link in fightLinks:
        allFightData.append(getFightStats(link, fightDates[i]))
        print(f"Fighter Link:{i}")
        i += 1
        if i > 8000:
            break

    with open("allfightStats.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "fightid",
            "date",
            "fighter1id",
            "fighter2id",
            "winner",
            "Fighter 1 Name",
            "Fighter 1 Link",
            "Fighter 2 Name",
            "Fighter 2 Link",
            "KD 1",
            "KD 2",
            "Sig Strike 1",
            "Sig Strike 2",
            "Sig Strike Acc 1",
            "Sig Strike Acc 2",
            "Total Strikes 1",
            "Total Strikes 2",
            "TD 1",
            "TD 2",
            "TD Acc 1",
            "TD Acc 2",
            "Sub Atts 1",
            "Sub Atts 2",
            "Revs 1",
            "Revs 2",
            "Ctrl Time 1",
            "Ctrl Time 2",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(allFightData)

    with open("fighters.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["fighterid", "link"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for link, fid in fighterids.items():
            writer.writerow({"fighterid": fid, "link": link})


if __name__ == "__main__":
    main()
