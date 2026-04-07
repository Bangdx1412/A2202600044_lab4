# KẾT QUẢ TEST CASES — TravelBuddy Agent

---

## Test 1 — Câu hỏi mở, chưa có thông tin

**Mục tiêu:** Kiểm tra khả năng dẫn dắt hội thoại khi người dùng chưa cung cấp thông tin.

**Tool được gọi:** Không có (Agent trả lời trực tiếp)

**Lý do không gọi tool:** Chưa đủ thông tin (điểm đi, điểm đến, ngân sách) để tra cứu.

```
Bạn: xin chào ! tôi muốn đi du lịch nhưng chưa biết đi đâu

TravelBuddy đang suy nghĩ...
--- 💬 Agent trả lời trực tiếp

TravelBuddy: Chào bạn! Rất vui được giúp bạn lên kế hoạch cho chuyến đi sắp tới.
Việt Nam mình có nhiều địa điểm đẹp lắm. Để TravelBuddy gợi ý cho bạn những nơi
phù hợp nhất, bạn có thể cho mình biết một chút về:

1. Ngân sách dự kiến của bạn là khoảng bao nhiêu?
2. Bạn muốn đi du lịch trong khoảng thời gian nào?
3. Bạn thích kiểu du lịch như thế nào? (biển, núi, thành phố...)
```

**Nhận xét:** Agent không gọi tool khi chưa đủ thông tin — đúng behavior. Hỏi lại đúng 3 thông tin cốt lõi cần thiết.

---

## Test 2 — Tìm kiếm chuyến bay đơn giản

**Mục tiêu:** Kiểm tra tool `search_flights` hoạt động đúng với route cơ bản.

**Tool được gọi:**
```
--- 🛠️ Agent gọi tool: search_flights({'destination': 'Đà Nẵng', 'origin': 'Hà Nội'})
```

**Lý do gọi tool:** Người dùng cung cấp đủ điểm đi + điểm đến → agent tra cứu ngay, không hỏi lại.

```
Bạn: Tìm giúp tôi chuyến hà nội đi đà nẵng

TravelBuddy đang suy nghĩ...
--- 🛠️ Agent gọi tool: search_flights({'destination': 'Đà Nẵng', 'origin': 'Hà Nội'})
--- 💬 Agent trả lời trực tiếp

TravelBuddy: Tuyệt vời! TravelBuddy đã tìm thấy một số chuyến bay từ Hà Nội đi Đà Nẵng:

- Vietnam Airlines (hạng phổ thông): 06:00 - 07:20, giá 1.450.000đ
- Vietnam Airlines (hạng thương gia): 14:00 - 15:20, giá 2.800.000đ
- VietJet Air (hạng phổ thông): 08:30 - 09:50, giá 890.000đ
- Bamboo Airways (hạng phổ thông): 11:00 - 12:20, giá 1.200.000đ
```

**Nhận xét:** `search_flights` trả về đúng 4 chuyến bay có trong mock data. Agent trình bày rõ ràng, hỏi thêm ngân sách để tư vấn tiếp.

---

## Test 3 — Multi-step tool chaining (tư vấn trọn gói)

**Mục tiêu:** Kiểm tra khả năng gọi nhiều tool liên tiếp, sử dụng kết quả tool trước để quyết định tham số tool sau.

**Tool được gọi (theo thứ tự):**
```
--- 🛠️ Agent gọi tool: search_flights({'origin': 'Hà Nội', 'destination': 'Phú Quốc'})
--- 🛠️ Agent gọi tool: calculate_budget({'total_budget': 5000000, 'expenses': 'vé_máy_bay:2200000, khách_sạn:1600000'})
--- 🛠️ Agent gọi tool: search_hotels({'city': 'Phú Quốc', 'max_price_per_night': 1400000})
```

**Chuỗi suy luận của Agent:**
1. `search_flights` → Tìm vé rẻ nhất: VietJet Air 1.100.000đ/chiều → khứ hồi 2.200.000đ
2. `calculate_budget` → Ngân sách còn lại: 5.000.000 - 2.200.000 = 2.800.000đ → tối đa 1.400.000đ/đêm
3. `search_hotels` → Lọc khách sạn Phú Quốc ≤ 1.400.000đ/đêm

```
Bạn: Tôi ở hà nội, muốn đi phú quốc 2 đêm, budget 5 triệu, tư vấn giúp tôi

TravelBuddy đang suy nghĩ...
--- 🛠️ Agent gọi tool: search_flights({'origin': 'Hà Nội', 'destination': 'Phú Quốc'})
--- 🛠️ Agent gọi tool: calculate_budget({'total_budget': 5000000, 'expenses': 'vé_máy_bay:2200000, khách_sạn:1600000'})
--- 🛠️ Agent gọi tool: search_hotels({'city': 'Phú Quốc', 'max_price_per_night': 1400000})
--- 💬 Agent trả lời trực tiếp

TravelBuddy:

Chuyến bay:
VietJet Air (economy): 16:00 - 18:15, giá 1.100.000đ/chiều → khứ hồi 2.200.000đ

Khách sạn:
- Lahana Resort (3 sao): 800.000đ/đêm, Dương Đông, rating 4.0
- 9Station Hostel (2 sao): 200.000đ/đêm, Dương Đông, rating 4.5

Tổng chi phí ước tính (VietJet + Lahana Resort):
- Vé máy bay: 2.200.000đ
- Khách sạn (2 đêm): 1.600.000đ
- Tổng chi: 3.800.000đ
- Ngân sách còn lại: 1.200.000đ

Gợi ý thêm:
Với 1.200.000đ còn lại, bạn có thể thưởng thức hải sản chợ đêm Dinh Cậu,
đi cáp treo Hòn Thơm, hoặc thuê xe máy khám phá Bãi Sao, Bãi Khem.
```

**Nhận xét:** Agent thực hiện đúng 3-bước tool chaining. Biết dùng kết quả `search_flights` để tính ngân sách còn lại, rồi dùng ngân sách đó làm `max_price_per_night` cho `search_hotels`. Output đầy đủ 4 phần theo response_format.

---

## Test 4 — Yêu cầu ngoài khả năng (đặt phòng)

**Mục tiêu:** Kiểm tra constraint "không đặt phòng trực tiếp".

**Tool được gọi:** Không có

**Lý do không gọi tool:** Yêu cầu đặt phòng nằm ngoài scope của tool hiện có.

```
Bạn: Tôi muốn đặt khách sạn

TravelBuddy đang suy nghĩ...
--- 💬 Agent trả lời trực tiếp

TravelBuddy: À vâng, TravelBuddy rất sẵn lòng giúp bạn tìm kiếm khách sạn phù hợp.
Tuy nhiên, TravelBuddy chỉ có thể tìm kiếm thông tin về các khách sạn và gợi ý cho
bạn thôi, chứ không thể trực tiếp đặt phòng giúp bạn được.

Bạn có thể truy cập Booking.com, Agoda, Traveloka... để đặt phòng nhé.
```

**Nhận xét:** Agent từ chối đúng, lịch sự, không hallucinate chức năng không có. Hướng dẫn user sang kênh phù hợp.

---

## Test 5 — Yêu cầu ngoài domain (lập trình)

**Mục tiêu:** Kiểm tra constraint "từ chối yêu cầu không liên quan đến du lịch".

**Tool được gọi:** Không có

**Lý do không gọi tool:** Yêu cầu lập trình Python hoàn toàn ngoài domain du lịch.

```
Bạn: Giải giúp tôi bài tập lập trình python về linked list

TravelBuddy đang suy nghĩ...
--- 💬 Agent trả lời trực tiếp

TravelBuddy: Chào bạn, TravelBuddy rất vui được trò chuyện với bạn. Tuy nhiên,
mình là trợ lý du lịch chuyên về các chuyến đi, đặt vé máy bay và khách sạn
ở Việt Nam thôi. Mình không thể giúp bạn giải bài tập lập trình Python được.

Nếu bạn có bất kỳ câu hỏi nào liên quan đến du lịch Việt Nam,
đừng ngần ngại hỏi mình nhé! 😊
```

**Nhận xét:** Agent từ chối đúng domain constraint trong system prompt. Thái độ lịch sự, kiên quyết, không bị "lách" bởi yêu cầu off-topic.

---

## Tổng kết

| Test | Nội dung | Tool gọi | Kết quả |
|------|----------|----------|---------|
| 1 | Câu hỏi mở | Không có | Hỏi lại đúng thông tin |
| 2 | Tìm vé máy bay | `search_flights` | Trả đủ 4 chuyến bay |
| 3 | Tư vấn trọn gói có budget | `search_flights` → `calculate_budget` → `search_hotels` | Multi-step chaining thành công |
| 4 | Đặt khách sạn | Không có | Từ chối đúng, hướng dẫn kênh khác |
| 5 | Bài tập lập trình | Không có | Từ chối đúng domain |