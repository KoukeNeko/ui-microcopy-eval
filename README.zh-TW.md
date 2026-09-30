<h1 align="center">ui-microcopy-eval</h1>

<p align="center">
  <strong><a href="https://github.com/KoukeNeko/ui-microcopy">ui-microcopy</a> skill 背後的量測。</strong><br>
  兩位出題者的 held-out 題目、七條模型管道、異家族的 judge、配對分析——以及每一筆生成與判定，全部入庫。
</p>

<p align="center">
  <img alt="Held-out 題目" src="https://img.shields.io/badge/HELD--OUT-32_BRIEFS-2196F3?style=for-the-badge">
  <img alt="紀錄數" src="https://img.shields.io/badge/RECORDS-2%2C016_GEN_·_2%2C746_VERDICTS-4CAF50?style=for-the-badge">
  <img alt="Python 3，無相依套件" src="https://img.shields.io/badge/PYTHON_3-NO_DEPS-00A5A5?style=for-the-badge&logo=python&logoColor=white">
</p>

<p align="center">
  <a href="README.md">English</a> · <strong>繁體中文</strong>
</p>

<p align="center">
  <a href="#量什麼">量什麼</a>
  · <a href="#結果">結果</a>
  · <a href="#怎麼跑">怎麼跑</a>
  · <a href="#怎麼讀結果">怎麼讀結果</a>
  · <a href="#檔案配置">檔案配置</a>
</p>

```sh
python3 v2/eval_v2.py contamination --skill-dir ~/.claude/skills/ui-microcopy          # 雙向
python3 v2/eval_v2.py generate --channel ollama:gemma4:31b-cloud --arms control,skill --samples 2
python3 v2/eval_v2.py judge --judge ollama:nemotron-3-super:cloud
python3 v2/eval_v2.py report
```

```text
| judge    | author | arm      | pairs | b  | c  | net Δ | clustered 95% CI | Δ facts |
| gemma    | all    | skill v2 | 504   | 80 | 42 | +8%   | +1% … +15%       | −3.4%   |
| nemotron | all    | skill v2 | 271   | 36 | 14 | +8%   | +1% … +15%       | +1.1%   |
```

skill 的第一版由同一個模型在同一個 session 裡寫成、出題、評分，成績漂亮——直到審計發現評分器四分之三的禁止字串就在 skill 內文裡、兩題題幹引用了 skill 自己的句子。替自己打分的 skill 量到的是服從，不是泛化。這個 repo 是為了把那個數字換成一個「可能會錯」的數字而做的工具。

**這裡沒有任何東西看過 skill。** 32 題由兩位不同模型家族的出題者寫成，都沒看過 skill 或它的字串；雙向 grep 確認沒有字串從 skill 跑到題目、或從題目跑到 skill。judge 是沒寫過 skill 的家族的模型，依一份只寫元件與必要事實、不寫教義的 rubric 評兩軸。

**每個數字都是配對的。** 一個 arm 與 control 的比較發生在同一模型、同一題、同一次抽樣、同一欄位上，報 McNemar 的 b／c 與以題為叢集的 bootstrap 信賴區間。報告裡也有絕對通過率，但主張不建立在那上面。

## 量什麼

### held-out 評測（`v2/`）

| | |
| --- | --- |
| **題目** | 32 題，在 `v2/probes_v2/`——Claude 出 16、GPT 出 16；十種產品情境、十種元件；zh-TW 20、en 6、ja 6。每條字串的必要事實（`must_convey`）由出題者列出。 |
| **arms** | `control`（只給題）· `rules`（否定清單，每條「不要」附替代寫法）· `exemplar`（元件→形式→範例，不含禁止）· `schema`（只給欄位長度與可空約束）· `skill`（v1）· `skill2` / `skill2b`（v2 草稿）· `postfilter`（control 輸出經 linter 樣式過濾，只有 runtime 題） |
| **管道** | `ollama:<model>`（deepseek、gemma4、nemotron、glm）、`codex`（GPT-6，隔離的 `CODEX_HOME`）、`cloakgpt:<session>`、`dry` + `ingest` 給人工驅動的 agent。Claude 的結果來自帶著使用者規則檔的子代理，標為 *rules-in-context*，不當 control。 |
| **judge** | gemma4 與 nemotron。每條字串各給 `facts_present` 與 `surplus` 的 0／1；紀錄跨 arm 打亂、去掉 arm 標籤後分批評；主結果裡 judge 不評自家族的輸出。 |
| **人工校準** | 提出抱怨的人盲評 108 條——一批隨機分層、一批依 judge 判定分層。 |
| **客觀量** | 語言洩漏（英文題出現中日文字、繁中題出現簡體字、日文題只有漢字）、備註非空率、字串長度——直接從生成檔統計，不經 judge。 |

### 術語表交付（`v2/drift/`）

16 題繁中題，刻意誘發中國用語但不寫出那個詞（「app 為了加快載入而暫存在裝置上的資料」，不寫 快取）；五種把詞表交給模型的方式、四個模型、每格兩次抽樣，共 640 次生成，只用 skill 的 linter 規則評分。

### 第一版工具（`run_eval.py`、`fixtures.json`、`results/`）

九題、四個 arm，用 linter 加每題的 require／forbid 樣式評分。留著是為了記錄最早量了什麼、以及它為什麼不算數：題目與評分器和被評的 skill 共用文字。它的結果是開發過程的證據；下面的表不依賴它。

## 結果

### skill 對 control，同一組模型

淨通過差 = (b − c)/n，通過 = *沒有多餘且必要事實齊全*；CI 為以題為叢集的 bootstrap。只計 v1 與 v2 都有的管道（Claude Haiku 與 Sonnet、deepseek、gemma、nemotron）；judge 不評自家族。

| judge | 題目 | rules | exemplar | schema | skill v1 | skill v2 |
| --- | --- | --- | --- | --- | --- | --- |
| gemma | 全部 32 | +12 [+2, +21] | +7 [−4, +18] | 0 [−6, +8] | +8 [0, +15] | **+8 [+1, +15]** |
| gemma | Claude 出 | +18 [+6, +31] | +12 [−3, +28] | +2 [−7, +13] | +16 [+8, +25] | +13 [+3, +23] |
| gemma | GPT 出 | +4 [−9, +15] | −1 [−11, +8] | −3 [−12, +5] | −5 [−16, +3] | 0 [−8, +8] |
| nemotron | 全部 32 | −2 [−14, +11] | −1 [−12, +8] | −8 [−17, +3] | −2 [−12, +7] | **+8 [+1, +15]** |
| nemotron | Claude 出 | +9 [−13, +29] | +4 [−11, +19] | −4 [−19, +14] | +2 [−11, +14] | +14 [+5, +21] |
| nemotron | GPT 出 | −12 [−26, −1] | −7 [−23, +6] | −11 [−24, +1] | −8 [−22, +5] | +1 [−8, +9] |

Δ 必要事實（gemma）：rules −6.5、exemplar −8.3、schema −11.6、skill v1 −6.5、skill v2 −3.4；nemotron 下 −9.7、−2.2、−11.6、−7.9、**+1.1**。GPT 出的那一半，v1 掉了 15.7 點必要事實；v2 掉 8.8（gemma）與 1.7（nemotron）。每一種教模型刪東西的介入都刪到事實；v2 是把事實與語言排在刪減前面的那一個。

客觀量：英文題出現中文的字串——deepseek 53% → 15%、gemma 41% → 0%、nemotron 82% → 0%（v1 → v2）；題目沒列任何事實的備註，control 填了 88%、v1 12%、v2 0%；linter 當後處理 −1 pp [−3, 0]，Δ 事實 −4.0。judge 之間對 surplus 的一致性，gemma 對 nemotron：κ 0.45（1,276 條）。

### 人看到的

108 條盲評：判多餘 4 條（3.7%）、判缺資訊 0 條；25 條 control 全部乾淨。judge 標的 27 條裡，評分者只同意 1 條——judge 精確度 5%，κ ≈ 0。評分者反對的是捏造的主張（「不會儲存**或追蹤**」，題目只說 *不儲存*）與一句多餘的指示；judge 標而評分者放過的是 "successfully"、目的子句、onboarding 的效益句、錯誤訊息裡的範例、確認訊息的驚嘆號。judge 量的是對教義的嚴格服從；提出教義的人並不那樣嚴格地用它。明細在 [`v2/eval_v2/human_calibration.md`](v2/eval_v2/human_calibration.md)。

### 術語表交付

| arm | 字串數 | 含中國用語 | 95% CI | 標準台灣詞 |
| --- | --- | --- | --- | --- |
| control（只給題） | 315 | **0.0%** | 0–1% | 42.9% |
| 一句否定指示「不用中國大陸用語」 | 333 | **2.4%** | 1–5% | 45.3% |
| 只給畫面相關的 1–3 列 | 366 | 0.0% | 0–1% | **65.6%** |
| 整份 40 列的表 | 354 | 0.0% | 0–1% | 51.1% |
| 整表加 60 列雜訊 | 360 | 0.3% | 0–2% | 51.9% |

四個模型自己不會漏中國用語；唯一漏詞的條件是那一句否定指示（deepseek 在 control 六次寫 解除安裝，加了那句六次寫 卸載）；讓標準詞使用率上升的是畫面相關的那幾列，整張表的效果大約一半。各模型與各題的表在 [`v2/drift/results.md`](v2/drift/results.md)。

## 怎麼跑

Python 3，無相依套件。生成需要模型管道：`ollama:<model>` 要 `localhost:11434` 的 Ollama daemon，`codex` 要 Codex CLI，`cloakgpt:<id>` 要一個 CloakGPT session。被測的 skill 從 `~/.claude/skills/ui-microcopy` 讀（或腳本旁的 `skill_v2/`）。

```sh
# 1. 證明題目與 skill 沒有共用字串，雙向
python3 v2/eval_v2.py contamination --skill-dir ~/.claude/skills/ui-microcopy
python3 v2/eval_v2.py contamination --skill-dir ~/.claude/skills/ui-microcopy --reverse

# 2. 生成——一次一條管道，每題每 arm 兩次抽樣
python3 v2/eval_v2.py generate --channel ollama:deepseek-v4.1-flash:cloud --arms control,rules,exemplar,schema,skill,skill2b --samples 2
python3 v2/eval_v2.py generate --channel codex --arms control,skill --samples 2

# 3. 用與受試者不同家族的模型當 judge
python3 v2/eval_v2.py judge --judge ollama:gemma4:31b-cloud
python3 v2/eval_v2.py judge --judge ollama:nemotron-3-super:cloud

# 4. 對人校準，然後出報告
python3 v2/eval_v2.py sample-for-human --n 40          # 產生盲評表與解答
python3 v2/eval_v2.py human --rated human_sample.rated.md --key human_sample.key.json
python3 v2/eval_v2.py report                            # 配對表、洩漏、非空率、κ

# 人工驅動的管道（agent、人）
python3 v2/eval_v2.py dry --channel-label claude-sonnet-rules-in-context --arms control,skill2b
#   ... 填 eval_v2/pending/<channel>/<arm>/<probe>.<k>.txt ...
python3 v2/eval_v2.py ingest --channel-label claude-sonnet-rules-in-context

# 術語表交付
python3 v2/drift/run.py                 # 16 題 × 5 arms × 4 模型 × 2 次
python3 v2/drift/score.py > v2/drift/results.md

# 第一版工具
python3 run_eval.py --channel ollama:glm-5.3:cloud --arms control,rules,skill
python3 run_eval.py --score results/final
```

紀錄落在 `v2/eval_v2/gen/<channel>/<arm>/<probe>.<k>.json` 與 `v2/eval_v2/judge/<judge>/<channel>/<arm>/<probe>.<k>.json`；`report` 讀現有的全部。改了 skill 的範例就重跑污染檢查；改了 rubric 就重做一次人工抽樣。

## 怎麼讀結果

- **在管道內配對。** 同一模型、同一題、同一次抽樣、同一欄位的 `control → skill` 才是 skill 的效果。絕對通過率混了覆蓋不同的管道，只能描述。
- **兩個 judge，或者不算。** gemma 與 nemotron 對 v1 意見相反（+8 對 −2），對 v2 一致。一個 judge 的數字就只是一個 judge 的數字。
- **judge 比使用者嚴。** 與人的 κ 兩批都接近零。arm 之間的差異說的是「對教義嚴格讀法的服從度」，不是人會多在意。
- **看事實那一軸。** 「無多餘」上升、「事實齊全」下降的 arm，教的是刪除。通過的定義要兩者皆備。
- **Claude 管道不是 control。** 這台機器上的子代理帶著使用者的規則檔；它們的列回答的是「skill 對已在 context 裡的規則有沒有增量」。
- **開發證據，不是驗證。** v2 的語言修正是看了第一稿在這些題上的結果後改的；出貨版另有兩處後續修改（範例清洗、備註槽位）未重測。驗證性的量測需要凍結的 skill 與沒人看過的題目。

## 檔案配置

```text
v2/
  eval_v2.py                       held-out 工具：contamination、generate、judge、human、report
  probes_v2/
    probes_claude.json             16 題，Claude 出
    probes_gpt.json                16 題，GPT 出
    SCHEMA.md                      題目格式
    judge_rubric.md                judge 看到的兩軸 rubric
    arms/rules_only.md             否定清單 arm
    arms/exemplar_only.md          正例 arm
  eval_v2/
    gen/<channel>/<arm>/           2,016 筆生成
    judge/<judge>/<channel>/<arm>/ 2,746 筆判定
    report.md                      README 摘要的完整表
    human_calibration.md           兩批盲評，含 κ
    human_sample1.rated.md, human_sample2.rated.md
  drift/
    probes.json, run.py, score.py  術語表交付實驗
    gen/                           640 筆生成
    results.md
run_eval.py, fixtures.json, results/   第一版工具與它的執行紀錄
```

## 限制

- 32 題、每題 2 次抽樣、32 個叢集單位：看得到十個百分點以上的效果，看不到更細的。驗證性設計約需 120–390 題。
- 人工評分只有一位，也是提出抱怨的人；這是校準，不是評分者間信度。
- GPT-6 沒有 v2 的結果（Codex 配額在執行中用完）；glm 只跑了 Claude 出的那一半。
- judge 的多餘判準與 skill 的教義共用同一套分類；通過率不是介面品質的量度。
- 術語表實驗只涵蓋四個開源模型與 16 題；「標準台灣詞」是窄定義（寫「暫存資料」不算用了 快取，也不算錯）。
