import streamlit as st
from st_supabase_connection import SupabaseConnection

# 1. ページの設定（ブラウザのタブに表示される名前など）
st.set_page_config(page_title="IT資産管理システム", layout="wide")

st.title("💻 IT資産管理システム")

# 2. Supabaseへの接続設定
# ※実際のURLやパスワードは、後でStreamlit側の「Secrets」に隠して設定します
conn = st.connection("supabase", type=SupabaseConnection)

# 3. PC資産一覧の表示
st.subheader("📊 PC資産一覧")
try:
    # pc_assetsテーブルからデータを取得
    # user_accountsテーブルと結合（Join）して利用者名も表示する欲張り設計です！
    query = "*, user_accounts(user_name)"
    rows = conn.query(query, table="pc_assets", ttl="10m").execute()
    
    if rows.data:
        # 取得したデータを綺麗な表形式で表示
        st.dataframe(rows.data, use_container_width=True)
    else:
        st.info("データがまだ登録されていません。pc_assetsテーブルにデータを入れてみてください。")
except Exception as e:
    st.error(f"エラーが発生しました: {e}")

# 4. IPアドレスの管理状況もついでに表示
st.divider() # 区切り線
st.subheader("🌐 IPアドレス管理状況")
try:
    ip_rows = conn.query("*", table="ip_management", ttl="10m").execute()
    if ip_rows.data:
        st.table(ip_rows.data)
except Exception as e:
    st.warning("IPアドレスデータの取得に失敗しました。")
