import requests
import smtplib

STOCK_NAME = "TSLA" # Use any stock name
COMPANY_NAME = "Tesla Inc" # Use the company name of above stock name

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "" # Use API key from "https://www.alphavantage.co/query"
NEWS_API_KEY = "" # Use API key from "https://newsapi.org/v2/everything"

stock_api_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

response = requests.get(STOCK_ENDPOINT, params=stock_api_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = float(yesterday_data["4. close"])

#Get the day before yesterday's closing stock price

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = float(day_before_yesterday_data["4. close"])

difference = abs(yesterday_closing_price - day_before_yesterday_closing_price)

#Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.

diff_percent = (difference / yesterday_closing_price) * 100

if diff_percent > 5:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": STOCK_NAME
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    three_articles = articles[:3]

    formatted_articles = [f"Headline:\n{article['title']}.\n\nBrief:\n{article['description']}" for article in three_articles]
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login("sahilkapoortest@gmail.com", "Apptest@123")
        for article in formatted_articles:
            message = f"Subject: Stock Alert\n\n{article}".encode('utf-8')
            connection.sendmail(
                from_addr="sahilkapoortest@gmail.com",
                to_addrs="sahilkapoortest@yahoo.com",
                msg=message
            )

