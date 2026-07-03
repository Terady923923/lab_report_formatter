# 血液検査所見フォーマッター

症例報告・論文作成時に、血液検査所見を単位つきで整形するStreamlitアプリです。

## ファイル構成

- app.py
- requirements.txt

## ローカル実行

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Cloud

1. GitHubで新規リポジトリを作成
2. app.py と requirements.txt をアップロード
3. Streamlit Community CloudでNew app
4. Repository、branch、Main file path = app.py を指定
5. Deploy
```

## 注意

通常のテキストコピーではWord側の書式設定に依存します。
アプリ内の「Times New Roman形式でコピー」ボタンでは、ブラウザが対応していればHTML書式つきでコピーします。
