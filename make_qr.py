import qrcode

# 💡 카카오페이/토스 송금 링크 또는 안내 문구 삽입
# 예시 1: 카카오페이 송금 링크 주소 (실제 본인의 송금 링크나 계좌 정보 입력)
# 예시 2: "농협 301-XXXX-XXXX-XX 해담은농장" 같은 텍스트 정보 입력도 가능합니다.
pay_url = "https://qr.kakaopay.com/xxxxxx"  # 본인의 카카오페이 송금 링크 입력

# QR 코드 객체 생성 설정
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)

# 데이터 추가 및 이미지 생성
qr.add_data(pay_url)
qr.make(fit=True)

# 이미지 색상 커스텀 (선택사항)
img = qr.make_image(fill_color="black", back_color="white")

# 파일로 저장 (해담은농장 프로젝트 폴더에 저장)
img.save("qr_code.png")

print("QR 코드 이미지('qr_code.png')가 성공적으로 생성되었습니다!")