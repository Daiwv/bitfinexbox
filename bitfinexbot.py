# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 23:13:06 2016

@author: xanadmin
"""
import websocket
import json
import threading
import numpy
import time
#market_orders_unparsed={}
market_orders={}
def start_polling(message_data,marknum):
    def on_message(ws, message):
#        print message
        if message.find('hb') == -1:
#            market_orders_unparsed[marknum]=message
            market_orders[marknum]=numpy.fromstring(message[1:-1],sep=",")
#            if marknum == 0:
#                print time.ctime()
    
    def on_error(ws, error):
        print error
    
    def on_close(ws):
        print "### closed ###"
    
    def on_open(ws):
        ws.send(message_data)
    #    def run(*args):
    #    thread.start_new_thread(run, ())
    
    
    if __name__ == "__main__":
#        websocket.enableTrace(True)
        ws = websocket.WebSocketApp("wss://api2.bitfinex.com:3000/ws",
                                    on_message = on_message,
                                    on_error = on_error,
                                    on_close = on_close)
        ws.on_open = on_open
        wst = threading.Thread(target=ws.run_forever)
        wst.daemon = True
        wst.start()

# Market 0
message_data=json.dumps({"event":"subscribe","channel":"ticker","pair":"BTCUSD","prec":"P0"})
start_polling(message_data,0)
# Market 1
message_data=json.dumps({"event":"subscribe","channel":"ticker","pair":"LTCUSD","prec":"P0"})
start_polling(message_data,1)
# Market 2
message_data=json.dumps({"event":"subscribe","channel":"ticker","pair":"LTCBTC","prec":"P0"})
start_polling(message_data,2)

# market_orders[0][1] is a bid and market_orders[0][3] is an ask
#  Forwards would be a sell at highest bid BTC->USD, a buy at lowest ask USD->LTC, a sell at highest bid LTC->BTC on markets 0, 1, 2
# Backwards would be a buy at lowest ask BTC->LTC, sell at highest bid LTC->USD, then buy at lowest ask USD->BTC on markets 2, 1, 0
testwallet=1

#FORWARDS
def forward_search():
    global n_forw,n_forw_bad, for_run,result_for
    n_forw=0
    n_forw_bad=0
    for_run=1
    while for_run==1:    
        time.sleep(0.3)
        result_for=(((((market_orders[0][1]*testwallet)*.998)/market_orders[1][3])*.998)*market_orders[2][1])*.998
        if result_for > 1:
            n_forw=n_forw+1
            print 'FORWARDS (Bitfinex)'
            print time.ctime()
        else:
            n_forw_bad=n_forw_bad+1
        

#BACKWARDS
def backward_search():
    global n_back,n_back_bad, bac_run,result_bac
    n_back=0
    n_back_bad=0
    bac_run=1
    while bac_run==1:
        time.sleep(0.3)
        result_bac=(((((testwallet/market_orders[2][3])*.998)*market_orders[1][1])*.998)/market_orders[0][3])*.998
        if result_bac > 1:
            n_back=n_back+1
            print 'BACKWARDS (Bitfinex)'
            print time.ctime()
        else:
            n_back_bad=n_back_bad+1
  
fsT=threading.Thread(target=forward_search)
bsT=threading.Thread(target=backward_search)
fsT.daemon=True
bsT.daemon=True
fsT.start()
bsT.start()


# REMEMBER to turn off both searches when initiating a trade
# TO DO:
# Find max amounts that can be traded through all 3 trades at once - only trade that
# Incorporate fees
# Code trades
# Put in while loop


