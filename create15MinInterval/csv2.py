import pandas as pd
# import mplfinance

originalData = pd.read_csv('/Users/khushnarang/PycharmProjects/FirstWork/DataUsed/nifty_5minute_data.csv')

originalData['date'] = pd.to_datetime(originalData['date'])


originalData.set_index('date', inplace = True)

df_resampled = originalData.resample('15T').agg({
    'open': 'first',
    'high': 'max',
    'low': 'min',
    'close': 'last',
    'volume': 'sum'
}).dropna()

df_resampled = df_resampled.reset_index()
df = pd.DataFrame(df_resampled)
df.to_csv('/Users/khushnarang/Desktop/newCsv/create15MinInterval/15MinInterval.csv', index=False)

newData = pd.read_csv('/Users/khushnarang/Desktop/newCsv/create15MinInterval/15MinInterval.csv')
# newData['date'] = pd.to_datetime(newData['date'])
# mplfinance.plot(newData.set_index('date'), type = "candle", style = "charles")