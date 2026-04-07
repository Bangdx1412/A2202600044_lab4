from langchain_core.tools import tool


FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1_450_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business"},
        {"airline": "VietJet Air", "departure": "08:30", "arrival": "09:50", "price": 890_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "11:00", "arrival": "12:20", "price": 1_200_000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1_350_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "18:15", "price": 1_100_000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1_600_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "07:30", "arrival": "09:40", "price": 950_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1_300_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_200_000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1_300_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780_000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "15:00", "arrival": "16:00", "price": 650_000, "class": "economy"},
    ],
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1_800_000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Sala Danang Beach", "stars": 4, "price_per_night": 1_200_000, "area": "Mỹ Khê", "rating": 4.3},
        {"name": "Fivitel Danang", "stars": 3, "price_per_night": 650_000, "area": "Sơn Trà", "rating": 4.1},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 250_000, "area": "Hải Châu", "rating": 4.6},
        {"name": "Christina's Homestay", "stars": 2, "price_per_night": 350_000, "area": "An Thượng", "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3_500_000, "area": "Bãi Dài", "rating": 4.4},
        {"name": "Sol by Meliá", "stars": 4, "price_per_night": 1_500_000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort", "stars": 3, "price_per_night": 800_000, "area": "Dương Đông", "rating": 4.0},
        {"name": "9Station Hostel", "stars": 2, "price_per_night": 200_000, "area": "Dương Đông", "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "stars": 5, "price_per_night": 2_800_000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1_400_000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 550_000, "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room", "stars": 2, "price_per_night": 180_000, "area": "Quận 1", "rating": 4.6},
    ],
}

# Hàm hỗ trợ format tiền tệ (1.450.000đ)
def format_currency(amount):
    return f"{amount:,.0f}".replace(",", ".") + "đ"

@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố. Trả về danh sách chuyến bay hoặc thông báo lỗi.
    """
    # 1. Thử tra chiều xuôi
    flights = FLIGHTS_DB.get((origin, destination))
    
    # 2. Nếu không thấy, thử tra ngược chiều (theo yêu cầu đề bài)
    if not flights:
        flights = FLIGHTS_DB.get((destination, origin))
    
    if not flights:
        return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."

    # 3. Format danh sách dễ đọc
    result = [f"Chuyến bay từ {origin} đến {destination}:"]
    for f in flights:
        price_str = format_currency(f['price'])
        result.append(f"- {f['airline']} ({f['class']}): {f['departure']}-{f['arrival']}, Giá: {price_str}")
    
    return "\n".join(result)

@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có lọc theo giá tối đa và sắp xếp theo rating.
    """
    hotels = HOTELS_DB.get(city, [])
    
    # 1. Lọc theo giá
    filtered_hotels = [h for h in hotels if h['price_per_night'] <= max_price_per_night]
    
    if not filtered_hotels:
        return f"Không tìm thấy khách sạn tại {city} với giá dưới {format_currency(max_price_per_night)}. Hãy thử tăng ngân sách."

    # 2. Sắp xếp theo rating giảm dần (ưu tiên khách sạn tốt nhất)
    sorted_hotels = sorted(filtered_hotels, key=lambda x: x['rating'], reverse=True)

    # 3. Format kết quả
    result = [f"Danh sách khách sạn tại {city} (Giá < {format_currency(max_price_per_night)}):"]
    for h in sorted_hotels:
        price_str = format_currency(h['price_per_night'])
        result.append(f"- {h['name']} ({h['stars']}*): {price_str}/đêm, Khu vực: {h['area']}, Rating: {h['rating']}")
    
    return "\n".join(result)

@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại. 
    expenses định dạng: 'tên_khoản:số_tiền, tên_khoản:số_tiền'
    """
    try:
        # 1. Parse chuỗi expenses thành dict
        # Ví dụ: "vé_máy_bay:890000, khách_sạn:650000"
        expense_items = {}
        parts = expenses.split(",")
        for p in parts:
            name, price = p.split(":")
            expense_items[name.strip()] = int(price.strip())
        
        # 2. Tính toán
        total_expense = sum(expense_items.values())
        remaining = total_budget - total_expense
        
        # 3. Format bảng chi tiết
        lines = ["Bảng chi phí:"]
        for name, price in expense_items.items():
            lines.append(f"- {name.replace('_', ' ').capitalize()}: {format_currency(price)}")
        
        lines.append("-" * 20)
        lines.append(f"Tổng chi: {format_currency(total_expense)}")
        lines.append(f"Ngân sách: {format_currency(total_budget)}")
        lines.append(f"Còn lại: {format_currency(remaining)}")
        
        # 4. Cảnh báo nếu vượt ngân sách
        if remaining < 0:
            lines.append(f"⚠️ Vượt ngân sách {format_currency(abs(remaining))}! Cần điều chỉnh.")
            
        return "\n".join(lines)
        
    except Exception:
        return "Lỗi: Định dạng chuỗi expenses sai. Vui lòng dùng 'tên:số_tiền, tên:số_tiền'."
