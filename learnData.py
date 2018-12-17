import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

df = pd.read_csv("code_9433_plus.csv")
df = df.sort_values(by=["index"], ascending=False)
print(df.tail(20))


df = df.iloc[0:len(df) - 1]
print(df.tail())

df_train = df.iloc[1:len(df)-1]
df_test = df.iloc[len(df)-1:len(df)]

#print("train", df_train)
#print("test", df_test)

xlist = [

		"diff_1309",#上海株式指数・上証50連動型上場投資信託

		"diff_1322",#上場インデックスファンド中国A株（パンダ）CSI300

		"diff_1326",#SPDRゴールド・シェア

		"diff_1343",#NEXT FUNDS 東証REIT指数連動型上場投信

		"diff_1543",#純パラジウム上場信託（現物国内保管型）

		"diff_1551",#JASDAQ-TOP20上場投信

		"diff_1633",#NEXT FUNDS 不動産（TOPIX-17）上場投信

		"diff_1678",#NEXT FUNDS インド株式指数・Nifty 50連動型上場投信

		"diff_1681",#上場インデックスファンド海外新興国株式（MSCIエマージング）

		"diff_1682",#NEXT FUNDS 日経・東商取白金指数連動型上場投信

		"diff_1698",#上場インデックスファンド日本高配当（東証配当フォーカス100）

		]


x_train = []
y_train = []
for s in range(0, len(df_train) - 1):
	#print("x_train : ", df_train["Date"].iloc[s])
	#print("y_train : ", df_train["Date"].iloc[s + 1])
	#print("")
	x_train.append(df_train[xlist].iloc[s])

	if df_train["Close"].iloc[s + 1] > df_train["Close"].iloc[s]:
		y_train.append(1)
	else:
		y_train.append(-1)

#print(x_train)
#print(y_train)

rf = RandomForestClassifier(n_estimators=len(x_train), random_state=0)
rf.fit(x_train, y_train)


test_x = df_test[xlist].iloc[0]
test_y = rf.predict(test_x.values.reshape(1, -1))

print("result : ", test_y[0])
