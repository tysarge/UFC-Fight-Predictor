import pandas as pd
import getFighterStats as fs
import csv

col_names = [
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

data = pd.read_csv("allfightStats.csv", names=col_names, header=0)

data_dict = data.to_dict('records')

idLink = pd.read_csv("fighters.csv", names=['fighterid', 'link'], header=0)
idLink_dict = idLink.set_index('fighterid')['link'].to_dict()
linkId_dict = idLink.set_index('link')['fighterid'].to_dict()

def previousfightData(fighter_id,date):
    prevFights = []
    currentDays = daysSince2000(date)

    staticInfo = fs.getFighterStats(idLink_dict[fighter_id])
    
    for row in data_dict:
        if daysSince2000(row['date']) < currentDays:
            if row['fighter1id'] == fighter_id:
                prevFights.append((row,True))
            elif row['fighter2id'] == fighter_id:
                prevFights.append((row,False))
        if len(prevFights) > 4:
            break
   
    size = len(prevFights)
    
    if size == 0:
        
        fighter_dict = {
            "kd": 0,
            "sig_strike": 40,
            "total_strikes": 59,
            "td": 1,
            "ctrl_time": 60
        }
    else:
        td_total = int(0)
        kd_total = int(0)
        sig_strike_total = int(0)
        total_strikes_total = int(0)
        ctrl_time_total = int(0)

        for fight in prevFights:
            
            if fight[1]:
                kd_total += int(fight[0]['KD 1'])
                sig_strike_total += int(fight[0]['Sig Strike 1'].split(' of ')[0])
                total_strikes_total += int(fight[0]['Total Strikes 1'].split(' of ')[0])
                td_total += int(fight[0]['TD 1'].split(' of ')[0])
                ctrl_time_total += convertTime(fight[0]['Ctrl Time 1'])
            else:
                kd_total += int(fight[0]['KD 2'])
                sig_strike_total += int(fight[0]['Sig Strike 2'].split(' of ')[0])
                total_strikes_total += int(fight[0]['Total Strikes 2'].split(' of ')[0])
                td_total += int(fight[0]['TD 2'].split(' of ')[0])
                ctrl_time_total += convertTime(fight[0]['Ctrl Time 2'])
        
        fighter_dict = {
            "kd": kd_total/size,
            "sig_strike": sig_strike_total/size,
            "total_strikes": total_strikes_total/size,
            "td": td_total/size,
            "ctrl_time": ctrl_time_total/size
        }
        
    return fighter_dict | staticInfo



def convertTime(ctrl_time_str):
    if ctrl_time_str == "N/A":
        return 0
    minutes, seconds = ctrl_time_str.split(':')
    minutes = int(minutes)
    seconds = int(seconds)
    return minutes * 60 + seconds
def daysSince2000(date_str):
    month_map = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12
    }

    month_str,day, year = date_str.replace(',', '').split(' ')
    month = month_map[month_str]
    day = int(day)
    year = int(year)

    days_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    total_days = 0

    for y in range(2000, year):
        total_days += 365
        if (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0):
            total_days += 1

    for m in range(1, month):
        total_days += days_in_months[m - 1]
        if m == 2 and ((year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)):
            total_days += 1

    total_days += day

    return total_days

def main(url1, url2, date):
    # i = 1
    # for fight in data_dict:
    #     f1_stats = previousfightData(fight['fighter1id'], fight['date'])
    #     f2_stats = previousfightData(fight['fighter2id'], fight['date'])
        
    #     stats_dif = {
    #         "kd_diff": f1_stats['kd'] - f2_stats['kd'],
    #         "sig_strike_diff": f1_stats['sig_strike'] - f2_stats['sig_strike'],
    #         "total_strikes_diff": f1_stats['total_strikes'] - f2_stats['total_strikes'],
    #         "td_diff": f1_stats['td'] - f2_stats['td'],
    #         "ctrl_time_diff": f1_stats['ctrl_time'] - f2_stats['ctrl_time'],
    #         "height_diff": f1_stats['Height'] - f2_stats['Height'],
    #         "weight_diff": int(f1_stats['Weight']) - int(f2_stats['Weight']),
    #         "reach_diff": int(f1_stats['Reach']) - int(f2_stats['Reach']),
    #         "age_diff": int(f1_stats['Age']) - int(f2_stats['Age']),
    #         "winrate_diff": f1_stats['Winrate'] - f2_stats['Winrate'],
    #     }
    #     print(i)
    #     i+=1
    #     if i > 10:
    #         break


    # with open('organizedFightStats.csv', "w", newline="", encoding="utf-8") as csvfile:
    #     fieldnames = [
    #         "kd_diff",
    #         "sig_strike_diff",
    #         "total_strikes_diff",
    #         "td_diff",
    #         "ctrl_time_diff",
    #         "height_diff",
    #         "weight_diff",
    #         "reach_diff",
    #         "age_diff",
    #         "winrate_diff",
    #         "winner"
    #     ]
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #     writer.writeheader()

    #   i = 1
        
        # for fight in data_dict:
        #     f1_stats = previousfightData(fight['fighter1id'], fight['date'])
        #     f2_stats = previousfightData(fight['fighter2id'], fight['date'])
            
        #     stats_dif = {
        #         "kd_diff": f1_stats['kd'] - f2_stats['kd'],
        #         "sig_strike_diff": f1_stats['sig_strike'] - f2_stats['sig_strike'],
        #         "total_strikes_diff": f1_stats['total_strikes'] - f2_stats['total_strikes'],
        #         "td_diff": f1_stats['td'] - f2_stats['td'],
        #         "ctrl_time_diff": f1_stats['ctrl_time'] - f2_stats['ctrl_time'],
        #         "height_diff": f1_stats['Height'] - f2_stats['Height'],
        #         "weight_diff": int(f1_stats['Weight']) - int(f2_stats['Weight']),
        #         "reach_diff": int(f1_stats['Reach']) - int(f2_stats['Reach']),
        #         "age_diff": int(f1_stats['Age']) - int(f2_stats['Age']),
        #         "winrate_diff": f1_stats['Winrate'] - f2_stats['Winrate'],
        #         "winner": 1 if fight['winner'] == True else 0
        #     }
            # writer.writerow(stats_dif)
            # print(f"Fight Processed:{i}/8001")
            # i+=1

    
    f1_stats = previousfightData(linkId_dict[url1], date)
    f2_stats = previousfightData(linkId_dict[url2], date)
    stats_dif = {
    "kd_diff": f1_stats['kd'] - f2_stats['kd'],
    "sig_strike_diff": f1_stats['sig_strike'] - f2_stats['sig_strike'],
    "total_strikes_diff": f1_stats['total_strikes'] - f2_stats['total_strikes'],
    "td_diff": f1_stats['td'] - f2_stats['td'],
    "ctrl_time_diff": f1_stats['ctrl_time'] - f2_stats['ctrl_time'],
    "height_diff": f1_stats['Height'] - f2_stats['Height'],
    "weight_diff": int(f1_stats['Weight']) - int(f2_stats['Weight']),
    "reach_diff": int(f1_stats['Reach']) - int(f2_stats['Reach']),
    "age_diff": int(f1_stats['Age']) - int(f2_stats['Age']),
    "winrate_diff": f1_stats['Winrate'] - f2_stats['Winrate'],
    }
    return stats_dif
        
