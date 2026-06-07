#MAIN Làm 3 việc
#1.Gọi API thời tiết để lấy dữ liệu
#2.Xử lí data json trả về
#3.Lưu vào bảng weather trong PostgreSQL

import requests #thư viện giúp gọi API
import os
from dotenv import load_dotenv
from db import get_engine
from sqlalchemy import text

engine = get_engine()
load_dotenv()

def save_weather(city, temp, humidity, description):
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
    api_key = os.getenv('API_KEY')
    city = input("Nhập tên thành phố (tiếng Anh): ").title()

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&lang=vi"
    #q → tên thành phố
    #appid → API key để xác thực
    #lang=vi → trả về mô tả thời tiết bằng tiếng Việt

    try:
        response = requests.get(url)
        response.raise_for_status() #nếu có lỗi HTTP sẽ ném ra exception, và chúng ta sẽ bắt nó trong except
        data = response.json() #chuyển dữ liệu JSON thành dict của Python
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi gọi API: {e}")
        exit()

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

#====Cấu trúc====
#Tạo engine : Lúc này Python chưa kết nối thật — chỉ tạo ra "bản đồ" biết database ở đâu.
#engine.connect() : Mở kết nối thật sự với database, giống như mở cửa vào nhà.
#conn.execute() : Python gửi câu SQL qua kết nối → PostgreSQL nhận → xử lý → thêm data vào bảng.
#conn.commit() : PostgreSQL lưu data thật sự vào ổ cứng.