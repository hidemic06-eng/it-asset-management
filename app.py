import streamlit as st
from supabase import create_client
import pandas as pd # データの加工用に必要です

# 1. ページ設定
st.set_page_config(page_title="IT資産管理システム", layout="wide")
st.title("💻 IT資産管理システム")

# 2. SecretsからURLとKeyを直接読み込む
url = st.secrets["connections"]["supabase"]["url"]
key = st.secrets["connections"]["supabase"]["key"]

# 3. 接続クライアントの作成
@st.cache_resource
def get_supabase():
    return create_client(url, key)

supabase = get_supabase()

# 4. データ表示
st.subheader("📊 PC資産一覧")
try:
    # データを取得（リレーションでユーザー名も取得）
    response = supabase.table("pc_assets").select("*, user_accounts(user_name)").execute()
    
    if response.data:
        # リスト形式のデータを加工しやすい「DataFrame」に変換
        df = pd.DataFrame(response.data)
        
        # --- 日付形式の変換処理 ---
        if 'updated_at' in df.columns:
            # 1. 文字列を日時に変換
            # 2. 世界標準時(UTC)から日本時間(Asia/Tokyo)に変換
            # 3. 読みやすい書式（2026/03/31 13:00）に整形
            df['updated_at'] = pd.to_datetime(df['updated_at']).dt.tz_convert('Asia/Tokyo').dt.strftime('%Y/%m/%d %H:%M')
        # ------------------------

        # 画面に表を表示
        st.dataframe(df, use_container_width=True)
        
    else:
        st.info("データが見つかりません。Supabase側にデータがあるか確認してください。")
except Exception as e:
    st.error(f"接続に失敗しました: {e}")
