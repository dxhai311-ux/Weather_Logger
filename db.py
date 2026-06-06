import os #lấy dữ liệu từ file .env
from dotenv import load_dotenv #đọc dữ liệu từ file .env
from sqlalchemy import create_engine, text #thư viện giúp kết nối với database

load_dotenv() #đọc file .env

def get_engine():
    #lấy dữ liệu từ file .env
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    database = os.getenv('DB_NAME')

    #tạo kết nối với database
    engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}/{database}")
    #postgresql  → loại database là PostgreSQL
    #psycopg2    → driver để Python nói chuyện với PostgreSQL
    #localhost   → địa chỉ máy chạy PostgreSQL
    #weather_logger → tên database trong PostgreSQL
    return engine

def create_table():
    engine = get_engine() #B1: kết nối với database
    #B2: tạo bảng nếu chưa tồn tại
    with engine.connect() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS weather (
                id SERIAL PRIMARY KEY,
                city VARCHAR(100),
                temperature FLOAT,
                humidity INT,
                description VARCHAR(200),
                recorded_at TIMESTAMP DEFAULT NOW()
            )
        """))
        connection.commit() #B3: lưu thay đổi vào database
        print('Bảng weather đã sãn sàng!') #để dễ debug
#PostgreSQL hoạt động theo transaction — tức là mọi thay đổi được giữ tạm thời, chưa lưu thật sự cho đến khi commit.
if __name__ == "__main__":
    create_table()
#====Chi tiết===
#CREATE TABLE → tạo bảng mới
#IF NOT EXISTS → nếu bảng đã có rồi thì bỏ qua, không báo lỗi
#weather → tên bảng

#id → tên cột
#SERIAL → tự động tăng: 1, 2, 3, 4...
#PRIMARY KEY → mỗi dòng có id duy nhất, không được trùng

#recorded_at → tên cột
#TIMESTAMP → lưu ngày + giờ
#DEFAULT NOW() → tự động điền thời gian hiện tại