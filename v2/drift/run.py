#!/usr/bin/env python3
"""Lexicon-delivery experiment: does how the zh-TW term table is handed to the
model change the mainland-term rate on briefs that invite drift?

Arms: control (brief only) · instruct (one line) · relevant (line + the
1-3 rows this brief needs) · table (line + the skill's full 40-row table) ·
bigtable (line + full table + 60 non-software cross-strait rows).
Scored mechanically with the skill linter's term rules; no LLM judge.
"""
import json, re, sys, time, urllib.request, random
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(Path.home() / ".claude/skills/ui-microcopy/scripts"))
import microcopy_lint as L

PROBES = json.loads((HERE / "probes.json").read_text())
LEX = (Path.home() / ".claude/skills/ui-microcopy/references/zh-tw-lexicon.md").read_text()
# the two term tables from the lexicon, nothing else
TABLE = LEX[LEX.index("## 第一層"):LEX.index("## 白名單")].strip()
BIG_EXTRA = """
## 其他兩岸用語（非軟體）

| 不用 | 用 |
| --- | --- |
""" + "\n".join(f"| {a} | {b} |" for a, b in [
 ("土豆","馬鈴薯"),("西紅柿","番茄"),("菠蘿","鳳梨"),("獼猴桃","奇異果"),("酸奶","優格"),("方便麵","泡麵"),("冰棍","冰棒"),
 ("出租車","計程車"),("公交車","公車"),("地鐵","捷運"),("自行車","腳踏車"),("摩托車","機車"),("打車","叫車"),("航班","班機"),("登機牌","登機證"),
 ("空調","冷氣"),("洗髮水","洗髮精"),("創可貼","OK繃"),("圓珠筆","原子筆"),("橡皮","橡皮擦"),("復印","影印"),("塑料","塑膠"),
 ("幼兒園","幼稚園"),("高考","學測"),("本科","大學部"),("研究生","研究所"),("導師","指導教授"),
 ("質量","品質"),("水平","水準"),("渠道","通路"),("項目","專案"),("領導","主管"),("工資","薪水"),("快遞","宅配"),("郵編","郵遞區號"),
 ("身份證","身分證"),("賓館","飯店"),("前台","櫃檯"),("衛生間","廁所"),("激光","雷射"),("光盤","光碟"),("芯片","晶片"),("硅","矽"),
 ("納米","奈米"),("概率","機率"),("變量","變數"),("數組","陣列"),("循環","迴圈"),("對象","物件"),("打印機","印表機"),("掃描儀","掃描器"),
 ("攝像頭","網路攝影機"),("揚聲器","喇叭"),("充電寶","行動電源"),("數碼","數位"),("短信","簡訊"),("社交媒體","社群媒體"),("博客","部落格"),
 ("點贊","按讚"),("屏蔽","封鎖"),("舉報","檢舉"),
])
INSTRUCT = "所有字串使用台灣的正體中文介面用語，不用中國大陸用語。"

def relevant_rows(p):
    rows = []
    for line in TABLE.splitlines():
        if line.startswith("|") and any(d in line for d in p["drift"]):
            rows.append(line)
    return "台灣用語對照（本畫面相關）：\n| 不用 | 用 |\n| --- | --- |\n" + "\n".join(rows) if rows else ""

def prompt(p, arm):
    fields = "\n".join(f'- "{k}"：{v}' for k, v in p["fields"].items())
    head = f"你在寫一個 app 的介面字串。語言：繁體中文。\n\n畫面：{p['screen']}\n\n請寫出：\n{fields}\n"
    extra = ""
    if arm == "instruct": extra = INSTRUCT + "\n"
    elif arm == "relevant": extra = INSTRUCT + "\n" + relevant_rows(p) + "\n"
    elif arm == "table": extra = INSTRUCT + "\n" + TABLE + "\n"
    elif arm == "bigtable": extra = INSTRUCT + "\n" + TABLE + "\n" + BIG_EXTRA + "\n"
    tail = '只輸出一個 JSON 物件，鍵為 s1、s2、s3，值為字串；不要其他文字。'
    return head + ("\n" + extra if extra else "") + "\n" + tail

def ollama(model, text):
    body = json.dumps({"model": model, "prompt": text, "stream": False, "think": False}).encode()
    req = urllib.request.Request("http://localhost:11434/api/generate", data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        payload = json.loads(r.read())
    return re.sub(r"<think(?:ing)?>.*?</think(?:ing)?>", "", payload.get("response", ""), flags=re.S)

def extract(raw):
    m = re.search(r"\{.*\}", raw, re.S)
    if not m: return None
    try: return json.loads(m.group(0))
    except Exception: return None

ARMS = ("control", "instruct", "relevant", "table", "bigtable")
MODELS = sys.argv[1:] or ["deepseek-v4.1-flash:cloud", "gemma4:31b-cloud", "nemotron-3-super:cloud", "glm-5.3-flash:cloud"]
SAMPLES = 2
OUT = HERE / "gen"; OUT.mkdir(exist_ok=True)

def run_model(model):
    tag = model.replace(":", "-").replace("/", "-")
    jobs = [(p, a, s) for p in PROBES for a in ARMS for s in range(SAMPLES)]
    random.Random(7).shuffle(jobs)
    for p, a, s in jobs:
        f = OUT / f"{tag}.{p['id']}.{a}.{s}.json"
        if f.exists(): continue
        t0 = time.time()
        try:
            raw = ollama(model, prompt(p, a)); err = ""
        except Exception as e:
            raw, err = "", repr(e)
        f.write_text(json.dumps({"model": model, "probe": p["id"], "arm": a, "sample": s, "raw": raw,
                                 "parsed": extract(raw), "error": err, "seconds": round(time.time() - t0, 1)}, ensure_ascii=False, indent=1))
    return model

if __name__ == "__main__":
    with ThreadPoolExecutor(len(MODELS)) as ex:
        for m in ex.map(run_model, MODELS): print("done", m, flush=True)
    print("DRIFT_DONE")
