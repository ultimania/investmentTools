import pandas as pd


df = pd.read_csv("4307_2018.csv", header=0)
df.columns=["Date", "Open", "High", "Low", "Close", "Volume", "Trading Value"]
df["index"] = [i for i in range(len(df))]
print(df.head(20))

etf_list = [

		1309,#上海株式指数・上証50連動型上場投資信託

		1322,#上場インデックスファンド中国A株（パンダ）CSI300

		1326,#SPDRゴールド・シェア

		1343,#NEXT FUNDS 東証REIT指数連動型上場投信

		1543,#純パラジウム上場信託（現物国内保管型）

		1551,#JASDAQ-TOP20上場投信

		1633,#NEXT FUNDS 不動産（TOPIX-17）上場投信

		1678,#NEXT FUNDS インド株式指数・Nifty 50連動型上場投信

		1681,#上場インデックスファンド海外新興国株式（MSCIエマージング）

		1682,#NEXT FUNDS 日経・東商取白金指数連動型上場投信

		1698,#上場インデックスファンド日本高配当（東証配当フォーカス100）

		]

for etf in etf_list:
	#print(etf)
	df_etf = pd.read_csv(str(etf) + "_2018.csv", header=0)
	df_etf.columns=["Date", "Open", "High", "Low", "Close", "Volume", "Trading Value"]

	dates = []
	closeis = []
	for d in df["Date"]:
		#try:
		date = df_etf.loc[(df_etf.Date == d), "Date"]
        if len(date) == 0:
            date = tmp_date
        else:
            tmp_date = date
		yesterday_date = date.values[0]
		dates.append(date.values[0])

		close = df_etf.loc[(df_etf.Date == d), "Close"]
        if len(close) == 0:
            close = tmp_close
        else:
            tmp_close = close
		if str(close.values[0]) != str("nan"):
			yesterday_close = close.values[0]
			closeis.append(close.values[0])	

		else:
			#print("nan")
			closeis.append(yesterday_close)
		
	df_etf2 = pd.DataFrame({"Date_" + str(etf) : dates,
							"Close_" + str(etf) : closeis})

	df = pd.concat([df, df_etf2], axis=1)
	df["diff_" + str(etf)] = (df["Close_" + str(etf)] / df["Close_" + str(etf)].shift(-1)) - 1
	#print(df)

df.to_csv("code_4307_plus.csv")