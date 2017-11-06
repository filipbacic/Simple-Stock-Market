# -*- coding: utf-8 -*-

from stock_market import *


"""
Few examples of how to use stock_market.py
"""

# creating stocks which will be tracked
create_stock('TEA', 'C', 0, 100)
create_stock('POP', 'C', 8, 100)
create_stock('ALE', 'C', 23, 60)
create_stock('GIN', 'P', 8, 100, 0.02)
create_stock('JOE', 'C', 13, 250)

change_stock_type('GIN', 'C')
change_stock_type('GIN', 'P', 0.02)

change_last_dividend('TEA', 6)
change_last_dividend('TEA', 0)

change_par_value('TEA', 75)
change_par_value('TEA', 100)

change_fixed_dividend('GIN', 0.05)
change_fixed_dividend('GIN', 0.02)


print("Dividend yields:")
print(dividend_yield('TEA', 100))
print(dividend_yield('POP', 100))
print(dividend_yield('ALE', 100))
print(dividend_yield('GIN', 100))
print(dividend_yield('JOE', 100))

print("P/E ratios:")
print(pe_ratio('POP', 100))
print(pe_ratio('ALE', 100))
print(pe_ratio('GIN', 100))
print(pe_ratio('JOE', 100))

# creating some trade records
record_trade('TEA', 5, 'B', 135, 1000)
record_trade('TEA', 15, 'S', 120, 100)
record_trade('GIN', 20, 'S', 56, 500)
record_trade('TEA', 18, 'B', 130)
record_trade('GIN', 10, 'B', 70, -2)


print("Volume Weighted Stock Prices:")
print(volume_weighted_stock_price('TEA'))
print(volume_weighted_stock_price('GIN'))

print("GBCE All Share Index:")
print(gbce_all_share_index())