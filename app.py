import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

# ページ設定
st.set_page_config(
    page_title="ASU Webスクレイピングツール",
    page_icon="🕷️",
    layout="centered"
)

# ヘッダー
st.markdown("### 🏢 ASU")
st.title("🕷️ Webスクレイピングツール")
st.write("WebページからタイトルとH1見出しを取得します")

st.markdown("---")

# 説明
with st.expander("📖 使い方"):
    st.markdown("""
    ### このツールでできること
    - Webページのタイトルを取得
    - H1見出しを取得
    - ページの基本情報を確認
    
    ### 使い方
    1. URLを入力
    2. 「情報を取得」ボタンをクリック
    3. ページ情報が表示されます
    
    ### 注意
    - 一部のサイトはアクセス制限があります
    - 商用利用の場合は各サイトの規約を確認してください
    """)

st.markdown("---")

# URL入力
st.subheader("🔗 URLを入力してください")

url = st.text_input(
    "WebページのURL",
    placeholder="https://example.com",
    help="httpsから始まる完全なURLを入力してください"
)

# サンプルURL
st.markdown("**サンプルURL（クリックでコピー）:**")
sample_urls = [
    "https://www.yahoo.co.jp/",
    "https://news.yahoo.co.jp/",
    "https://www.nhk.or.jp/",
]

for sample_url in sample_urls:
    st.code(sample_url)

# 取得ボタン
if st.button("🕷️ 情報を取得", type="primary", use_container_width=True):
    
    if not url:
        st.error("❌ URLを入力してください")
    elif not url.startswith(("http://", "https://")):
        st.error("❌ URLは http:// または https:// から始まる必要があります")
    else:
        try:
            # ヘッダーを設定（ブラウザのふりをする）
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            with st.spinner("ページを取得中..."):
                # ページを取得
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                
                # 文字コードを自動判定
                response.encoding = response.apparent_encoding
            
            # HTMLを解析
            soup = BeautifulSoup(response.content, 'html.parser')
            
            st.success("✅ ページの取得に成功しました！")
            
            st.markdown("---")
            st.subheader("📊 取得した情報")
            
            # タイトルを取得
            title = soup.find('title')
            if title:
                st.markdown("### 📄 ページタイトル")
                st.info(title.get_text(strip=True))
            else:
                st.warning("⚠️ タイトルが見つかりませんでした")
            
            st.markdown("---")
            
            # H1見出しを取得
            h1_tags = soup.find_all('h1')
            if h1_tags:
                st.markdown("### 📌 H1見出し")
                for idx, h1 in enumerate(h1_tags, 1):
                    h1_text = h1.get_text(strip=True)
                    if h1_text:
                        st.write(f"{idx}. {h1_text}")
            else:
                st.info("ℹ️ H1見出しが見つかりませんでした")
            
            st.markdown("---")
            
            # H2見出しを取得
            h2_tags = soup.find_all('h2', limit=5)  # 最初の5個だけ
            if h2_tags:
                st.markdown("### 📝 H2見出し（最大5個）")
                for idx, h2 in enumerate(h2_tags, 1):
                    h2_text = h2.get_text(strip=True)
                    if h2_text:
                        st.write(f"{idx}. {h2_text}")
            
            st.markdown("---")
            
            # リンク数を取得
            links = soup.find_all('a')
            st.markdown("### 🔗 ページ情報")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("リンク数", len(links))
            
            with col2:
                images = soup.find_all('img')
                st.metric("画像数", len(images))
            
            with col3:
                paragraphs = soup.find_all('p')
                st.metric("段落数", len(paragraphs))
            
            st.markdown("---")
            
            # メタ情報
            st.markdown("### 🔍 メタ情報")
            
            # description
            description = soup.find('meta', attrs={'name': 'description'})
            if description and description.get('content'):
                st.write("**説明文:**")
                st.info(description.get('content'))
            
            # keywords
            keywords = soup.find('meta', attrs={'name': 'keywords'})
            if keywords and keywords.get('content'):
                st.write("**キーワード:**")
                st.info(keywords.get('content'))
            
            st.markdown("---")
            
            # HTMLソースの一部を表示
            with st.expander("🔧 HTMLソース（最初の1000文字）"):
                html_text = str(soup)[:1000]
                st.code(html_text, language='html')
        
        except requests.exceptions.Timeout:
            st.error("❌ タイムアウト: ページの読み込みに時間がかかりすぎています")
        
        except requests.exceptions.ConnectionError:
            st.error("❌ 接続エラー: インターネット接続を確認してください")
        
        except requests.exceptions.HTTPError as e:
            st.error(f"❌ HTTPエラー: {e}")
            st.info("ℹ️ このページはアクセスが制限されている可能性があります")
        
        except Exception as e:
            st.error(f"❌ エラーが発生しました: {str(e)}")

# 注意事項
st.markdown("---")
st.warning("""
⚠️ **注意事項**
- Webスクレイピングは各サイトの利用規約を確認してください
- 過度なアクセスはサーバーに負荷をかけます
- 商用利用の場合は特に注意が必要です
- このツールは学習目的で作成されています
""")

# フッター
st.markdown("---")
st.caption("🕷️ ASU - Webスクレイピングツール")
st.caption("Created with ❤️ by ASU")
