#  bullish --> Hammer
#  bearish --> marubuzu



import talib
import numpy as np
import pandas as pd

# file directory
tradeArray1 = np.array([])
tradeArray2 = np.array([])
tradeArray3 = np.array([])
typeArray = np.array([])
indexArray = np.array([])
dummyIndex = 0
df = pd.read_csv('/Users/khushnarang/Desktop/newCsv/Combinations/newData.csv')
dataAll = pd.read_csv('//Users/khushnarang/Desktop/newCsv/create15MinInterval/15MinInterval.csv')
dataAll['date'] = pd.to_datetime(dataAll['date'])

hammer_count = 0
bearish_marubuzu_pattern = 0

for j in range(0, 54):
    combinationType = 'hammer/marubuzu'
    unique_dates = dataAll['date'].dt.date.unique()
    second_data = unique_dates[j]
    data = dataAll[dataAll['date'].dt.date == second_data]
    # Convert the data to numpy arrays
    open_price = np.array(data['open'])
    high_price = np.array(data['high'])
    low_price = np.array(data['low'])
    close_price = np.array(data['close'])

    hammer_pattern = talib.CDLHAMMER(open_price, high_price, low_price, close_price)

    marubuzu_pattern = talib.CDLMARUBOZU(open_price, high_price, low_price, close_price)


    hammer_count += len([x for x in hammer_pattern if x == 100])
    bearish_marubuzu_pattern += len([x for x in marubuzu_pattern  if x == -100])



    my_array = np.zeros(len(data['close']))

    index = 0
    for x in hammer_pattern:
        if x == 100:
            my_array[index] += 1
        index += 1

    index = 0
    for x in marubuzu_pattern:
        if x == -100:
            my_array[index] -= 1
        index += 1

    # for x in my_array:
    #     if x == 2:
    #         print(x)
    #     elif x == -2:
    #         print(x)


    initial_investment = 100
    dummy_investment = 0
    signal = 0  # will tell about buy time and sell time

    recent_buy = 0
    for i in range(0, len(my_array)):
        if my_array[i] == 1 and signal == 0:
            signal = 1
            dummy_investment -= data['open'][i + (25 * j)]
            recent_buy = data['open'][i + (25 * j)]
        elif my_array[i] == -1 and signal == 1:
            signal = 0
            dummy_investment += data['open'][i + (25 * j)]

    if signal == 1:
        dummy_investment += recent_buy
    outcomeWithoutPattern = initial_investment + (data['close'][25 * j + 24] - data['open'][25 * j]) * (
        initial_investment) / data['open'][25 * j]
    outcomeWithPattern = initial_investment + (dummy_investment * initial_investment / data['open'][25 * (j)])

    tradeArray1 = np.append(tradeArray1, outcomeWithPattern)
    tradeArray2 = np.append(tradeArray2, outcomeWithoutPattern)
    tradeArray3 = np.append(tradeArray3, initial_investment)
    typeArray = np.append(typeArray, combinationType)
    indexArray = np.append(indexArray, dummyIndex)
    dummyIndex += 1
    # print("DAY:- ", second_data, end="  ||  ")
    # print("Current Investment Value by using pattern: $", outcomeWithPattern)
    # print("\nCurrent Investment Value without using pattern: $", outcomeWithoutPattern)

# newData['InitialInvestment'] = tradeArray3
# newData['InvestmentUsingPattern'] = tradeArray1
# newData['InvestmentWithoutPattern'] = tradeArray2
# newData.to_csv('/Users/khushnarang/PycharmProjects/FirstWork/DataRecived/Combination2.csv', index = False)

data = {'index': indexArray, 'date': unique_dates, 'combination': typeArray, 'InitialInvestment': tradeArray3,
        'InvestmentUsingPattern': tradeArray1, 'InvestmentWithoutPattern': tradeArray2}
new_rows = pd.DataFrame(data)
df = pd.concat([df, new_rows], ignore_index=True)
df.to_csv('/Users/khushnarang/Desktop/newCsv/Combinations/newData.csv', index=False)