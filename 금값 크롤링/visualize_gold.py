import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import os

# 폰트 설정 (윈도우 환경, 한글 깨짐 방지)
try:
    font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
    rc('font', family=font_name)
    rc('axes', unicode_minus=False)
except Exception as e:
    print("맑은 고딕 폰트를 찾을 수 없어 기본 폰트를 사용합니다.")

def generate_visualizations(csv_file='gold_price_1year.csv'):
    if not os.path.exists(csv_file):
        print(f"파일을 찾을 수 없습니다: {csv_file}")
        return

    # CSV 데이터 로드
    df = pd.read_csv(csv_file)
    
    # '고시날짜' 컬럼을 datetime 객체로 변환
    df['고시날짜'] = pd.to_datetime(df['고시날짜'])
    
    # 날짜 기준으로 정렬 (오래된 날짜가 먼저 오도록)
    df = df.sort_values(by='고시날짜')
    
    # --- 그래프 1: 살 때 vs 팔 때 순금 시세 트렌드 ---
    plt.figure(figsize=(12, 6))
    plt.plot(df['고시날짜'], df['내가 살 때(순금 3.75g)'], label='내가 살 때 (순금)', color='tomato', linewidth=2)
    plt.plot(df['고시날짜'], df['내가 팔 때(순금 3.75g)'], label='내가 팔 때 (순금)', color='royalblue', linewidth=2)
    
    plt.title('최근 1년 한국금거래소 순금 시세 변동 추이 (3.75g 기준)', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('날짜', fontsize=12)
    plt.ylabel('가격 (원)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=12)
    plt.tight_layout()
    
    # 이미지 저장
    plt.savefig('gold_price_trend.png', dpi=300)
    print("그래프 1 저장 완료: gold_price_trend.png")
    plt.close()
    
    # --- 그래프 2: 팔 때 순도별 시세 비교 ---
    plt.figure(figsize=(12, 6))
    plt.plot(df['고시날짜'], df['내가 팔 때(순금 3.75g)'], label='순금 (24K)', color='gold', linewidth=2)
    plt.plot(df['고시날짜'], df['내가 팔 때(18K)'], label='18K', color='darkorange', linewidth=2)
    plt.plot(df['고시날짜'], df['내가 팔 때(14K)'], label='14K', color='saddlebrown', linewidth=2)
    
    plt.title('최근 1년 내가 팔 때 순도별(24K, 18K, 14K) 금 시세 추이', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('날짜', fontsize=12)
    plt.ylabel('가격 (원)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=12)
    plt.tight_layout()
    
    # 이미지 저장
    plt.savefig('gold_sell_types.png', dpi=300)
    print("그래프 2 저장 완료: gold_sell_types.png")
    plt.close()

if __name__ == "__main__":
    generate_visualizations()
