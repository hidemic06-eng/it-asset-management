import streamlit as st
from supabase import create_client

# ページ設定
st.set_page_config(page_title="IT資産管理システム", layout="wide")
st.title("💻 IT資産管理システム")

# SecretsからURLとKeyを直接読み込む
url = st.secrets["connections"]["supabase"]["url"]
key = st.secrets["connections"]["supabase"]["key"]

# 接続クライアントの作成
@st.cache_resource
def get_supabase():
    return create_client(url, key)

supabase = get_supabase()

# データ表示
st.subheader("📊 PC資産一覧")
try:
    # データを取得（リレーションでユーザー名も取得）
    response = supabase.table("pc_assets").select("*, user_accounts(user_name)").execute()
    
    if response.data:
        st.dataframe(response.data, use_container_width=True)
    else:
        st.info("データが見つかりません。Supabase側にデータがあるか確認してください。")
except Exception as e:
    st.error(f"接続に失敗しました: {e}")
