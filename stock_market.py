# -*- coding: utf-8 -*-

import time
from scipy.stats.mstats import gmean

"""
This is the main file where all the classes and functions are defined for using
simple stock market.
Comments are put only to places where they really enhance understanding.
"""

class Stock:
    """Main class for storing stock info."""    
    def __init__(self, stock_name, stock_type, last_dividend, par_value, fixed_dividend):
        self.stock_name = stock_name
        self.stock_type = stock_type[:1].upper()
        self.last_dividend = last_dividend
        self.par_value = par_value
        self.fixed_dividend = fixed_dividend
        # timestamp_start is used so that in trade_records we are not dealing with big numbers
        self.timestamp_start = round(time.time())        
        self.trade_records = []
        
    def __eq__(self, otherStock):
        # used only in unit test for comparing two instances of Stock class
        return (self.stock_name == otherStock.stock_name and self.stock_type == otherStock.stock_type and
                self.last_dividend == otherStock.last_dividend and self.par_value == otherStock.par_value and
                self.fixed_dividend == otherStock.fixed_dividend and 
                self.trade_records[:] == otherStock.trade_records[:])                
        

class Error(Exception):
    def __init__(self, msg):
        print(msg)


stocks = {}
""" 
Dictionary for keeping all Stock instances, so that stocks can be referenced by their name
"""

def create_stock(stock_name, stock_type, last_dividend, par_value, fixed_dividend = None):
    try:
        if stock_name in stocks:
            raise Error("Stock " + stock_name + " is already created.")
        
        if stock_type not in ('C', 'P'):
            raise Error("Stock type is not properly set.")
        
        if last_dividend < 0:
            raise Error("Last Dividend needs to be non-negative.")
            
        if par_value < 0:
            raise Error("Par Value needs to be non-negative." ) 
            
        if stock_type == 'P' and fixed_dividend < 0:
            raise Error("Fixed Dividend needs to be non-negative.")
            
        stocks[stock_name] = Stock(stock_name, stock_type, last_dividend, par_value, fixed_dividend)     
    
    except TypeError:
        raise Error("Please set all arguments correctly.")


def remove_stock(stock_name):    
    if stock_name not in stocks:
        raise Error("Stock " + stock_name + " is not yet created.")
        
    del stocks[stock_name]


def change_stock_type(stock_name, new_stock_type, new_fixed_dividend = None):
    try:
        if stock_name not in stocks:
            raise Error("Stock " + stock_name + " is not yet created.")
        
        if new_stock_type not in ('C', 'P'):
            raise Error("Stock type is not properly set.")        
            
        if new_stock_type == 'P' and new_fixed_dividend < 0:
            raise Error("Fixed Dividend needs to be non-negative.")
        
        stock = stocks[stock_name]       
        
        stock.stock_type = new_stock_type
        stock.fixed_dividend = new_fixed_dividend
    
    except TypeError:
        raise Error("Please set all arguments correctly.")   
        

def change_last_dividend(stock_name, new_last_dividend):
    try:
        if stock_name not in stocks:
            raise Error("Stock " + stock_name + " is not yet created.")            
            
        if new_last_dividend < 0:
            raise Error("Last Dividend needs to be non-negative.")
            
        stocks[stock_name].last_dividend = new_last_dividend
    
    except TypeError:
        raise Error("Please set all arguments correctly.")           


def change_par_value(stock_name, new_par_value):
    try:
        if stock_name not in stocks:
            raise Error("Stock " + stock_name + " is not yet created.")            
            
        if new_par_value < 0:
            raise Error("Par Value needs to be non-negative." ) 
            
        stocks[stock_name].par_value = new_par_value
    
    except TypeError:
        raise Error("Please set all arguments correctly.")


def change_fixed_dividend(stock_name, new_fixed_dividend):
    try:
        if stock_name not in stocks:
            raise Error("Stock " + stock_name + " is not yet created.")  
            
        stock = stocks[stock_name]
            
        if stock.stock_type == 'C':
            raise Error("Stock needs to be of Preferred type.")
        
        if new_fixed_dividend < 0:
            raise Error("Fixed Dividend needs to be non-negative.")
            
        stock.fixed_dividend = new_fixed_dividend
    
    except TypeError:
        raise Error("Please set all arguments correctly.")
        

def dividend_yield(stock_name, stock_price):
    try:
        if stock_name not in stocks:
            raise Error("Stock " + stock_name + " is not yet created.")
            
        if stock_price <= 0:
            raise Error("Stock price needs to be positive.")
        
        stock = stocks[stock_name]
        
        if stock.stock_type == 'P':
            return stock.fixed_dividend * stock.par_value / stock_price            
        else:
            return stock.last_dividend / stock_price
            
    except TypeError:
        raise Error("Please set all arguments correctly.")
        
        
def pe_ratio(stock_name, stock_price):
    try:
        if stock_name not in stocks:
            raise Error("Stock " + stock_name + " is not yet created.")
            
        if stock_price <= 0:
            raise Error("Stock price needs to be positive.")
        
        stock = stocks[stock_name]
        
        # This can be changed to be normal output and not an error, but this 
        #     case was not described in the assignment
        if stock.last_dividend == 0:
            raise Error("P/E Ratio cannot be calculated, because stock's Last Dividend is 0.")
        
        return stock_price / stock.last_dividend
            
    except TypeError:
        raise Error("Please set all arguments correctly.")       
        
        
def record_trade(stock_name, quantity, buy_sell_ind, stock_price, time_shift = 0):
    """
    Add new entry to stock's trade_records list
    """
    try:
        if stock_name not in stocks:
            raise Error("Stock " + stock_name + " is not yet created.")
            
        if stock_price <= 0:
            raise Error("Stock price needs to be positive.")
            
        if quantity <= 0:
            raise Error("Quantity needs to be positive.")
        
        if buy_sell_ind not in ('B', 'S'):
            raise Error("Buy or sell indicator is not properly set.")         
        
        stock = stocks[stock_name]       
        
        # time_shift is used only for testing purposes so that we can easily simulate records through time
        # timestamp_start is used so that in trade_records we are not dealing with big timestamps
        timestamp = round(time.time() - stock.timestamp_start - time_shift)
        
        stock.trade_records.append((timestamp, quantity, buy_sell_ind, stock_price))
            
    except TypeError:
        raise Error("Please set all arguments correctly.")

def volume_weighted_stock_price(stock_name):
    try:
        if stock_name not in stocks:
            raise Error("Stock " + stock_name + " is not yet created.")
   
        stock = stocks[stock_name]       
        
        # specified in minutes
        window_length = 15        
        
        # used as a boundary, so that only stocks with timestamps greater or 
        #    equal to this are taken into account
        boundary_timestamp = round(time.time() - window_length * 60 - stock.timestamp_start)
        
        quantity_sum = 0
        quantity_price_sum = 0
        result = 0
        # calculations start with latest trades down until trades around boundary_timestamp
        for record in reversed(stock.trade_records):
            if record[0] < boundary_timestamp:
                break
            # record[1] is quantity and and record[3] is price 
            quantity_sum += record[1]
            quantity_price_sum += record[1]*record[3]
        
        if quantity_sum > 0:
            result = quantity_price_sum / quantity_sum
            
        return result   
    except TypeError:
        pass

def gbce_all_share_index():
    """
    Return GBCE All Share Index using the geometric mean of prices for all stocks
    Last traded prices are used.
    Stocks which do not have trade records are ecluded from calculations.     
    """
    try:        
        excluded_stocks = []
        prices = []
        for stock in stocks.values():
            if len(stock.trade_records) > 0:
                # last traded price is used
                prices.append(stock.trade_records[-1][3])
            else:
                # excluded_stocks is not later used, but can be used for info 
                #   about stocks which are not taken into account
                excluded_stocks.append(stock.stock_name)
        if len(prices) == 0:
            raise Error("There are no trade records.")
        
        return gmean(prices)
    except TypeError:
        pass
         

        