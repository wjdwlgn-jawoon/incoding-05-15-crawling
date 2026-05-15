import urllib.request
import json
import csv
from datetime import datetime, timedelta

def fetch_gold_price(months=12):
    # 오늘 날짜와 1년 전 날짜 계산
    end_date = datetime.now()
    # 대략 1년(365일) 전
    start_date = end_date - timedelta(days=365)
    
    start_date_str = start_date.strftime('%Y.%m.%d')
    end_date_str = end_date.strftime('%Y.%m.%d')
    
    url = 'https://koreagoldx.co.kr/api/price/chart/list'
    
    # API 요청 데이터 (페이로드)
    # srchDt를 '1Y'로 설정하여 1년치 데이터를 요청합니다.
    payload = {
        'srchDt': '1Y',
        'type': 'Au',
        'dataDateStart': start_date_str,
        'dataDateEnd': end_date_str
    }
    
    data = json.dumps(payload).encode('utf-8')
    
    # 헤더 설정
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    
    print(f"한국금거래소에서 {start_date_str} ~ {end_date_str} 기간의 금 시세 데이터를 가져오는 중...")
    
    try:
        with urllib.request.urlopen(req) as response:
            response_data = response.read().decode('utf-8')
            json_data = json.loads(response_data)
            
            # 'list' 키 안에 데이터가 들어있음
            price_list = json_data.get('list', [])
            print(f"총 {len(price_list)}건의 데이터를 가져왔습니다.")
            return price_list
    except Exception as e:
        print(f"데이터 수집 중 오류가 발생했습니다: {e}")
        return []

def save_to_csv(data_list, filename='gold_price_1year.csv'):
    if not data_list:
        print("저장할 데이터가 없습니다.")
        return
        
    # CSV 파일로 저장
    # s_pure: 내가 살 때 순금(3.75g)
    # p_pure: 내가 팔 때 순금(3.75g)
    # p_18k: 내가 팔 때 18K(3.75g)
    # p_14k: 내가 팔 때 14K(3.75g)
    headers = ['고시날짜', '내가 살 때(순금 3.75g)', '내가 팔 때(순금 3.75g)', '내가 팔 때(18K)', '내가 팔 때(14K)']
    
    # 엑셀에서 한글이 깨지지 않도록 utf-8-sig 인코딩 사용
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        for item in data_list:
            date = item.get('date', '')
            buy_pure = item.get('s_pure', 0)
            sell_pure = item.get('p_pure', 0)
            sell_18k = item.get('p_18k', 0)
            sell_14k = item.get('p_14k', 0)
            
            writer.writerow([date, buy_pure, sell_pure, sell_18k, sell_14k])
            
    print(f"데이터가 현재 폴더의 '{filename}' 파일로 저장되었습니다.")

if __name__ == '__main__':
    data = fetch_gold_price()
    if data:
        save_to_csv(data)
