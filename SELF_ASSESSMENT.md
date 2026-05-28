# Tự Đánh Giá Chiến Lược Multi-MA Crossover trên VN30F1M

Em là **Trần Thanh Tùng**, hiện tại đang học tại University of Technology, Sydney chuyên ngành Computer Science (Honours) majors AI and Data Analytics. Trong bài reflection này em xin phép xưng là em.

---

## 1. Mô tả chiến lược

Ở trong bài test lần này, trading stratergy em sử dụng là **Multi-MA Crossover** áp dụng cho thị trường phái sinh **VN30F1M** trên khung thời gian **1 giờ (1H)**. Đây cũng là chiến lược em đã sử dụng song song với Fibonacci retracement để xác định các vùng vào lệnh (Entry zones: 0.5, 0.618, 0.786), vùng chốt lời (1.3, 1.6, 1.912) và quan trọng nhất là vùng cắt lỗi. Kết hợp cùng lý thuyết sóng Elliott để định vị sóng để double check lại xem đây là một con sóng điều chỉnh hay là sóng đẩy từ đó đưa ra quyết định vào lệnh hay không.

Nhưng ở bài này, vì khả năng code của em có hạn cũng như em không nghĩ với trading bot, mình nên gộp quá nhiều trading stratergy hay nhiều chỉ số đan xen với nhau. Nên ở đây, em chỉ để nguyên trading stratergy ở dạng thuần MA để giữ tính khách quan của giữ liệu. Logic cốt lõi của em dựa trên việc sắp xếp thứ tự của 4 đường trung bình động trên giá Close: **MA10, MA20, MA50, MA200** (bình thường trong thực chiến, em thường thêm MA5 và MA100 để có lớp tín hiệu sớm và một bộ filter trung hạn dày hơn, để dễ dàng vào lệnh).

**Điều kiện vào lệnh:**

- **Vào LONG (+1)**: khi cấu trúc bullish stack được xác lập: `MA10 > MA20 > MA50 > MA200`. Đây là trạng thái dòng tiền ngắn hạn, trung hạn và dài hạn đều đồng pha tăng.
- **Vào SHORT (–1)**: khi cấu trúc bearish stack hình thành: `MA10 < MA20 < MA50 < MA200`, tức cả ba khung thời gian đều đồng pha giảm.
- **Đứng ngoài (0)**: mọi trường hợp các MA không xếp thẳng hàng, thường tương ứng với giai đoạn sideway hoặc đảo chiều.

Vị thế này sẽ được giữ cho đến khi điều kiện stack bị phá vỡ, tức là chiến lược tự động đóng/đảo vị thế dựa trên cấu trúc MA chứ không dùng stop-loss hay take-profit cố định.

---

## 2. Các chỉ số đạt được

Kết quả khi em backtest trên dữ liệu từ **13/08/2018 đến 27/05/2026** (gần 8 năm) cho thấy chiến lược có hiệu suất ổn định cả ở giai đoạn historical lẫn out-of-sample, phản ánh không bị overfit:

| Chỉ số | Historical (after fees) | Out-of-sample (after fees) |
|---|---|---|
| Lợi nhuận hàng năm | 20.48% | 15.61% |
| Mức sụt giảm tối đa | –13.94% | –10.95% |
| Sharpe Ratio | 1.47 | 1.43 |

**Một số chỉ số chi tiết khác đáng lưu ý:**

- **Tỷ lệ thắng**: 48.18% (tuy dưới 50% nhưng vẫn cho kết quả dương nhờ profit factor và độ lớn lệnh thắng).
- **Hệ số lợi nhuận (Profit Factor)**: 1.34 → kỳ vọng dương rõ ràng.
- **Hệ số Sortino**: 2.22 → cao hơn Sharpe khá nhiều, cho thấy biến động phía downside được kiểm soát tốt hơn so với upside.
- **Hệ số Calmar**: 116.83 → rất tốt, phản ánh lợi nhuận/drawdown.
- **Xác suất phá sản**: 0.99% → thấp, cho thấy chiến lược có biên an toàn về dài hạn (đây cũng là thứ em luôn ưu tiên vì em muốn đầu tư không phải đầu cơ).
- **Lợi nhuận trung bình mỗi lệnh**: 1.12
- **Tổn thất trung bình**: 6.31 → chênh lệch lớn, đây là dấu hiệu cần lưu ý.
- **Độ biến động**: 12.47 → em đánh giá ở mức trung bình.

**Quan trọng**: sự chênh lệch giữa Sharpe in-sample (1.47) và out-of-sample (1.43) chỉ khoảng 0.04 → đây là tín hiệu rất tích cực cho thấy chiến lược **không bị curve-fitting**, hành vi của nó trên dữ liệu chưa từng thấy gần như giữ nguyên so với dữ liệu lịch sử huấn luyện.

---

## 3. Điểm mạnh

- **Tính nhất quán giữa các giai đoạn**: Đây là điểm em tự tin nhất cho trading stratergy này với việc lợi nhuận, drawdown và Sharpe giữa historical và out-of-sample gần như tương đương. Một chiến lược như vậy dễ tin cậy hơn nhiều so với những chiến lược có Sharpe in-sample > 3 nhưng out-of-sample colapse.

- **Logic đơn giản**: Không có tham số magic nào được tối ưu hậu nghiệm (với 4 đường MA 10/20/50/200 là chuẩn phương pháp cổ điển). Khi vào lệnh thực, em biết và hiểu chính xác tín hiệu đến từ đâu.

- **Đối xứng long/short**: Trên thị trường phái sinh Việt Nam, khả năng kiếm tiền cả ở chiều giảm là lợi thế lớn so với thị trường cơ sở. Chiến lược tận dụng được điều này thay vì chỉ đứng ngoài chờ uptrend.

- **Tích hợp tự nhiên với phân tích kỹ thuật khác**: Đây cũng là một ưu điểm rất lớn của MA Crossover. Bộ khung MA này dễ kết hợp với Fibonacci để định mục tiêu, và với Elliott để xác định vị trí trong sóng lớn.

---

## 4. Điểm yếu & rủi ro

- **Win rate dưới 50%**: Dù theo lý thuyết và backtest, chiến lược có kỳ vọng dương, nhưng việc win rate dưới 50% cũng là một đều rất đáng để cân nhắc.

- **Chênh lệch lớn giữa lợi nhuận trung bình (1.12) và tổn thất trung bình (–6.31)**: Đây cũng là một điểm yếu của việc sử dụng MA Crossover để giao dịch bởi tỷ lệ này phản ánh việc chiến lược chốt lời sớm khi cấu trúc MA vừa rạn nứt, trong khi lệnh thua chỉ thoát khi cấu trúc đảo chiều hoàn toàn, tức là con bot sẽ chấp nhận lệnh thua dài (chấp nhận gồng lỗ) hơn so với lệnh thắng. Lợi nhuận tổng thể phụ thuộc nhiều vào những con sóng lớn để bù lại nhiều lệnh thua nhỏ.

- **Hiệu suất kém trong thị trường sideway**: Khi giá quẩn quanh các đường MA, hiện tượng whipsaw xảy ra liên tục (vào lệnh rồi đảo ngược, bị cắt cả hai chiều). Quan sát đường equity ở các giai đoạn ngang giai đoạn 2022 cho thấy điều này.

- **Thiếu cơ chế stop-loss/take-profit chủ động**: Chiến lược chỉ thoát khi cấu trúc MA đảo, đồng nghĩa với việc một cú sốc thị trường (tin tức, gap) có thể sẽ làm mất lợi nhuận tích lũy trước khi tín hiệu xác nhận đảo chiều xuất hiện. Vì đây là trading bot không phải người nên em cũng chưa biết cách xử lí vấn đề này. Có thể ở đây em sẽ kết hợp với xét sóng Elliott và cho bot học các mốc chốt lời cắt lỗ để giải quyết điểm yếu này.

---

## 5. Đề xuất cải thiện

Với kiến thức của em thì em sẽ ưu tiên tối ưu lại trading bot theo các hướng sau:

- **Bổ sung MA5 và MA100** để cung cấp tín hiệu sớm về xung lực ngắn hạn và có thể dùng để vào lệnh sớm hơn một nhịp khi 3 MA dài đã xếp đúng hướng cũng như hỗ trợ lọc bớt tín hiệu giả.

- **Tích hợp Fibonacci Retracement** để có thể tự động hóa việc vào lệnh. Khi vào lệnh long, lấy đỉnh–đáy gần nhất và đặt take-profit tại Fibonacci extension 1.272 hoặc 1.618; stop-loss tại retracement 0.618, không cần chờ MA đảo.

- **Tránh vào lệnh trong 15 phút đầu phiên** (biến động bất thường) **và 15 phút cuối phiên** (đây là theo kinh nghiệm cá nhân của em thôi) vì nó hay bị nhiễu và dễ bị quét SL.

- **Walk-forward optimization thay vì backtest tĩnh** ví dụ như tái tối ưu định kỳ (ví dụ mỗi 6 tháng) để chiến lược thích nghi với chế độ thị trường mới, thay vì giữ cứng tham số 10/20/50/200 cho suốt 8 năm.

---

Đây là bài reflection nhỏ về trading stratergy của em. Cảm ơn QuantVN đã publish github để em có thể backtest trên máy tính của mình thay vì phải crawl data các dữ liệu phái sinh hay cổ phiếu vì hiện tại em đang không crawl được data các cổ phiếu, nên nếu được rất mong được đồng hành với QuantVN.

Em cũng đang định hướng đến project về việc kết hợp **hybrid forecasting models** và **econometric** (ML/DL và sử dụng những bài toán cổ điển như MIDAS, ...) để forecast thị trường chứng khoán Việt Nam. Cùng với đó là build một **RAG** để hỏi đáp về vấn đề tài chính, định hướng đầu tư,... như mấy con AI của các phần mềm chứng khoán Việt Nam hiện tại. Từ đó deploy một product maybe dùng **Streamlit** và **real-time inferences** cho project cuối khóa của mình.
