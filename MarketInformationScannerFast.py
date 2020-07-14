"""
Program Name: Market Information Scanner Fast
Functions Included:
    GetMarketValue
    GetSingleMarketValue
    GetAvgMarketOrder
    GetMarketInformation
Version: V1.0
Created By: Kevin Bichoupan
"""

import requests;
import json;
import ast;
import pandas;


def GetMarketValue():
    MarketValueData = requests.get("https://api.binance.com/api/v1/ticker/allPrices");
    MVD_Dict = ast.literal_eval(ast.literal_eval(json.dumps(MarketValueData.text)));
    DF = pandas.DataFrame.from_dict(MVD_Dict)[['symbol', 'price']];
    DF = DF[DF['symbol'].str.contains('BTC')];
    DF = (DF.sort_values('symbol')).reset_index(drop=True);
    return DF;

def GetAvgMarketOrder(symbol):
    MarketOrderData = requests.get("https://api.binance.com/api/v1/depth?symbol="+symbol);
    MOD_Dict = ast.literal_eval(ast.literal_eval(json.dumps(MarketOrderData.text)));
    TotalAsk = 0;
    WeightedAvgAsk = 0;
    TotalAskVol = 0;
    for i in MOD_Dict['asks']:
        TotalAsk = TotalAsk + float(i[0])*float(i[1]);
        TotalAskVol = TotalAskVol + float(i[1]);
    WeightedAvgAsk = TotalAsk/TotalAskVol;
    return WeightedAvgAsk;


def GetMarketInformation():
    Symbol = '';
    Price = 0;
    WeightedAvgAsk = 0;
    PercentAskVariation = 0;
    AverageMarketOrders = [];
    DF = pandas.DataFrame(columns = ['Symbol', 'Price', 'Weighted Average Ask', '% Ask Variation']);
    MarketValueDF = GetMarketValue();
    for index, row in MarketValueDF.iterrows():
        Symbol = str(row.symbol);
        Price = float(row.price);
        WeightedAvgAsk = GetAvgMarketOrder(Symbol);
        PercentAskVariation = (WeightedAvgAsk - Price)/Price;
        DF.loc[len(DF.index)] = [Symbol, Price, WeightedAvgAsk, PercentAskVariation];

    return DF.loc[DF['% Ask Variation'] > 0.1];

if __name__ == '__main__':
    GetMarketInformation();
                       
                          
