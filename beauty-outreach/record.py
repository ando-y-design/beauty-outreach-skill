"""送信後の台帳登録。メール/フォーム共通。
使い方:
  python -X utf8 record.py mail  "会社名" ドメイン "業態" 宛先メール 対象URL Gmail_id "きっかけ要約"
  python -X utf8 record.py form  "会社名" ドメイン "業態" フォームURL "完了表示の文言" "きっかけ要約"
カレントは任意。台帳は重複を拒否する（同一ドメイン/社名は2回目が弾かれる）。
"""
import json, pathlib, subprocess, sys, tempfile

PROJ = r"C:\Users\ando-y\Documents\Codex\2026-09-15\new-chat-2"
mode = sys.argv[1]
name, dom, ind = sys.argv[2], sys.argv[3], sys.argv[4]
tmp = pathlib.Path(tempfile.mkdtemp())
msgf = tmp / f"msg_{dom}.txt"
msgf.write_text(f"【美容皮膚科・美容クリニックの認知施策について】ChatGPT広告のご相談／株式会社DYM 安藤\n\n{name} ご担当者様\n（以降、標準文面＋DYM紹介リンク）", encoding="utf-8")
if mode == "mail":
    to, url, mid, trig = sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8]
    p = dict(key=name, company_name=name, domain=dom, industry=ind, form_url=to, status="送信完了",
             trigger=dict(category="公式サイト", summary=trig),
             review_note=f"公式サイト記載のメール窓口 {to} へGmail htmlBodyで送信",
             send=dict(url=url, message_file=str(msgf), result_text=f"Gmail message id {mid}"))
else:
    form, res, trig = sys.argv[5], sys.argv[6], sys.argv[7]
    p = dict(key=name, company_name=name, domain=dom, industry=ind, form_url=form, status="送信完了",
             trigger=dict(category="公式サイト", summary=trig),
             review_note="公式お問い合わせフォームから送信(送信後の完了表示を確認)",
             send=dict(url=form, message_file=str(msgf), result_text=res))
pf = tmp / f"p_{dom}.json"
pf.write_text(json.dumps(p, ensure_ascii=False), encoding="utf-8")
r = subprocess.run([sys.executable, r"work\outreach-manager\scripts\record_outreach.py", str(pf)],
                   cwd=PROJ, capture_output=True, text=True, encoding="utf-8", errors="replace")
print((r.stdout or "").strip() or (r.stderr or "").strip())
