from langchain_core.tools import tool

# =============================================================================
# MOCK DATA
# =============================================================================

FLIGHTS_DB = {
    # Tuyến Hà Nội <-> Đà Nẵng
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1_450_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business"},
        {"airline": "VietJet Air", "departure": "08:30", "arrival": "09:50", "price": 890_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "21:00", "arrival": "22:20", "price": 650_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "11:00", "arrival": "12:20", "price": 1_200_000, "class": "economy"},
        {"airline": "Vietravel Airlines", "departure": "16:30", "arrival": "17:50", "price": 950_000, "class": "economy"},
    ],
    # Tuyến Hà Nội <-> Phú Quốc
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2_100_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "13:00", "arrival": "15:15", "price": 4_500_000, "class": "business"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1_350_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "18:15", "price": 1_100_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "09:30", "arrival": "11:45", "price": 1_850_000, "class": "economy"},
    ],
    # Tuyến Hà Nội <-> Hồ Chí Minh
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1_600_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "10:00", "arrival": "12:10", "price": 1_800_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_200_000, "class": "business"},
        {"airline": "VietJet Air", "departure": "07:30", "arrival": "09:40", "price": 950_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "22:30", "arrival": "00:40", "price": 750_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1_300_000, "class": "economy"},
        {"airline": "Vietravel Airlines", "departure": "15:00", "arrival": "17:10", "price": 1_150_000, "class": "economy"},
    ],
    # Tuyến Hà Nội <-> Nha Trang
    ("Hà Nội", "Nha Trang"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:50", "price": 1_950_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "11:15", "arrival": "13:05", "price": 1_250_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "14:30", "arrival": "16:20", "price": 1_600_000, "class": "economy"},
    ],
    # Tuyến Hà Nội <-> Đà Lạt
    ("Hà Nội", "Đà Lạt"): [
        {"airline": "Vietnam Airlines", "departure": "07:30", "arrival": "09:20", "price": 2_050_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:50", "price": 1_400_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "09:00", "arrival": "10:50", "price": 1_750_000, "class": "economy"},
    ],
    # Tuyến Hồ Chí Minh <-> Đà Nẵng
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1_300_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "16:00", "arrival": "17:20", "price": 2_500_000, "class": "business"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "20:00", "arrival": "21:20", "price": 550_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "07:00", "arrival": "08:20", "price": 990_000, "class": "economy"},
    ],
    # Tuyến Hồ Chí Minh <-> Phú Quốc
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:00", "price": 1_250_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "11:00", "arrival": "12:00", "price": 750_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "15:00", "arrival": "16:00", "price": 650_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "10:00", "arrival": "11:00", "price": 950_000, "class": "economy"},
    ],
    # Tuyến Hồ Chí Minh <-> Nha Trang
    ("Hồ Chí Minh", "Nha Trang"): [
        {"airline": "Vietnam Airlines", "departure": "10:30", "arrival": "11:40", "price": 1_050_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "14:00", "arrival": "15:10", "price": 590_000, "class": "economy"},
    ],
    # Tuyến Hồ Chí Minh <-> Đà Lạt
    ("Hồ Chí Minh", "Đà Lạt"): [
        {"airline": "Vietnam Airlines", "departure": "06:30", "arrival": "07:30", "price": 950_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "12:00", "arrival": "13:00", "price": 490_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "17:30", "arrival": "18:30", "price": 550_000, "class": "economy"},
    ]
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "InterContinental Danang Sun Peninsula", "stars": 5, "price_per_night": 9_500_000, "area": "Bán đảo Sơn Trà", "rating": 4.9},
        {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1_800_000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Novotel Danang Premier", "stars": 5, "price_per_night": 2_200_000, "area": "Hải Châu", "rating": 4.6},
        {"name": "Sala Danang Beach", "stars": 4, "price_per_night": 1_200_000, "area": "Mỹ Khê", "rating": 4.3},
        {"name": "A La Carte Da Nang Beach", "stars": 4, "price_per_night": 1_500_000, "area": "Phước Mỹ", "rating": 4.4},
        {"name": "Fivitel Danang", "stars": 3, "price_per_night": 650_000, "area": "Sơn Trà", "rating": 4.1},
        {"name": "Avora Hotel", "stars": 3, "price_per_night": 750_000, "area": "Hải Châu", "rating": 4.2},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 250_000, "area": "Hải Châu", "rating": 4.6},
        {"name": "Christina's Homestay", "stars": 2, "price_per_night": 350_000, "area": "An Thượng", "rating": 4.7},
        {"name": "Rom Casa Hostel", "stars": 2, "price_per_night": 200_000, "area": "Ngũ Hành Sơn", "rating": 4.5},
    ],
    "Phú Quốc": [
        {"name": "JW Marriott Phu Quoc", "stars": 5, "price_per_night": 7_500_000, "area": "Bãi Khem", "rating": 4.9},
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3_500_000, "area": "Bãi Dài", "rating": 4.6},
        {"name": "Seashells Phu Quoc", "stars": 5, "price_per_night": 2_400_000, "area": "Dương Đông", "rating": 4.5},
        {"name": "Sol by Meliá", "stars": 4, "price_per_night": 1_500_000, "area": "Bãi Trường", "rating": 4.4},
        {"name": "Ocean Pearl Hotel", "stars": 4, "price_per_night": 1_100_000, "area": "Dương Đông", "rating": 4.1},
        {"name": "Lahana Resort", "stars": 3, "price_per_night": 800_000, "area": "Dương Đông", "rating": 4.2},
        {"name": "Miana Resort", "stars": 3, "price_per_night": 650_000, "area": "Trần Hưng Đạo", "rating": 4.3},
        {"name": "9Station Hostel", "stars": 2, "price_per_night": 200_000, "area": "Dương Đông", "rating": 4.5},
        {"name": "The Birdhouse", "stars": 2, "price_per_night": 300_000, "area": "Ông Lang", "rating": 4.6},
    ],
    "Hồ Chí Minh": [
        {"name": "Park Hyatt Saigon", "stars": 5, "price_per_night": 6_500_000, "area": "Quận 1", "rating": 4.8},
        {"name": "Rex Hotel", "stars": 5, "price_per_night": 2_800_000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1_400_000, "area": "Quận 1", "rating": 4.1},
        {"name": "Fusion Suites Saigon", "stars": 4, "price_per_night": 1_900_000, "area": "Quận 1", "rating": 4.5},
        {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 550_000, "area": "Quận 3", "rating": 4.4},
        {"name": "Wink Hotel", "stars": 3, "price_per_night": 850_000, "area": "Quận 1", "rating": 4.6},
        {"name": "The Common Room", "stars": 2, "price_per_night": 180_000, "area": "Quận 5", "rating": 4.6},
        {"name": "Kiki's House", "stars": 2, "price_per_night": 250_000, "area": "Quận 1", "rating": 4.2},
    ],
    "Hà Nội": [
        {"name": "Sofitel Legend Metropole", "stars": 5, "price_per_night": 8_000_000, "area": "Hoàn Kiếm", "rating": 4.9},
        {"name": "Lotte Hotel Hanoi", "stars": 5, "price_per_night": 3_200_000, "area": "Ba Đình", "rating": 4.7},
        {"name": "Hanoi La Siesta Hotel", "stars": 4, "price_per_night": 1_600_000, "area": "Hoàn Kiếm", "rating": 4.8},
        {"name": "The Light Hotel", "stars": 4, "price_per_night": 1_100_000, "area": "Hoàn Kiếm", "rating": 4.3},
        {"name": "Hanoi Boutique Hotel", "stars": 3, "price_per_night": 750_000, "area": "Phố Cổ", "rating": 4.4},
        {"name": "Old Quarter View", "stars": 3, "price_per_night": 600_000, "area": "Phố Cổ", "rating": 4.5},
        {"name": "Little Charm Hanoi Hostel", "stars": 2, "price_per_night": 200_000, "area": "Hoàn Kiếm", "rating": 4.6},
        {"name": "Hanoi Central Backpackers", "stars": 2, "price_per_night": 150_000, "area": "Hoàn Kiếm", "rating": 4.3},
    ],
    "Nha Trang": [
        {"name": "Vinpearl Luxury", "stars": 5, "price_per_night": 5_500_000, "area": "Đảo Hòn Tre", "rating": 4.8},
        {"name": "InterContinental Nha Trang", "stars": 5, "price_per_night": 3_500_000, "area": "Lộc Thọ", "rating": 4.7},
        {"name": "Novotel Nha Trang", "stars": 4, "price_per_night": 1_800_000, "area": "Lộc Thọ", "rating": 4.5},
        {"name": "Aaron Hotel", "stars": 3, "price_per_night": 650_000, "area": "Lộc Thọ", "rating": 4.2},
        {"name": "Mojzo Inn", "stars": 2, "price_per_night": 300_000, "area": "Tân Lập", "rating": 4.7},
    ],
    "Đà Lạt": [
        {"name": "Dalat Palace Heritage", "stars": 5, "price_per_night": 4_200_000, "area": "Phường 3", "rating": 4.6},
        {"name": "Ana Mandara Villas", "stars": 5, "price_per_night": 3_100_000, "area": "Phường 5", "rating": 4.5},
        {"name": "Colline Hotel", "stars": 4, "price_per_night": 1_500_000, "area": "Phường 1", "rating": 4.4},
        {"name": "Golf Valley Hotel", "stars": 4, "price_per_night": 1_350_000, "area": "Phường 2", "rating": 4.3},
        {"name": "Tigôn Dalat Hostel", "stars": 2, "price_per_night": 180_000, "area": "Phường 3", "rating": 4.6},
        {"name": "The Seen House", "stars": 2, "price_per_night": 400_000, "area": "Hồ Tuyền Lâm", "rating": 4.7},
    ]
}

# =============================================================================
# TOOLS IMPLEMENTATION
# =============================================================================

@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố.
    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
    - destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')
    """
    # Thử tra cứu chiều đi
    flights = FLIGHTS_DB.get((origin, destination))
    
    # Thử tra ngược nếu không có chiều đi
    if not flights:
        flights = FLIGHTS_DB.get((destination, origin))
        
    if not flights:
        return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."

    # Sắp xếp chuyến bay theo giá (tăng dần) và lấy 5 kết quả đầu tiên
    top_5_flights = sorted(flights, key=lambda x: x["price"])[:5]

    result = [f"Danh sách 5 chuyến bay giá tốt nhất giữa {origin} và {destination}:"]
    for f in top_5_flights:
        price_formatted = f"{f['price']:,}".replace(",", ".")
        result.append(f"- {f['airline']} ({f['class']}): Khởi hành {f['departure']} - Đến {f['arrival']} | Giá: {price_formatted}₫")
    
    return "\n".join(result)


@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.
    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - max_price_per_night: giá tối đa mỗi đêm (VNĐ), mặc định không giới hạn
    """
    hotels = HOTELS_DB.get(city)
    if not hotels:
        return f"Không tìm thấy dữ liệu khách sạn tại {city}."
    
    # Lọc theo giá
    filtered_hotels = [h for h in hotels if h["price_per_night"] <= max_price_per_night]
    
    if not filtered_hotels:
        price_formatted = f"{max_price_per_night:,}".replace(",", ".")
        return f"Không tìm thấy khách sạn tại {city} với giá dưới {price_formatted}₫/đêm. Hãy thử tăng ngân sách."
    
    # Sắp xếp theo rating giảm dần
    filtered_hotels.sort(key=lambda x: x["rating"], reverse=True)
    
    result = [f"Danh sách khách sạn tại {city} (Giá <= {f'{max_price_per_night:,}'.replace(',', '.')}₫/đêm):"]
    for h in filtered_hotels:
        price_formatted = f"{h['price_per_night']:,}".replace(",", ".")
        result.append(f"- {h['name']} ({h['stars']} sao) | Khu vực: {h['area']} | Rating: {h['rating']} | Giá: {price_formatted}₫/đêm")
        
    return "\n".join(result)


@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.
    Tham số:
    - total_budget: tổng ngân sách ban đầu (VNĐ)
    - expenses: chuỗi mô tả các khoản chi định dạng 'tên khoản: số tiền' (VD: 'vé máy bay: 890000, khách sạn: 650000')
    """
    try:
        expense_dict = {}
        # Parse chuỗi expenses
        items = expenses.split(",")
        for item in items:
            name, amount = item.split(":")
            expense_dict[name.strip()] = int(amount.strip())
            
        total_expense = sum(expense_dict.values())
        remaining = total_budget - total_expense
        
        result = ["Bảng chi phí:"]
        for name, amount in expense_dict.items():
            result.append(f"- {name.capitalize()}: {f'{amount:,}'.replace(',', '.')}₫")
            
        result.append(f"Tổng chi: {f'{total_expense:,}'.replace(',', '.')}₫")
        result.append(f"Ngân sách: {f'{total_budget:,}'.replace(',', '.')}₫")
        
        if remaining >= 0:
            result.append(f"Còn lại: {f'{remaining:,}'.replace(',', '.')}₫")
        else:
            result.append(f"Vượt ngân sách {f'{abs(remaining):,}'.replace(',', '.')}₫! Cần điều chỉnh.")
            
        return "\n".join(result)
        
    except Exception as e:
        return f"Lỗi định dạng đầu vào chi phí. Vui lòng nhập đúng định dạng (VD: 'vé máy bay: 890000, khách sạn: 650000'). Lỗi: {str(e)}"