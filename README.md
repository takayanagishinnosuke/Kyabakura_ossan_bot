# キャバクラ通いのおっさん風ラインボットです
- 夜蝶の気分でおっさんをカモってる雰囲気が味わえます
- 人の写真を送ると感情分析による返答がおこなわれます
- ポジティブかつ積極的なおっさんです。
- ID @636bqvxe
![スクリーンショット 2022-04-15 0 43 16](https://user-images.githubusercontent.com/97178451/163425744-c1b368e0-8f6c-4591-9eae-19c7ceeb4b7b.png)
## 工夫点
- python + LINE開発者ツール + Amazon rekognition  samcliを使用しAWSLamdeへ関数を格納し動かしてます。
- https://docs.aws.amazon.com/ja_jp/rekognition/latest/dg/faces-detect-images.html
## 参考記事
- https://qiita.com/kro/items/67f7510b36945eb9689b
- https://developers.line.biz/ja/docs/messaging-api/line-bot-sdk/
- https://qiita.com/taku-0728/items/c80bcf65aba318ac6db0
- https://qlitre-weblog.com/aws-lambda-line-bot/
- https://xp-cloud.jp/blog/2019/06/26/5572/
- 
## 失敗と今後取り組みたい事
- json形式で推論結果が返ってくるが、うまくdict型にできずstr型でむりくりなんとかしてる…
- 本当はもっと色々な推論結果から返答を作りたかったが間に合わず…
- 返答は定型文で、自然な会話感ができてない。言語生成を用いたmodelを組み込みたい
## 構築環境
- python3.8
- line-bot-sdk
- boto3
- aws-sam-cli
- awscli
## 手順 必要パッケージのinstall
- pip3 install awscli https://pypi.org/project/awscli/
- pip install line-bot-sdk https://pypi.org/project/line-bot-sdk/
## 手順2 deploy時
- https://docs.aws.amazon.com/ja_jp/serverless-application-model/latest/developerguide/serverless-getting-started-hello-world.html
- sam build -t template.json
- sam deploy --guided

## 参考
- https://docs.aws.amazon.com/ja_jp/serverless-application-model/latest/developerguide/serverless-getting-started.html
- https://github.com/line/line-bot-sdk-python
- https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md
- AWS samcli　についての初期設定はこちら　https://www.cloudsolution.tokai-com.co.jp/white-paper/2021/0617-239.html
