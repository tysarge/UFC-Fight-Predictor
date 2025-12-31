import pandas as pd
from sklearn.model_selection import train_test_split as tts
from sklearn.ensemble import RandomForestClassifier as rfc
from sklearn.metrics import accuracy_score as aS

data = pd.read_csv("organizedFightStats copy.csv", names=["kd_diff","sig_strike_diff","total_strikes_diff","td_diff","ctrl_time_diff","height_diff","weight_diff","reach_diff","age_diff","winrate_diff","winner"], header=0)

features = ['kd_diff','sig_strike_diff','total_strikes_diff','td_diff','ctrl_time_diff','height_diff','weight_diff','reach_diff','age_diff','winrate_diff']
X = data[features]
y = data.winner

X_train, X_test, y_train, y_test = tts(X, y, test_size=0.25, random_state=42)

model = rfc(n_estimators=400, random_state=42)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = aS(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")




