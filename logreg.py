import pandas as pd
from sklearn.model_selection import train_test_split as tts
from sklearn.linear_model import LogisticRegression as lr
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
import organize

logreg = lr(random_state=42, max_iter=99)

col_names = [
    "kd_diff",
    "sig_strike_diff",
    "total_strikes_diff",
    "td_diff",
    "ctrl_time_diff",
    "height_diff",
    "weight_diff",
    "reach_diff",
    "age_diff",
    "winrate_diff",
    "winner",
]

data = pd.read_csv("organizedFightStats copy.csv", names=col_names, header=0)

features = [
    "kd_diff",
    "sig_strike_diff",
    "total_strikes_diff",
    "td_diff",
    "ctrl_time_diff",
    "height_diff",
    "weight_diff",
    "reach_diff",
    "age_diff",
    "winrate_diff",
]

independent = data[features]
dependent = data.winner

X_train, X_test, y_train, y_test = tts(
    independent, dependent, test_size=0.25, random_state=42
)


logreg.fit(X_train, y_train)

y_pred = logreg.predict(X_test)

cm = confusion_matrix(y_test, y_pred)

target_names = ["Lose", "Win"]
# print(classification_report(y_test, y_pred, target_names=target_names))


def predict_fight():
    url1 = input("Enter Fighter 1 URL: ").strip()
    url2 = input("Enter Fighter 2 URL: ").strip()
    date = input("Enter Fight Date (ex. May 4, 2026): ").strip()
    featureOrder = [
        "kd_diff",
        "sig_strike_diff",
        "total_strikes_diff",
        "td_diff",
        "ctrl_time_diff",
        "height_diff",
        "weight_diff",
        "reach_diff",
        "age_diff",
        "winrate_diff",
    ]

    stats = organize.main(url1, url2, date)

    array = np.array([float(stats[f]) for f in featureOrder]).reshape(1, -1)

    prediction = logreg.predict(array)
    print()
    if prediction[0] == 1:
        print("Expect Fighter 1 Win")
    else:
        print("Expect Fighter 2 Win")

def predict_fight(url1,url2,date):
    featureOrder = [
        "kd_diff",
        "sig_strike_diff",
        "total_strikes_diff",
        "td_diff",
        "ctrl_time_diff",
        "height_diff",
        "weight_diff",
        "reach_diff",
        "age_diff",
        "winrate_diff",
    ]

    stats = organize.main(url1, url2, date)

    if (stats == -1):
        z = 0
    else:
        array = np.array([float(stats[f]) for f in featureOrder]).reshape(1, -1)

        prediction = logreg.predict(array)
        print()
        if prediction[0] == 1:
        
            return "Expect Fighter 1 Win"
        else:
            
            return "Expect Fighter 2 Win"
    return "SKIP"

