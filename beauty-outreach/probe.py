"""公式サイトのメール/問い合わせフォーム有無を調べる。
使い方: python -X utf8 probe.py www.example.com other.example.jp
出力: ドメイン | メール候補 | [(フォームURL, textarea数, 営業お断り, reCAPTCHA)]
"""
import re, sys, urllib.request
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124 Safari/537.36"}
EM = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def get(u):
    try:
        with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=12) as r:
            return r.geturl(), r.read(700000).decode(r.headers.get_content_charset() or "utf-8", "replace")
    except Exception:
        return u, ""


for d in sys.argv[1:]:
    _, top = get("https://" + d + "/")
    links = set(re.findall(r'href=["\']([^"\']+)["\']', top))
    cands = [l for l in links if re.search(r"contact|inquiry|toiawase|mail|問い合わ|form|privacy|company|tokusho|commerce", l, re.I)]
    emails = set(EM.findall(top))
    forms = []
    for l in list(cands)[:8]:
        if l.startswith("/"):
            l = "https://" + d + l
        if not l.startswith("http"):
            continue
        _, h = get(l)
        emails |= set(EM.findall(h))
        t = re.sub(r"<[^>]+>", " ", h)
        forms.append((l[:70], len(re.findall("<textarea", h, re.I)),
                      int(bool(re.search(r"営業[^。]{0,12}(お断り|ご遠慮)|セールス[^。]{0,8}(お断り|ご遠慮)", t))),
                      int(bool(re.search(r"recaptcha|hcaptcha|turnstile", h, re.I)))))
    emails = {e for e in emails if not re.search(r"png|jpg|sentry|example|sample|wixpress|recruit|saiyo", e, re.I)}
    print(d, "|", sorted(emails)[:4], "|", [f for f in forms if f[1] > 0][:3])
