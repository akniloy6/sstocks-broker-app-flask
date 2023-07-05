#Import necessary libraries

from flask import Flask, render_template, request, session, redirect, url_for
from flask_restful import Api,Resource
import json
import requests


#call app and api

app = Flask(__name__)
api = Api(app)

app.secret_key = '5765764' # Used for session management

# Load the shares data from a JSON file. replace this with the api's in the future

with open('stocks_broker.json') as f:
    shares_data = json.load(f)

with open('user_stock.json', 'r') as f:
    user_stock = json.load(f)

with open('user_detail.json', 'r') as f:
    user_data = json.load(f)

#app endpoints

#login

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    session['user_id'] = 'null'
    user_id = request.form['user_id']
    passs = request.form['password']
    #print(user_id)
    with open('user_detail.json') as f:
        users = json.load(f)
    us_id = users.get(user_id)
    print(us_id)
    print(type(us_id))
    session['user_id'] = user_id
    
    if us_id == None:
        session['user_id'] = 'null'
        return render_template('login.html', error='Invalid user_id')
    else:
        psw = us_id['password']
        print(psw)
        if psw == passs:
            print("okl")
            return redirect(url_for('users', u_id = user_id))
        elif psw== None:
            return render_template('login.html', error='invalid password')
        else:
            return render_template('login.html', error='invalid password')
    


#API to get json data

class Share_market(Resource):
    def get(self):
        with open('stocks_broker.json') as f:
            shares_data = json.load(f)
        return shares_data

api.add_resource(Share_market, '/market')

class User_info(Resource):
    def get(self):
        with open('user_detail.json') as f:
            user_data = json.load(f)
        return user_data

api.add_resource(User_info, '/user_data')

class User_stock(Resource):
    def get(self):
        with open('user_stock.json') as f:
            user_stock = json.load(f)
        return user_stock

api.add_resource(User_stock, '/user_stock')


#Route index

@app.route('/index')
def index():
    if session['user_id']== 'null':
        return redirect(url_for('login'))
    else:
        print(session['user_id'])
    shares = Share_market().get()
    return render_template('index_v2.html', shares=shares, u_id = session['user_id'])

# Define a function to update the shares data in the JSON file
def update_shares_data(stocks_broker):
    with open('stocks_broker.json', 'w') as f:
        json.dump(stocks_broker, f)
def update_user_stock_data(user_stock):
    with open('user_stock.json', 'w') as f:
        json.dump(user_stock, f)
def update_user_details_data(balance):
    with open('user_detail.json', 'w') as f:
        json.dump(balance, f)




# Define a route to display the search function
@app.route('/search', methods=['GET', 'POST'])
def search():
    keyword = request.args.get('keyword')
    symbol = request.args.get('symbol')
    print(keyword)
    print(symbol)

    if (keyword==None and symbol == None):
        return render_template('search.html')



    stock_data = Share_market().get()
    company_details = None

    if (keyword=="highest_price"):
        
        all_prices = []
        new_stock_data = []
        
        for stock in stock_data:
            all_prices.append(stock['price'])
            all_prices.sort(reverse=True)
        for i in range(len(all_prices)):
            for share in stock_data:
                if(share['price']==all_prices[i]):
                    new_stock_data.append(share)

        return render_template('sorted_by_highest_price.html', stock_data = new_stock_data)
    elif(keyword == None):
        for stock in stock_data:
            
            #print(stock)
            if stock['symbol'] == symbol:
                company_details = stock
                print(company_details)
        


        print(company_details)
        return render_template('company_details.html', company_details= company_details)

            
    return render_template('search.html')







# Define a route to display the user form

@app.route('/user/<u_id>', methods=['GET' ,'POST'])
def users(u_id):
    # Check if the user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))
    u_id = session['user_id']
    # Load the user data from the JSON file
    with open('user_detail.json', 'r') as f:
        users = json.load(f)
    with open('user_stock.json', 'r') as f:
        stocks = json.load(f)
    us_id = users.get(u_id)
    stocks_update = stocks.get(u_id)   
    return render_template('users.html', user_data=us_id, stocks = stocks_update)

#Api for buying share
class BuyShare(Resource):
    def post(self, symbol):
        share = None
        u_id = session['user_id']
        for s in shares_data:
            if s['symbol'] == symbol:
                share = s
                break
        price_per_share= share.get('price')
        stock_update = user_stock.get(u_id)
        user_ac_update = user_data.get(u_id)
        balance = user_ac_update.get('balance')
        stock = stock_update[symbol]

        if not share:
            return {"Failed to fetch share data": "share data not found"}

        if request.method == 'POST':
            quantity = int(request.form['quantity'])
            max_quantity_avai_to_buy = balance//price_per_share

            if quantity <= max_quantity_avai_to_buy:
                max_quantity_avai_to_buy -= quantity
                share['available_shares'] -= quantity
                user_ac_update['balance'] = balance - quantity*price_per_share
                stock_update[symbol] = stock + quantity
                update_user_stock_data(user_stock)
                update_user_details_data(user_data)
                update_shares_data(shares_data)
                return share, user_ac_update['balance']
            elif quantity > max_quantity_avai_to_buy:
                return share, balance

        return share, balance

api.add_resource(BuyShare, '/buy/share/<symbol>')

@app.route('/buy/<symbol>', methods=['GET', 'POST'])
def buy(symbol):
    #u_id = session['user_id']
    data, balance = BuyShare().post(symbol)
    #print(data)
    return render_template('buy.html', share=data, balance = balance )


class SellShare(Resource):
    def post(self, symbol):
        share = None
        u_id = session['user_id']
        for s in shares_data:
            if s['symbol'] == symbol:
                share = s
                break
        #print(user_data)
        price_per_share= share.get('price')
        stock_update = user_stock.get(u_id)
        #print(stock_update)
        user_ac_update = user_data.get(u_id)
        balance = user_ac_update.get('balance')
        stock = stock_update[symbol]
        if not share:
            return {"Failed to fetch share data": "share data not found"}
        if request.method == 'POST':
        
            quantity = int(request.form['quantity'])
            print(f'quantity: {quantity}')
            max_quantity_avai_to_sell = stock_update[symbol]

            if quantity <= max_quantity_avai_to_sell:
                max_quantity_avai_to_sell -= quantity
                share['available_shares'] += quantity
                user_ac_update['balance'] = balance + quantity*price_per_share
                stock_update[symbol] -= quantity

                update_user_stock_data(user_stock)
                update_user_details_data(user_data)
                update_shares_data(shares_data)
                return share, stock_update[symbol]
            elif quantity > max_quantity_avai_to_sell:
                print("Doesn't have enough shares to sell")
                return share, stock_update[symbol]
            
        return share, stock_update[symbol]

api.add_resource(SellShare)

# Define a route to display the sell form
@app.route('/sell/<symbol>', methods=['GET', 'POST'])
def sell(symbol):
    share, updated_share_count = SellShare().post(symbol)
    return render_template('sell.html', share=share, shares_available = updated_share_count, company_name= share['company_name'] )

#Thus rest api is used by deploying the CorConvRS restapi
class GetExchangeRate(Resource):
    def get(self,currency_rate = 1.0):

        if request.method == 'POST':
            current_currency = request.form['currency']
            desired_currency = request.form['des_currency']
            params = {"fromCur": current_currency, "toCur": desired_currency}
            url = 'http://localhost:8080/CurConvRS/webresources/exchangeRate'
            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.text
            else:
                data = None
            currency_rate, date_time = data.split(' @ ')
            all_data = {"currency_rate":currency_rate, "current_currency":current_currency, "desired_currency":desired_currency}
            return all_data
            #return currency_rate

api.add_resource(GetExchangeRate, '/exchange_rates/local')


class GetUpToDateExchangeRate(Resource):
    def get(self,currency_rate = 1.0):

        if request.method == 'POST':
            current_currency = request.form['currency']
            desired_currency = request.form['des_currency']
            url = "https://twelve-data1.p.rapidapi.com/currency_conversion"
            amount = 1 #put any value here

            symbol = current_currency + '/' + desired_currency

            querystring = {"symbol":symbol,"amount":amount}

            headers = {
                "X-RapidAPI-Key": "5b5f538fe3mshc980d6a97f3313dp13c6adjsn0307bacc58b4",
                "X-RapidAPI-Host": "twelve-data1.p.rapidapi.com"
            }

            response = requests.request("GET", url, headers=headers, params=querystring)        
            currency_rate = response.json().get('rate')
            return currency_rate

api.add_resource(GetUpToDateExchangeRate, '/exchange_rates/web')
        


@app.route('/exchange_rates', methods=['GET', 'POST'])
def exchange_rate():
    data = GetExchangeRate().get()
    print(data)
    
    if data==None:
         currency = "USD"
         des_currency = "GDB"
         exchange_rate = 1
    else:
        exchange_rate = data["currency_rate"]
        currency = data["current_currency"]
        des_currency = data["desired_currency"]
    
    
    exchange_rate_realtime = GetUpToDateExchangeRate().get()
    return render_template('curConv.html', exchange_rate=exchange_rate,
    exchange_rate_realtime= exchange_rate_realtime , u_id = session['user_id'],
    currency = currency, des_currency =des_currency)
    
    
if __name__ == '__main__':
    app.run(debug= True)
