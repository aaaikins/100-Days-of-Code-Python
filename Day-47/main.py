import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import requests


def get_price(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for HTTP errors
        content = response.text
        soup = BeautifulSoup(content, "html.parser")
        price_tag = soup.find(name="span", class_="aok-offscreen")
        price = price_tag.getText()
        price_as_float = float(price.replace("$", "").replace(",", ""))
        return price_as_float, soup
    except Exception as e:
        print(f"Error fetching price: {e}")
        return None, None


def send_email(to_email: str, message: str):
    from_email = os.getenv('FROM_EMAIL')
    password = os.getenv('EMAIL_PASSWORD')

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "Amazon Price Alert"

    body = f'Hey, \n\n{message}'
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")


def main():
    URL = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }

    BUY_PRICE = 100
    price_as_float, soup = get_price(URL, headers)

    if price_as_float and price_as_float < BUY_PRICE:
        title = soup.find(id="productTitle").get_text().strip()
        message = f"{title} is on sale for ${price_as_float}!"
        send_email("achaikins@gmail.com", message)

if __name__ == "__main__":
    main()
