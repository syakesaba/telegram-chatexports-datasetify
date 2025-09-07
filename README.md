telegram-chatexports-datasetify
=====

[エクスポートされたTelegramの個人チャットの内容](https://core.telegram.org/import-export)をファインチューニングに利用可能なdatasetに加工するスクリプトです。[NotebookLM](https://notebooklm.google.com)を多用しているので、コードは色々と汚いです。

入力
=====
`result.json`

出力
=====

- conv.csv
    - 列 conv_id: 会話の根と判定された個人チャットのmessage id
    - 列 

Telegramデスクトップ版でのエクスポート方法
=====

1. Telegramデスクトップ版アプリを起動します。
1. メニューアイコン（三本線）をクリックし、「設定」（Settings）を選択します。
1. 設定画面で「詳細」（Advanced）をクリックします。
1. 「Telegramデータのエクスポート」（Export Telegram data）を見つけてクリックします。
1. 何も選択せずエクスポートします。
1. 「エクスポート」（Export）ボタンをクリックすると、エクスポートが開始されます。
1. エクスポートが完了したら、指定した場所にファイルが生成されます。
1. そのファイルのうち、`result.json`を使用します。

注意点
=====
- **モバイル版（iOS/Android）アプリでは、直接チャット履歴をエクスポートすることはできません。** 必ずパソコン版のTelegramアプリを使ってください。
- エクスポートにかかる時間は、チャット履歴の量によって異なります。
- **秘密のチャット（Secret Chat）の履歴はエクスポートできません。** これは、プライバシー保護のために暗号化されているためです。