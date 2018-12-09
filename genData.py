import pandas as pd


df = pd.read_csv("code_4307.csv", header=0)
df.columns=["Date", "Open", "High", "Low", "Close", "Volume", "Trading Value"]
df["index"] = [i for i in range(len(df))]
print(df.head(20))

etf_list = [

		1309,#上海株式指数・上証50連動型上場投資信託

		1313,#サムスンKODEX200証券上場指数投資信託

		1314,#上場インデックスファンドS&P日本新興株100

		1322,#上場インデックスファンド中国A株（パンダ）CSI300

		1326,#SPDRゴールド・シェア

		1343,#NEXT FUNDS 東証REIT指数連動型上場投信

		1543,#純パラジウム上場信託（現物国内保管型）

		1548,#上場インデックスファンド中国H株（ハンセン中国企業株）

		#1549,#上場インデックスファンドNifty50先物（インド株式）

		1551,#JASDAQ-TOP20上場投信

		1633,#NEXT FUNDS 不動産（TOPIX-17）上場投信

		#1649,

		1673,#ETFS 銀上場投資信託

		1678,#NEXT FUNDS インド株式指数・Nifty 50連動型上場投信

		1681,#上場インデックスファンド海外新興国株式（MSCIエマージング）

		1682,#NEXT FUNDS 日経・東商取白金指数連動型上場投信

		1698,#上場インデックスファンド日本高配当（東証配当フォーカス100）

		]

for etf in etf_list:
	#print(etf)
	df_etf = pd.read_csv("etf_" + str(etf) + ".csv", header=0)
	df_etf.columns=["Date", "Open", "High", "Low", "Close", "Volume", "Trading Value"]

	dates = []
	closeis = []
	for d in df["Date"]:
		#try:
		date = df_etf.loc[(df_etf.Date == d), "Date"]
		yesterday_date = date.values[0]
		dates.append(date.values[0])

		close = df_etf.loc[(df_etf.Date == d), "Close"]
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