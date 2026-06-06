#MAIN Làm 3 việc
#1.Gọi API thời tiết để lấy dữ liệu
#2.Xử lí data json trả về
#3.Lưu vào bảng weather trong PostgreSQL

import requests #thư viện giúp gọi API
import os
from dotenv import load_dotenv
from db import get_engine
from sqlalchemy import text

def save_weather(city, temp, humidity, description):
    engine = get_engine()
    #text : Bọc câu SQL thành object mà SQLAlchemy 2.0 hiểu được,
    #nếu không có text thì nó sẽ hiểu là string bình thường
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO weather (city, temperature, humidity, description)
            VALUES (:city, :temp, :humidity, :description)
        """), {
            "city": city,
            "temp": temp,
            "humidity": humidity,
            "description": description
        })
        conn.commit()
    print("Đã lưu vào database!")
#execute(tham số 1, tham số 2) → thực thi câu SQL đã chuẩn bị
if __name__ == "__main__":
    load_dotenv()

    api_key = os.getenv('API_KEY')
    city = input("Nhập tên thành phố (tiếng Anh): ").title()

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&lang=vi"
    #q → tên thành phố
    #appid → API key để xác thực
    #lang=vi → trả về mô tả thời tiết bằng tiếng Việt

    response = requests.get(url) #gửi yêu cầu đến API và nhận phản hồi
    data = response.json() #chuyển đổi phản hồi từ API (định dạng JSON) thành một đối tượng Python (thường là dict hoặc list) để dễ dàng truy cập và xử lý dữ liệu.

    if data.get('cod') == '404': 
        #404: không tìm thấy thành phố
        #200: tìm thấy
        #401: API key sai
        #429 : gọi quá nhiểu request
        print("Không tìm thấy thành phố. Vui lòng thử lại.")
    else:
        city = data['name']
        temp = round(data['main']['temp'] - 273.15, 1) #đổi từ Kelvin sang Celsius
        humidity = data['main']['humidity']
        description = data['weather'][0]['description']

        print(f"Thành phố: {city}")
        print(f"Nhiệt độ: {temp:.1f}°C")
        print(f"Độ ẩm: {humidity}%")
        print(f"Mô tả: {description}")
        save_weather(city, temp, humidity, description)