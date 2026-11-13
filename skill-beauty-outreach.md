---
name: skill-beauty-outreach
description: 美容クリニック等へのChatGPT広告営業（メール/フォーム）の送信パイプライン＋新戦略（Yahoo!リスト×業界特化資料のページ案内）の引き継ぎ。2026-11-13作成。
---

# 美容クリニック営業（ChatGPT広告）— 引き継ぎスキル

安藤さんが「美容クリニック営業」「ChatGPT広告 送って」「営業自走」「戦略変える」等と言ったら、まずこのファイルを読む。
スクリプトは `C:\Users\ando-y\.claude\skills\beauty-outreach\`（probe.py / record.py）。

## 0. 現状（2026-11-13時点）
- 台帳累計 **438件**（メール＋フォーム）。公式サイトから連絡先が取れる美容専門クリニックは、MHLW725件・QLife・tribeau経由でほぼ試し終え、**今の方法では増えない**。
- 未解決: ①桑沢様（クリニックゼロプラス）宛てChatGPT訴求メールは安藤さんの「OK」待ち（下書き・送信なし） ②KANNO'A.clinic はブラウザ固まりで送信可否不明（再送禁止・自動返信なし） ③下記「新戦略」の文面変更待ち。
- 台帳 `C:\Users\ando-y\Documents\Codex\2026-09-15\new-chat-2\work\outreach-manager\data\companies.json` / 記録 `work\outreach-manager\scripts\record_outreach.py` / 除外チェック `C:\Users\ando-y\Claude\work\outreach_compact_check.py`。

## 1. 守るルール（安藤さん指定）
- 美容中心のみ。AGA/ED/植毛/歯科/内科・再生医療中心・包茎専門は除外。
- 営業お断り/業者お断りの明記、患者専用フォーム（生年月日・性別・年齢・来院歴・カルテ番号・希望日・必須住所）は**送らない**。性別・年齢を決めつけて入れるのも禁止。
- reCAPTCHA/hCaptcha等の画面上の認証は回避しない（バッジのみで画面に出ないものは可）。簡易な認証質問も見送り。
- 二重送信禁止: ドメイン**と**社名の両方で `companies.json` を検索。グループ/系列院の送信済みも重複扱い。到達不明は再送しない。
- 送信前に `python -X utf8 work\outreach_compact_check.py --project "C:\Users\ando-y\Documents\Codex\2026-09-15\new-chat-2" --term <ドメイン> --presend` で `"hits":[]` を確認。
- 成功は**完了表示（thanksページ/「送信されました」等）を確認した時だけ**記録。確認画面で値が空になる（CF7 multistep）・`csrf_failed`・「送信に失敗」は未送信扱い。
- 個人Gmail/docomo/outlook宛て、サイトのドメインと違うメール、ダミー(sample@)は送らない。DYM既存顧客は除外。
- 文面は「貴院」「御中/様」（御社NG）。ZoomのURLはプレーン。Gmailは `htmlBody` 必須（URLは `<a href>`）。
- チャット出力は最小限（進展・問題だけ1〜2行）。待機報告の繰り返しは禁止（安藤さんに強く嫌がられた）。

## 2. 送信パイプライン（1件ずつ）
1. 候補の公式サイトを探す: `WebSearch "<院名>" 公式サイト`（mode=extended・引用符付き。1件で公式URLが出るのは約7割）。
2. `python -X utf8 probe.py <ドメイン>` でメール/フォーム有無を確認。
3. 台帳重複チェック（上記）。
4. 経路:
   - **同一ドメインの法人向けメール**あり → `mcp__12a65b9c...__send_message`（to / subject / htmlBody）。MXは `nslookup -type=mx` で確認。
   - メールなし・シンプルなフォームあり → Chrome MCPで開き、JSで一括入力（native value setter＋input/change/blur。分割電話欄はXXX/XXXX/XXXXを個別、確認画面で必ず値を目視）→ 確認ボタン→送信（2段階フォームは2回クリック）→完了表示を確認。
5. 成功したら `record.py` で台帳登録（下記）。
6. 失敗パターン: 内科/皮膚科中心・年齢性別必須・ハニーポット欄（`nijimo_url_confirm`等は空のまま）・必須の「知ったきっかけ」は「その他」を選ぶ・Chromeが固まったら `tabs_create_mcp` で新規タブ（旧タブは閉じる）。

### 入力値（フォーム共通）
氏名 安藤 侑 / フリガナ アンドウ ユウ / メール ando-y@dym.jp / 電話 XXX-XXXX-XXXX / 会社 株式会社DYM / 部署 WEB事業部 / URL https://dym-design.com/

### メール件名・本文（現行・標準）
件名: 【美容皮膚科・美容クリニックの認知施策について】ChatGPT広告のご相談／株式会社DYM 安藤
本文の流れ: `<院名> ご担当者様` → 突然のご連絡 → `貴院の公式サイトで、<地域・診療内容>を提供されている点を拝見し、ChatGPT広告についてご連絡いたしました。` → 代表が代表兼医師・クリニック経営 → Google・LINEヤフー・Metaの3媒体で最上位認定かつクリニック運営の国内唯一の代理店 → クリニックではChatGPT広告の出稿ができないという定説だが出稿を工夫し運用実績あり → 最新事例・費用対効果を資料化 → ▼美容医療クリニック向け資料 https://drive.google.com/file/d/1d014PMkWZyQWtYIpBmyhLD1QGZrAQDDK/view?usp=sharing → オンライン30分（仮日程候補×5日。直近の候補は11/16〜20。**日付は毎回更新**）→ ▼株式会社DYM（P.11以降がWEB事業部紹介）https://dym-design.com/documents/company/DYM-businessguidebook.pdf → 署名（株式会社DYM WEB事業部 / 安藤侑 / ando-y@dym.jp / XXX-XXXX-XXXX）。

## 3. 台帳登録
```
python -X utf8 C:\Users\ando-y\.claude\skills\beauty-outreach\record.py mail "院名" ドメイン "業態" 宛先メール 対象URL GmailID "きっかけ要約"
python -X utf8 C:\Users\ando-y\.claude\skills\beauty-outreach\record.py form "院名" ドメイン "業態" フォームURL "完了表示の文言" "きっかけ要約"
```
出力例: `recorded 院名 -> 送信完了 (total 438)`。重複は拒否される。

## 4. 新戦略（2026-11-13 安藤さん指示・文面はこれから変更）
目的: 送る会社の**業界ごとに「御社の業界は資料のP.○から掲載」**とメールに入れ、その後メール文面も変える（文面の指示は未受領。受けたらページ案内の1文を組み込んで全体を書き直す）。

### リスト「新Yahoo!リスト」
- スプシID `1ynY7ggo99d1ib_EE33gpWva8pWg4XBeRkfuuD06-3Pg`（約95の業界別シート）。「サマリ」タブ=各シートのURL・リスト数・**業界特化資料のDriveフォルダ**・営業担当、「カテゴリ別資料」タブ=業界ごとの入れたい内容と実績。
- 各シートの行=Yahoo!広告の出稿主（アカウント名・企業名・URL・電話・配信金額・架電結果）。メール列はほぼ空 → 連絡先は上の §2 の要領で探す。
- 安藤さん担当は 医療・薬品（美容医療=42社 / 医薬品 / ヘルスケア / 歯科 / 医療機器 / その他医療）。ローンは60社。
- 「架電不可」の企業が多い。架電禁止・既存顧客の扱いは台帳の除外チェックと同じ。

### 業界特化資料 → ページ案内（ページ番号はテキスト抽出から推定。±1ずれの可能性。使う前に実スライドで確認）
ローン業界 業界特化資料（Drive ID `1_1C7uPHyM6nBZ23olID4hxKHjviFY56N`、2026/9）:
```
総論（市場・媒体トレンド）        P.2〜
消費者金融                        P.15〜
銀行カードローン                  P.26〜
不動産担保ローン                  P.32〜
事業者ローン＆ファクタリング      P.37〜
弊社実績                          P.41〜
DYMからのご提案                   P.46〜
```
美容医療クリニック向け資料（Drive ID `1d014PMkWZyQWtYIpBmyhLD1QGZrAQDDK`、全50p）:
```
医療脱毛（女性）P.4 / 医療脱毛（男性）P.5 / HIFU P.6 / アートメイク P.7
シミ消し P.8 / ワキガ P.9 / 二重整形 P.10〜11 / AGA P.12 / 包茎 P.13 / 一覧表 P.14
全体戦略 P.15〜 / 運用体制 P.18〜 / クリエイティブ戦略 P.22〜 / 配信戦略 P.32〜
サポート体制 P.38〜 / 運用開始スケジュール P.46
```
手順: 送る会社を資料内の小分類に振り分け → 「貴社の業界（◯◯）は、資料のP.○からご覧いただけます」を1文入れる → 振り分け不能は総論の先頭ページ。他業界の資料は「サマリ」のDriveフォルダを読み、各章の扉ページから「小分類→開始ページ」表を同様に作る（読み取りは read_file_content。ページ番号は `N Copyright` の位置から推定）。

## 5. 運用上の注意
- Stop hookで「進めて」が自動再送され続けると、1ターンごとに会話全体を再読み込みしてトークンを大量消費する（今回は81万トークンまで膨らみ5時間枠95%）。長引いたら `/goal clear` と新セッションで再開する。
- 実績のあるノウハウ: JS一括入力＋get_page_textでの確認が最速。read_page/screenshotの多用は避ける。
- 使用量: 週間20%は残す（5時間枠80%超で新規送信を止める）。
