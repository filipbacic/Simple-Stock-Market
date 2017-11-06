# -*- coding: utf-8 -*-

from stock_market import *
import unittest
from scipy.stats.mstats import gmean

class MyTest(unittest.TestCase):
    def test_creating_stock(self):
        self.assertTrue(stocks == {})
        self.assertEqual(create_stock('TEA', 'C', 0, 100), None)
        self.assertTrue(stocks['TEA'] == Stock('TEA', 'C', 0, 100, None))
        self.assertEqual(create_stock('POP', 'C', 8, 100), None)
        self.assertEqual(create_stock('ALE', 'C', 23, 60), None)
        self.assertEqual(create_stock('GIN', 'P', 8, 100, 0.02), None)
        self.assertEqual(create_stock('JOE', 'C', 13, 250), None)        
        
        with self.assertRaises(Error, msg= "Stock TEA is already created."):
            create_stock('TEA', 'C', 0, 100)
            
        with self.assertRaises(Error, msg= "Stock type is not properly set."):
            create_stock('COF', 'T', 0, 100)
            
        with self.assertRaises(Error, msg= "Last Dividend needs to be non-negative."):
            create_stock('COF', 'C', -5, 100)
            
        with self.assertRaises(Error, msg= "Par Value needs to be non-negative."):
            create_stock('COF', 'C', 0, -100)
            
        with self.assertRaises(Error, msg= "Fixed Dividend needs to be non-negative."):
            create_stock('COF', 'P', 8, 100, -0.02)
            
        with self.assertRaises(Error, msg= "Please set all arguments correctly."):
            create_stock('COF', 'C', 'C', 100)
            
        stocks.clear()

    def test_removing_stock(self):
        with self.assertRaises(Error, msg= "Stock POP is not yet created."):
            remove_stock('POP')        
        
        self.assertEqual(create_stock('POP', 'C', 0, 100), None)
        
        self.assertTrue('POP' in stocks)
        remove_stock('POP')
        self.assertFalse('POP' in stocks)        
        
    def test_changing_stock_type(self):
        with self.assertRaises(Error, msg= "Stock TEA is not yet created."):
            change_stock_type('TEA', 'P', 0.05)       
        
        self.assertEqual(create_stock('TEA', 'C', 0, 100), None)
        self.assertEqual(create_stock('GIN', 'P', 8, 100, 0.02), None)        
        self.assertEqual(change_stock_type('TEA', 'P', 0.05), None)
        self.assertTrue(stocks['TEA'] == Stock('TEA', 'P', 0, 100, 0.05))
        self.assertEqual(change_stock_type('GIN', 'C'), None)
        self.assertTrue(stocks['GIN'] == Stock('GIN', 'C', 8, 100, None))                
            
        with self.assertRaises(Error, msg= "Stock type is not properly set."):
            change_stock_type('TEA', 'H')
            
        with self.assertRaises(Error, msg= "Fixed Dividend needs to be non-negative."):
            change_stock_type('GIN', 'P', -0.05)
            
        with self.assertRaises(Error, msg= "Please set all arguments correctly."):
            change_stock_type('GIN', 'P')
        
        stocks.clear()
        
    def test_changing_last_dividend(self):
        with self.assertRaises(Error, msg= "Stock TEA is not yet created."):
            change_last_dividend('TEA', 6)       
        
        self.assertEqual(create_stock('TEA', 'C', 0, 100), None)        
        self.assertEqual(change_last_dividend('TEA', 6), None)
        self.assertTrue(stocks['TEA'] == Stock('TEA', 'C', 6, 100, None))                           
            
        with self.assertRaises(Error, msg= "Last Dividend needs to be non-negative."):
            change_last_dividend('TEA', -6)
            
        with self.assertRaises(Error, msg= "Please set all arguments correctly."):
            change_last_dividend('TEA', 'C')
        
        stocks.clear()     
        
    def test_changing_par_value(self):
        with self.assertRaises(Error, msg= "Stock TEA is not yet created."):
            change_par_value('TEA', 75)       
        
        self.assertEqual(create_stock('TEA', 'C', 0, 100), None)        
        self.assertEqual(change_par_value('TEA', 75), None)
        self.assertTrue(stocks['TEA'] == Stock('TEA', 'C', 0, 75, None))                           
            
        with self.assertRaises(Error, msg= "Par Value needs to be non-negative."):
            change_par_value('TEA', -75)
            
        with self.assertRaises(Error, msg= "Please set all arguments correctly."):
            change_par_value('TEA', 'C')
        
        stocks.clear()   
        
    def test_changing_fixed_dividend(self):
        with self.assertRaises(Error, msg= "Stock TEA is not yet created."):
            change_fixed_dividend('TEA', 0.05)       
        
        self.assertEqual(create_stock('TEA', 'C', 0, 100), None)  
        self.assertEqual(create_stock('GIN', 'P', 8, 100, 0.02), None)
        self.assertEqual(change_fixed_dividend('GIN', 0.05), None)
        self.assertTrue(stocks['GIN'] == Stock('GIN', 'P', 8, 100, 0.05))                           

        with self.assertRaises(Error, msg= "Stock needs to be of Preferred type."):
            change_fixed_dividend('TEA', 0.05)
            
        with self.assertRaises(Error, msg= "Fixed Dividend needs to be non-negative."):
            change_fixed_dividend('GIN', -0.05)
            
        with self.assertRaises(Error, msg= "Please set all arguments correctly."):
            change_fixed_dividend('GIN', 'C')
        
        stocks.clear()  

    def test_dividend_yield(self):
        with self.assertRaises(Error, msg= "Stock TEA is not yet created."):
            dividend_yield('TEA', 150)
            
        self.assertEqual(create_stock('TEA', 'C', 5, 100), None)
        self.assertEqual(create_stock('GIN', 'P', 8, 100, 0.02), None)
        self.assertEqual(dividend_yield('TEA', 150), 5/150)
        self.assertEqual(dividend_yield('GIN', 150), 0.02*100/150)
        
        with self.assertRaises(Error, msg= "Stock price needs to be positive."):
            dividend_yield('GIN', -150)    
            
        with self.assertRaises(Error, msg= "Stock price needs to be positive."):
            dividend_yield('GIN', 0)

        with self.assertRaises(Error, msg= "Please set all arguments correctly."):
            dividend_yield('GIN', 'C')            
        
        stocks.clear() 
        
    def test_pe_ratio(self):
        with self.assertRaises(Error, msg= "Stock TEA is not yet created."):
            pe_ratio('TEA', 80)
            
        self.assertEqual(create_stock('TEA', 'C', 5, 100), None)
        self.assertEqual(create_stock('GIN', 'P', 8, 100, 0.02), None)
        self.assertEqual(pe_ratio('TEA', 80), 80/5)
        self.assertEqual(pe_ratio('GIN', 150), 150/8)
        
        self.assertEqual(create_stock('POP', 'C', 0, 100), None)
        
        with self.assertRaises(Error, msg= "Stock price needs to be positive."):
            pe_ratio('TEA', -80)    
            
        with self.assertRaises(Error, msg= "Stock price needs to be positive."):
            pe_ratio('TEA', 0)
            
        with self.assertRaises(Error, msg= "P/E Ratio cannot be calculated, because stock's Last Dividend is 0."):
            pe_ratio('POP', 150)    

        with self.assertRaises(Error, msg= "Please set all arguments correctly."):
            pe_ratio('GIN', 'C')            
        
        stocks.clear()         
        
    def test_recording_trades(self):
        with self.assertRaises(Error, msg= "Stock TEA is not yet created."):
            record_trade('TEA', 5, 'B', 135)
            
        self.assertEqual(create_stock('TEA', 'C', 5, 100), None)
        self.assertEqual(create_stock('GIN', 'P', 8, 100, 0.02), None)
        self.assertEqual(record_trade('TEA', 5, 'B', 135, 1), None)
        self.assertEqual(record_trade('TEA', 15, 'S', 120), None)
        self.assertEqual(record_trade('GIN', 20, 'S', 56), None)
        self.assertEqual(record_trade('TEA', 18, 'B', 130, -1), None)
        self.assertEqual(record_trade('GIN', 10, 'B', 70, -2), None)
        
        self.assertEqual(stocks['TEA'].trade_records, [(-1, 5, 'B', 135),
                               (0, 15, 'S', 120), (1, 18, 'B', 130)])

        self.assertEqual(stocks['GIN'].trade_records, [(0, 20, 'S', 56), (2, 10, 'B', 70)])

        with self.assertRaises(Error, msg= "Stock price needs to be positive."):
            record_trade('TEA', 15, 'S', -120)    
            
        with self.assertRaises(Error, msg= "Stock price needs to be positive."):
            record_trade('TEA', 15, 'S', 0)
            
        with self.assertRaises(Error, msg= "Quantity needs to be positive."):
            record_trade('TEA', -15, 'S', -120)    
            
        with self.assertRaises(Error, msg= "Quantity needs to be positive."):
            record_trade('TEA', 0, 'S', 0)
            
        with self.assertRaises(Error, msg= "Buy or sell indicator is not properly set."):
            record_trade('TEA', 15, 'C', 120)
            
        with self.assertRaises(Error, msg= "Buy or sell indicator is not properly set."):
            record_trade('TEA', 15, 120, 120)
            
        with self.assertRaises(Error, msg= "Please set all arguments correctly."):
            record_trade('TEA', 'B', 'S', 120)             
                               
        stocks.clear()
        
    def test_volume_weighted_stock_price(self):
        with self.assertRaises(Error, msg= "Stock TEA is not yet created."):
            volume_weighted_stock_price('TEA')
            
        self.assertEqual(create_stock('TEA', 'C', 5, 100), None)
        self.assertEqual(create_stock('GIN', 'P', 8, 100, 0.02), None)
        self.assertEqual(record_trade('TEA', 5, 'B', 135, 1000), None)
        self.assertEqual(record_trade('TEA', 15, 'S', 120, 100), None)
        self.assertEqual(record_trade('GIN', 20, 'S', 56, 500), None)
        self.assertEqual(record_trade('TEA', 18, 'B', 130), None)
        self.assertEqual(record_trade('GIN', 10, 'B', 70, -2), None)
        
        self.assertEqual(stocks['TEA'].trade_records, [(-1000, 5, 'B', 135),
                               (-100, 15, 'S', 120), (0, 18, 'B', 130)])

        self.assertEqual(stocks['GIN'].trade_records, [(-500, 20, 'S', 56), (2, 10, 'B', 70)])
        
        self.assertEqual(volume_weighted_stock_price('TEA'), (15*120 + 18*130)/(15+18))
        self.assertEqual(volume_weighted_stock_price('GIN'), (20*56 + 10*70)/(20+10))
        
        stocks.clear()
        
    def test_gbce_all_share_index(self):
        with self.assertRaises(Error, msg= "There are no trade records."):
            gbce_all_share_index()
            
        self.assertEqual(create_stock('TEA', 'C', 5, 100), None)
        self.assertEqual(create_stock('GIN', 'P', 8, 100, 0.02), None)
        self.assertEqual(create_stock('POP', 'C', 8, 100), None)
        
        with self.assertRaises(Error, msg= "There are no trade records."):
            gbce_all_share_index()
        
        self.assertEqual(record_trade('TEA', 5, 'B', 135, 1000), None)
        self.assertEqual(record_trade('TEA', 15, 'S', 120, 100), None)
        self.assertEqual(record_trade('GIN', 20, 'S', 56, 500), None)
        self.assertEqual(record_trade('POP', 18, 'B', 130), None)
        self.assertEqual(record_trade('GIN', 10, 'B', 70, -2), None)
        
        self.assertEqual(stocks['TEA'].trade_records, [(-1000, 5, 'B', 135),
                               (-100, 15, 'S', 120)])

        self.assertEqual(stocks['GIN'].trade_records, [(-500, 20, 'S', 56), (2, 10, 'B', 70)])
        
        self.assertEqual(stocks['POP'].trade_records, [(0, 18, 'B', 130)])
        
        self.assertEqual(gbce_all_share_index(), gmean([120, 70,130]))
        
        stocks.clear()        

if __name__ == '__main__':
    unittest.main()
    #print(stocks)