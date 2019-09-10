# tasukaru_bot
助かる  
  ## 必要なもの  
  ### Discord  
  Discordbotのアクセストークン  
  ### Twitter  
  Twitterの各種キー(4つ)  
  ### GoogleDrive  
  credentials.json(認証済であることを証明するためのファイル(?) 最初のみブラウザによる認証があり、生成される)  
  hogehoge.json(GoogleDriveのキーが入ってるやつ)  

  ## 準備  
  settings.yaml の各種キーを埋める  
  tasukaru.py の 11行目 book_name を埋める  
  tasukaru_bot.py の 45行目 client.run('***') にDiscordbotのアクセストークンを入力  

  ## ざっくりした動作説明  
  0.待機状態
  1.twitterのURLを検知すると画像付きかどうか見る  
  2.画像付きならばローカルに落とす、そうでないならば0に戻る  
  3.GoogleDriveにその画像をアップロードする。その後ローカルの画像を削除する。  
  4.GoogleSpreadSheetに各種情報を書き込む。フォーマットは身内で使ってるシステム用。  
  5.助かる。0に戻る  
  
  ## 履歴
  ### ver 1.0.0
  公開用にコメント追加とか各種キー削除など整備した  
  
