import streamlit as st
import pandas as pd
import os
import datetime

# 페이지 기본 설정
st.set_page_config(page_title="해담은 (HDN) 농장 - 농산물 직거래 포털", page_icon="🌾", layout="wide")

# 🎨 [UI 스타일링] 모든 상품 이미지의 높이와 크기를 일정하게 고정하여 글자 위치를 맞춤
st.markdown("""
<style>
    /* 상품 이미지 카드 고정 크기 및 비율 유지 설정 */
    [data-testid="stImage"] img {
        height: 160px !important;
        width: 100% !important;
        object-fit: cover !important;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Header & Branding
st.title("🌾 해담은 (HDN) 농장")
st.caption("햇살과 정성을 담은 신선 농산물 직거래 포털")

# 1. 세션 상태 초기화
if 'menu' not in st.session_state:
    st.session_state.menu = "농장소개"

if 'cart' not in st.session_state:
    st.session_state.cart = [] # 장바구니 리스트

if 'orders' not in st.session_state:
    st.session_state.orders = [] # 전체 주문 내역 저장소 (배송 조회용)

# 주문 폼 입력값 유지 변수
if 'order_name' not in st.session_state:
    st.session_state.order_name = ""
if 'order_phone' not in st.session_state:
    st.session_state.order_phone = ""
if 'order_address' not in st.session_state:
    st.session_state.order_address = ""
if 'order_message' not in st.session_state:
    st.session_state.order_message = ""

# 결제 완료 후 영수증 출력을 위한 세션 변수
if 'order_completed' not in st.session_state:
    st.session_state.order_completed = False
if 'last_order_info' not in st.session_state:
    st.session_state.last_order_info = {}

# 각 상품별 수량 세션 초기화
if 'qty_egg' not in st.session_state:
    st.session_state.qty_egg = 3
if 'qty_crn' not in st.session_state:
    st.session_state.qty_crn = 10
if 'qty_oni' not in st.session_state:
    st.session_state.qty_oni = 1
if 'qty_tur' not in st.session_state:
    st.session_state.qty_tur = 1
if 'qty_tur_pow' not in st.session_state:
    st.session_state.qty_tur_pow = 1
if 'qty_red_beet' not in st.session_state:
    st.session_state.qty_red_beet = 1
if 'qty_dry_eggplant' not in st.session_state:
    st.session_state.qty_dry_eggplant = 1
if 'qty_malt' not in st.session_state:
    st.session_state.qty_malt = 1

def change_menu(target_menu):
    st.session_state.menu = target_menu

# 스마트 이미지 출력 함수 (한글/영문 및 확장자 여러 개를 유연하게 탐색)
def show_product_image(file_candidates, emoji_icon):
    if isinstance(file_candidates, str):
        file_candidates = [file_candidates]
    
    found_file = None
    for f in file_candidates:
        if os.path.exists(f):
            found_file = f
            break
            
    if found_file:
        st.image(found_file, use_container_width=True)
    else:
        st.markdown(f"<h1 style='text-align: center; font-size: 60px; margin: 20px 0;'>{emoji_icon}</h1>", unsafe_allow_html=True)

# 2. 상단 네비게이션 라디오 버튼 (고객 쇼핑 동선에 맞춘 순서)
cart_count = len(st.session_state.cart)
menu_list = [
    "농장소개", 
    "제철 농산물 (쇼핑)", 
    f"장바구니 ({cart_count}개)", 
    "주문/예약 문의", 
    "농장 출하 캘린더", 
    "배송 조회"
]

menu_mapping = {
    "농장소개": "농장소개",
    "제철 농산물 (쇼핑)": "제철 농산물 (쇼핑)",
    f"장바구니 ({cart_count}개)": "장바구니",
    "주문/예약 문의": "주문/예약 문의",
    "농장 출하 캘린더": "농장 출하 캘린더",
    "배송 조회": "배송 조회"
}

current_display_menu = [k for k, v in menu_mapping.items() if v == st.session_state.menu][0]
current_index = menu_list.index(current_display_menu)

selected_display = st.radio(
    "메뉴 선택",
    menu_list,
    index=current_index,
    key="menu_radio",
    horizontal=True,
    on_change=lambda: change_menu(menu_mapping[st.session_state.menu_radio])
)

st.markdown("---")

# 3. 각 메뉴별 화면 구현
if st.session_state.menu == "농장소개":
    st.header("☀️ 햇살을 담다, 해담은 농장")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("농장 철학 및 특징")
        st.write("""
        - **하우스 스마트 재배**: 3월부터 11월까지 최적의 환경에서 자라는 명품 가지
        - **땅을 쉬게 하는 고집**: 7~8월 한여름 휴작을 통해 토양 충전 및 가을 수확 준비
        - **당일 수확 / 당일 발송**: 6월과 10월, 가장 달콤한 찰옥수수 직거래
        - **건강한 먹거리**: 제철에 수확한 신선한 양파, 마늘, 그리고 건강한 강황 및 가공 농산물 직거래
        """)
    with col2:
        st.info("💡 **7~8월 가지 휴작 안내**\n\n더 맛있는 가을 가지 생산을 위해 한여름(7~8월)에는 하우스가 쉬어가는 기간입니다. 이 시기를 피해 제철에 가장 맛있는 농산물을 만나보세요!")

elif st.session_state.menu == "제철 농산물 (쇼핑)":
    st.header("🍆 해담은 대표 농산물")
    st.info("💡 상품별 수량을 선택하신 후 **[장바구니 담기]**를 누르면 여러 상품을 함께 담을 수 있습니다.")
    
    # 1행 상품들 (가지, 옥수수, 양파&마늘, 건강 강황)
    cols1 = st.columns(4)
    
    # 1. 명품 가지
    with cols1[0]:
        show_product_image(["가지.jpg", "가지.png", "eggplant.jpg", "eggplant.png"], "🍆")
        st.subheader("명품 가지")
        st.write("출하: **3월 ~ 6월 / 9월 ~ 11월**")
        st.write("가격: **3개 3,000원 / 6개 5,000원**")
        
        qty_eggplant = st.number_input("수량 (개)", min_value=0, max_value=100, step=1, key="qty_egg")
        if qty_eggplant > 0:
            calc_price = (qty_eggplant // 6) * 5000 + ((qty_eggplant % 6) // 3) * 3000 + ((qty_eggplant % 6) % 3) * 1000
        else:
            calc_price = 0
            
        st.write(f"예상 금액: **{calc_price:,}원**")
        if st.button("🛒 장바구니 담기", key="btn_egg"):
            if qty_eggplant > 0:
                st.session_state.cart.append({"name": "명품 가지", "price": calc_price, "unit": f"{qty_eggplant}개"})
                st.success(f"명품 가지 {qty_eggplant}개가 장바구니에 담겼습니다!")
                st.rerun()
            else:
                st.warning("수량을 1개 이상 선택해 주세요.")

    # 2. 여름/가을 옥수수
    with cols1[1]:
        show_product_image(["옥수수.jpg", "옥수수.png", "corn.jpg", "corn.png"], "🌽")
        st.subheader("여름/가을 옥수수")
        st.write("출하: **6월 ~ 7월 / 10월**")
        st.write("가격: **개당 1,000원**")
        
        qty_corn = st.number_input("수량 (개)", min_value=0, max_value=100, step=1, key="qty_crn")
        price_corn = qty_corn * 1000
        
        st.write(f"예상 금액: **{price_corn:,}원**")
        if st.button("🛒 장바구니 담기", key="btn_crn"):
            if qty_corn > 0:
                st.session_state.cart.append({"name": "여름/가을 옥수수", "price": price_corn, "unit": f"{qty_corn}개"})
                st.success(f"옥수수 {qty_corn}개가 장바구니에 담겼습니다!")
                st.rerun()
            else:
                st.warning("수량을 1개 이상 선택해 주세요.")

    # 3. 양파 & 마늘
    with cols1[2]:
        show_product_image(["양파마늘.jpg", "양파마늘.png", "onion.jpg", "onion.png"], "🧅")
        st.subheader("양파 & 마늘")
        st.write("출하: **수확 후 연중 저장판매**")
        st.write("가격: **양파 5kg / 12,000원**")
        
        qty_onion = st.number_input("수량 (망)", min_value=0, max_value=50, step=1, key="qty_oni")
        price_onion = qty_onion * 12000
        
        st.write(f"예상 금액: **{price_onion:,}원**")
        if st.button("🛒 장바구니 담기", key="btn_oni"):
            if qty_onion > 0:
                st.session_state.cart.append({"name": "양파 & 마늘", "price": price_onion, "unit": f"양파 5kg x {qty_onion}망"})
                st.success(f"양파 5kg {qty_onion}망이 장바구니에 담겼습니다!")
                st.rerun()
            else:
                st.warning("수량을 1개 이상 선택해 주세요.")

    # 4. 건강 강황
    with cols1[3]:
        show_product_image(["강황.png", "강황.jpg", "turmeric.jpg", "turmeric.png"], "🟡")
        st.subheader("건강 강황")
        st.write("출하: **생강황 / 분말 / 환**")
        st.write("가격: **강황분말 500g / 20,000원**")
        
        qty_tur = st.number_input("수량 (개)", min_value=0, max_value=50, step=1, key="qty_tur")
        price_tur = qty_tur * 20000
        
        st.write(f"예상 금액: **{price_tur:,}원**")
        if st.button("🛒 장바구니 담기", key="btn_tur"):
            if qty_tur > 0:
                st.session_state.cart.append({"name": "건강 강황", "price": price_tur, "unit": f"강황분말 500g x {qty_tur}개"})
                st.success(f"강황분말 {qty_tur}개가 장바구니에 담겼습니다!")
                st.rerun()
            else:
                st.warning("수량을 1개 이상 선택해 주세요.")

    st.markdown("---")
    
    # 2행 추가 상품들 (강황가루, 레드비트, 건가지, 엿기름)
    cols2 = st.columns(4)

    # 5. 강황가루 200g (18,000원)
    with cols2[0]:
        show_product_image(["강황가루.jpg", "강황가루.png"], "🟡")
        st.subheader("강황가루 200g")
        st.write("출하: **연중 상시 판매**")
        st.write("가격: **200g / 18,000원**")
        
        qty_tur_pow = st.number_input("수량 (개)", min_value=0, max_value=50, step=1, key="qty_tur_pow")
        price_tur_pow = qty_tur_pow * 18000
        
        st.write(f"예상 금액: **{price_tur_pow:,}원**")
        if st.button("🛒 장바구니 담기", key="btn_tur_pow"):
            if qty_tur_pow > 0:
                st.session_state.cart.append({"name": "강황가루", "price": price_tur_pow, "unit": f"200g x {qty_tur_pow}개"})
                st.success(f"강황가루 200g {qty_tur_pow}개가 장바구니에 담겼습니다!")
                st.rerun()
            else:
                st.warning("수량을 1개 이상 선택해 주세요.")

    # 6. 레드비트(건비트) 90g (7,800원)
    with cols2[1]:
        show_product_image(["레드비트.jpg", "레드비트.png", "beet.jpg"], "🔴")
        st.subheader("레드비트(건비트)")
        st.write("출하: **연중 상시 판매**")
        st.write("가격: **90g / 7,800원**")
        
        qty_red_beet = st.number_input("수량 (개)", min_value=0, max_value=50, step=1, key="qty_red_beet")
        price_red_beet = qty_red_beet * 7800
        
        st.write(f"예상 금액: **{price_red_beet:,}원**")
        if st.button("🛒 장바구니 담기", key="btn_red_beet"):
            if qty_red_beet > 0:
                st.session_state.cart.append({"name": "레드비트(건비트)", "price": price_red_beet, "unit": f"90g x {qty_red_beet}개"})
                st.success(f"레드비트(건비트) 90g {qty_red_beet}개가 장바구니에 담겼습니다!")
                st.rerun()
            else:
                st.warning("수량을 1개 이상 선택해 주세요.")

    # 7. 건가지 70g (4,000원)
    with cols2[2]:
        show_product_image(["건가지.jpg", "건가지.png"], "🍆")
        st.subheader("건가지")
        st.write("출하: **연중 상시 판매**")
        st.write("가격: **70g / 4,000원**")
        
        qty_dry_eggplant = st.number_input("수량 (개)", min_value=0, max_value=50, step=1, key="qty_dry_eggplant")
        price_dry_eggplant = qty_dry_eggplant * 4000
        
        st.write(f"예상 금액: **{price_dry_eggplant:,}원**")
        if st.button("🛒 장바구니 담기", key="btn_dry_eggplant"):
            if qty_dry_eggplant > 0:
                st.session_state.cart.append({"name": "건가지", "price": price_dry_eggplant, "unit": f"70g x {qty_dry_eggplant}개"})
                st.success(f"건가지 70g {qty_dry_eggplant}개가 장바구니에 담겼습니다!")
                st.rerun()
            else:
                st.warning("수량을 1개 이상 선택해 주세요.")

    # 8. 엿기름 500g (5,400원)
    with cols2[3]:
        show_product_image(["엿기름.jpg", "엿기름.png", "malt.jpg"], "🌾")
        st.subheader("엿기름")
        st.write("출하: **연중 상시 판매**")
        st.write("가격: **500g / 5,400원**")
        
        qty_malt = st.number_input("수량 (개)", min_value=0, max_value=50, step=1, key="qty_malt")
        price_malt = qty_malt * 5400
        
        st.write(f"예상 금액: **{price_malt:,}원**")
        if st.button("🛒 장바구니 담기", key="btn_malt"):
            if qty_malt > 0:
                st.session_state.cart.append({"name": "엿기름", "price": price_malt, "unit": f"500g x {qty_malt}개"})
                st.success(f"엿기름 500g {qty_malt}개가 장바구니에 담겼습니다!")
                st.rerun()
            else:
                st.warning("수량을 1개 이상 선택해 주세요.")

    st.markdown("---")
    st.subheader("🛍️ 현재 장바구니 담긴 내역")
    if len(st.session_state.cart) > 0:
        shop_total = 0
        for item in st.session_state.cart:
            st.write(f"- **{item['name']}** ({item['unit']}) : {item['price']:,}원")
            shop_total += item['price']
        st.write(f"**총 예상 금액: {shop_total:,}원**")
        
        if st.button("🛒 장바구니 페이지로 이동하기"):
            st.session_state.menu = "장바구니"
            st.rerun()
    else:
        st.info("아직 장바구니에 담긴 상품이 없습니다.")

elif st.session_state.menu == "장바구니":
    st.header("🛒 장바구니 현황")
    
    if len(st.session_state.cart) == 0:
        st.info("장바구니가 비어 있습니다. '제철 농산물 (쇼핑)'에서 상품을 담아보세요!")
    else:
        total_price = 0
        for i, item in enumerate(st.session_state.cart):
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.write(f"**{item['name']}** ({item['unit']})")
            with col2:
                st.write(f"{item['price']:,}원")
            with col3:
                if st.button("삭제", key=f"del_{i}"):
                    st.session_state.cart.pop(i)
                    st.rerun()
            total_price += item['price']
            
        st.markdown("---")
        st.subheader(f"총 결제 예상 금액: {total_price:,}원")
        
        col_a, col_b = st.columns([1, 4])
        with col_a:
            if st.button("주문서 작성하기"):
                st.session_state.menu = "주문/예약 문의"
                st.rerun()
        with col_b:
            if st.button("장바구니 비우기"):
                st.session_state.cart = []
                st.rerun()

elif st.session_state.menu == "주문/예약 문의":
    st.header("📩 주문 및 결제 프로세스")
    
    if st.session_state.order_completed:
        info = st.session_state.last_order_info
        st.success(f"🎉 **{info['name']}님, 결제 및 주문 접수가 정상 완료되었습니다!**")
        
        st.markdown("---")
        st.subheader("🧾 [해담은 농장] 주문 영수증 (주문 내역서)")
        st.write(f"• **주문자 성함**: {info['name']}")
        st.write(f"• **연락처**: {info['phone']}")
        st.write(f"• **배송지 주소**: {info['address']}")
        if info['message']:
            st.write(f"• **요청사항**: {info['message']}")
        st.write(f"• **선택한 결제 방식**: {info['pay_method']}")
        st.write(f"• **주문 일시**: {info['date']}")
        
        st.markdown("#### 📦 주문 상품 목록")
        for item in info['items']:
            st.write(f"- {item['name']} ({item['unit']}) : {item['price']:,}원")
        
        st.markdown(f"### **총 결제 금액: {info['total']:,}원**")
        st.info("💡 입금 확인 후 당일 수확하여 신선하게 발송해 드립니다. 상단 메뉴의 **[배송 조회]**에서 진행 상황을 확인하실 수 있습니다!")
        
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            if st.button("쇼핑 계속하기"):
                st.session_state.order_completed = False
                st.session_state.menu = "제철 농산물 (쇼핑)"
                st.rerun()
        with col_btn2:
            if st.button("배송 조회하러 가기"):
                st.session_state.order_completed = False
                st.session_state.menu = "배송 조회"
                st.rerun()
            
    else:
        total_price = sum([item['price'] for item in st.session_state.cart])
        
        if len(st.session_state.cart) == 0:
            st.warning("⚠️ 장바구니가 비어 있습니다. '제철 농산물 (쇼핑)'에서 상품을 먼저 담아주세요!")
            if st.button("쇼핑하러 가기"):
                st.session_state.menu = "제철 농산물 (쇼핑)"
                st.rerun()
        else:
            st.subheader("1️⃣ 주문자 및 배송 정보 입력")
            st.session_state.order_name = st.text_input("주문자 성함", value=st.session_state.order_name)
            st.session_state.order_phone = st.text_input("연락처", value=st.session_state.order_phone)
            st.session_state.order_address = st.text_input("배송지 주소", value=st.session_state.order_address)
            st.session_state.order_message = st.text_area("배송 요청사항 (선택)", value=st.session_state.order_message)
            
            st.markdown("---")
            
            st.subheader("2️⃣ 주문 상품 및 결제 금액 확인")
            for item in st.session_state.cart:
                st.write(f"- **{item['name']}** ({item['unit']}) : {item['price']:,}원")
            st.markdown(f"### **총 결제하실 금액: {total_price:,}원**")
                
            st.markdown("---")
            
            st.subheader("3️⃣ 결제 방식 선택")
            pay_method = st.radio(
                "결제 방식을 선택해 주세요",
                ["무통장 입금 (계좌이체)", "카카오페이 / 토스 QR 간편송금"],
                horizontal=True
            )
            
            if pay_method == "무통장 입금 (계좌이체)":
                st.info("🏦 **[무통장 입금 안내]**\n- NH농협은행: 302-8200-1517-71\n- 예금주: 박성범 (해담은농장)\n- 위 계좌로 금액을 송금해 주시면 확인 후 발송됩니다.")
            else:
                st.info("📱 **[QR 간편송금 안내]**\n- 스마트폰 카메라 또는 카카오페이/토스 앱으로 아래 QR을 스캔하여 송금해 주세요.")
                
                if os.path.exists("qr_code.png"):
                    st.image("qr_code.png", caption="해담은농장 카카오페이/토스 송금 QR", width=250)
                elif os.path.exists("qr_code.jpg"):
                    st.image("qr_code.jpg", caption="해담은농장 카카오페이/토스 송금 QR", width=250)
                else:
                    st.warning("⚠️ 'qr_code.png' 또는 'qr_code.jpg' 파일이 폴더에 없습니다. 카카오페이/토스 송금 QR 이미지를 폴더에 추가해 주세요.")
                
            st.markdown("---")
            
            if st.button("💳 결제 완료 및 주문 접수하기", type="primary"):
                if not st.session_state.order_name or not st.session_state.order_phone or not st.session_state.order_address:
                    st.warning("성함, 연락처, 배송지 주소를 모두 입력해 주세요!")
                else:
                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    
                    # 새로운 주문 객체 생성
                    new_order = {
                        "name": st.session_state.order_name,
                        "phone": st.session_state.order_phone,
                        "address": st.session_state.order_address,
                        "message": st.session_state.order_message,
                        "pay_method": pay_method,
                        "items": list(st.session_state.cart),  # 장바구니 상품 복사
                        "total": total_price,
                        "date": current_time,
                        "status": "📦 입금 대기 / 상품 준비중",
                        "tracking": "발송 전 (택배사 등록 대기)"
                    }
                    
                    # 주문 내역에 추가
                    st.session_state.orders.append(new_order)
                    st.session_state.last_order_info = new_order
                    st.session_state.order_completed = True
                    
                    # 결제 완료 후 장바구니 비우기
                    st.session_state.cart = []
                    st.rerun()

elif st.session_state.menu == "농장 출하 캘린더":
    st.header("📅 해담은 연간 농산물 출하 캘린더")
    
    calendar_data = {
        "품목": ["하우스 가지", "여름 옥수수", "양파 / 마늘", "가을 옥수수", "건강 강황", "강황가루", "레드비트(건비트)", "건가지", "엿기름"],
        "주요 출하 시기": ["3월 ~ 6월, 9월 ~ 11월", "6월 ~ 7월", "초여름 수확 후 지속 판매", "10월 (가을 한정!)", "연중 (가공품)", "연중 상시", "연중 상시", "연중 상시", "연중 상시"],
        "특이사항": ["7~8월 고온기 휴작", "당일 수확/발송", "망 단위 / 소포장", "가을 2차 수확 특선", "분말, 환, 즙 옵션", "200g 포장", "90g 포장", "70g 포장", "500g 포장"]
    }
    st.table(pd.DataFrame(calendar_data))

elif st.session_state.menu == "배송 조회":
    st.header("🚚 주문 및 배송 현황 조회")
    st.info("💡 주문 시 입력하신 **연락처(전화번호)**를 입력하시면 나의 주문 내역과 배송 상태를 확인하실 수 있습니다.")
    
    search_phone = st.text_input("조회할 연락처를 입력하세요 (예: 010-1234-5678)")
    
    if search_phone:
        matched_orders = [o for o in st.session_state.orders if search_phone.strip() in o['phone']]
        
        if len(matched_orders) == 0:
            st.warning("입력하신 연락처로 조회된 주문 내역이 없습니다.")
        else:
            st.success(f"총 {len(matched_orders)}건의 주문 내역이 조회되었습니다.")
            for idx, order in enumerate(matched_orders):
                with st.expander(f"📦 주문일시: {order['date']} - 주문자: {order['name']} (총 {order['total']:,}원)", expanded=True):
                    st.write(f"• **배송 상태**: **{order['status']}**")
                    st.write(f"• **송장 번호**: {order['tracking']}")
                    st.write(f"• **배송지 주소**: {order['address']}")
                    st.write(f"• **결제 방식**: {order['pay_method']}")
                    if order['message']:
                        st.write(f"• **요청사항**: {order['message']}")
                    st.markdown("---")
                    st.markdown("**[주문 상품 목록]**")
                    for item in order['items']:
                        st.write(f"- {item['name']} ({item['unit']}) : {item['price']:,}원")
                    st.markdown(f"**총 결제 금액: {order['total']:,}원**")
    else:
        st.write("연락처를 입력해 주세요.")