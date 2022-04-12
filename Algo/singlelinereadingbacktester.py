# Apr_08 Backtester for single-line data

# Instructions:
#
# from backTester import backTest
#
# backTest(
#    list_of_values {python.list}, 
#    list_of_dates {python.list},
#    strategy {function(list) -> Any},
#    start_index {int}, 
#    strategy_inc_pred [optional = True],
#    strategy_dec_pred [optional = False],
#    strategy_null_pred [optional = None],
#    backtest_interval [optional = 1{days}],
#    for_profit [optional = False]
# ) -> return 0

def backTest(dataVal = 0, dataDate = 0, strategy = 0, startDate = 0, trueVal = True, falseVal = False, nullVal = None, testFreq = 1, for_profit = False):
    
    if dataVal == 0 or dataDate == 0 or strategy == 0 or startDate == 0:
        print("Error: dataVal, dataDate, strategy, startDate must be defined")
        return 1

    currData = []
    msgCount = 0
    indexVal = 1.00
    if for_profit == True:
        purchaseVal = 0.00
        purchasedMode = None
    
    for i in range(startDate, len(dataVal), testFreq):
        currData.append(dataVal[i])
        try:
            if (strategy(currData) == trueVal):
                print("Future Inc on day: " + str(dataDate[i]))
                msgCount += 1

                if for_profit == True:
                    if purchasedMode == "Short":
                        indexVal = _calcReturns(indexVal, purchaseVal, currData[i], "Short")
                        purchasedMode = None
                        purchaseVal = 0.00
                    elif purchasedMode == None:
                        purchasedMode = "Long"
                        purchaseVal = currData[i]

            elif (strategy(currData) == falseVal):
                print("Future Dec on day: " + str(dataDate[i]))
                msgCount += 1

                if for_profit == True:
                    if purchasedMode == "Long":
                        indexVal = _calcReturns(indexVal, purchaseVal, currData[i], "Long")
                        purchasedMode = None
                        purchaseVal = 0.00
                    elif purchasedMode == None:
                        purchasedMode = "Short"
                        purchaseVal = currData[i]

            elif (strategy(currData) == nullVal):
                print("No prediction on day: " + str(dataDate[i]))
        except:
            print("Error: strategy execution failed on day: " + str(dataDate[i]))
            return 1

    print(str(len(dataVal) - startDate) + " days of data tested, " + str(msgCount) + " predictions sent.")
    if for_profit == True:
        print("Initial value: 1.00, Final value: " + str(indexVal))

    print("Backtest complete")
    return 0

def _calcReturns(indexVal, purchaseVal, currVal, mode):
    if mode == "Long":
        #calculate percent change
        percentChange = ((currVal - purchaseVal) / purchaseVal) * 100
        return indexVal * (1 + percentChange)

    elif mode == "Short":
        percentChange = ((purchaseVal - currVal) / purchaseVal) * 100
        return indexVal * (1 + percentChange)
