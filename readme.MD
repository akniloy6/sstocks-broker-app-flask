This project demonstrates the basic functionality of Flask and Flask rest API to
create a stocks broking service. It is a standalone light weight app which runs on the browser. 

An html web page based gui has been developed along with flask REST-api’s to fetch data from the database to create the share broking service. A static database has been used for this project which consists of 3 JSON files: stocks_broker.json, user_details.json and user_stocks.json. The stocks_broker.json file holds company details the user_details.josn holds user information and the user_stocks.json file holds which user has what amount of shares in each company. 

The web app works by requesting data in the broser through html templates and the api end points fetching these data using flask’s rest api’s developed for the purpose. Initially, a login page is setup which can be only be accessed using the right combo of user_id and password. 

After successful login, a user is shown the user page. This page fetches data from user_details.json for a particular user. There are two links on this page, one is to go directly to the share brokers market for buying or selling share, other one is the money exchange rate page where the user can see the exchange rates for different currencies. 

# Buy & Sell
The share brokers market page shows company details with a buy and sell option. Each user has a fixed amount of money in his account. After clicking the buy button he is routed to a page where he can buy that company’s share. Once submitted the amount of shares a user wants to buy, the api checks the user’s balance and determines whether if he has enough money to buy these shares. If balance is sufficient, the purchase is complete, and the api updates the json files accordingly.
If a user wants to sell a particular company’s share, he can click on the sell button and he will be routed to a landing page. The sell api checks whether he has shares which is sellable, and update the database accordingly. 

# Search 
The search function can be called upon by clicking on the search button on the market’s page. There are two search criteria: search by highest price or search by company symbol. If clicked by highest_price a list of companies with maximum to minimum share prices are shown in order. If searched by a company symbol, the details of that company is fetched and shown. 

# Integrating Currency conversion rate
The currency conversion rate service has been integrated in the web app in the /exchange route. Once the user goes to this link, he is opted for 2 inputs: the currency he wants to convert and the currency which he wants to convert into. For example: USD to GBP. Once submitted, the web app fetches data using 2 rest apis. The local currency converter, which has been provided in the module called CurConvRS, has been deployed. This shows conversion values which was predetermined within the api. This api is written in java. By consuming this api from the following link after deployment, the desired outcome was found.  http://localhost:8080/CurConvRS/webresources/exchangeRate. 

# Using External REST API

Another rest api from a public api provider rapidApi has been used to get real time exchange rates. This api was provided by tweleve data which returns real time exchange rates of currencies from the web by consuming it, that is,  when requested using the get method from the following url provided by the website: “https://twelve-data1.p.rapidapi.com/currency_conversion”.


Top Level Diagram of the project

![alt text](https://github.com/akniloy6/stocks-broker-app-flask/blob/main/top level.drawio.png?raw=true)



Run the following commands to get the project up & running:

pip install -r requirements.txt
python app.py
......
Runs on python 3.7
For the share Exchange api to work please deploy CurConvRS before running app.py
login with user: admin123 pass: admin321"# stocks-broker-app-flask" 
