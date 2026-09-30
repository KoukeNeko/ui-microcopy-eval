<h1 align="center">ui-microcopy-eval</h1>

<p align="center">
  <strong><a href="https://github.com/KoukeNeko/ui-microcopy">ui-microcopy</a> skill 的評測工具與量測紀錄。</strong><br>
  兩位出題者的 held-out 題目、七條模型管道、異家族 judge、配對分析；全部生成與判定檔皆入庫。
</p>

<p align="center">
  <img alt="Held-out 題目" src="https://img.shields.io/badge/HELD--OUT-32_BRIEFS-2196F3?style=for-the-badge">
  <img alt="紀錄數" src="https://img.shields.io/badge/RECORDS-2%2C016_GEN_·_2%2C746_VERDICTS-4CAF50?style=for-the-badge">
  <img alt="Python 3，無相依套件" src="https://img.shields.io/badge/PYTHON_3-NO_DEPS-00A5A5?style=for-the-badge&logo=python&logoColor=white">
</p>

<p align="center">
  <strong>繁體中文</strong> · <a href="README.en.md">English</a>
</p>

<p align="center">
  <a href="#量測設計">量測設計</a>
  · <a href="#結果">結果</a>
  · <a href="#執行">執行</a>
  · <a href="#結果判讀">結果判讀</a>
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

## 簡介

skill 的第一版由同一模型於同一 session 撰寫、出題與評分。審計結果：評分器四分之三的禁止字串出現於 skill 內文，兩題題幹引用 skill 的句子。此類評測量到的是服從度，不是泛化能力。本 repo 為取代該結果而建立的量測工具，設計原則如下。

- **題目與 judge 未接觸 skill。** 32 題由兩個模型家族的出題者撰寫，均未取得 skill 或其字串；雙向 grep 確認 skill 與題目之間無共用字串。judge 為未參與撰寫 skill 的模型家族，依只描述元件與必要事實、不含教義的 rubric 評分。
- **所有數字皆為配對比較。** arm 與 control 的比較在同一模型、同一題、同一次抽樣、同一欄位上進行，回報 McNemar 的 b／c 與以題為叢集的 bootstrap 信賴區間。報告亦列出絕對通過率，僅供描述。

## 量測設計

### held-out 評測（`v2/`）

| | |
| --- | --- |
| **題目** | 32 題，位於 `v2/probes_v2/`：Claude 出題 16、GPT 出題 16；十種產品情境、十種元件；zh-TW 20、en 6、ja 6。各字串的必要事實（`must_convey`）由出題者列出。 |
| **arms** | `control`（僅題目）· `rules`（否定清單，每條附替代寫法）· `exemplar`（元件→形式→範例，不含禁止）· `schema`（僅欄位長度與可空約束）· `skill`（v1）· `skill2` / `skill2b`（v2 草稿）· `postfilter`（control 輸出經 linter 樣式過濾，僅 runtime 題） |
| **管道** | `ollama:<model>`（deepseek、gemma4、nemotron、glm）、`codex`（GPT-6，隔離 `CODEX_HOME`）、`cloakgpt:<session>`、`dry` + `ingest`（人工驅動的 agent）。Claude 結果來自載有使用者規則檔的子代理，標為 *rules-in-context*，不作為 control。 |
| **judge** | gemma4 與 nemotron。每條字串評 `facts_present` 與 `surplus`（0／1）；紀錄跨 arm 隨機排序、移除 arm 標籤後分批評分；主結果不含 judge 對自家族輸出的判定。 |
| **人工校準** | 問題提出者盲評 108 條：一批隨機分層，一批依 judge 判定分層。 |
| **客觀量** | 語言洩漏（英文題出現中日文字、繁中題出現簡體字、日文題僅含漢字）、備註非空率、字串長度；直接由生成檔統計。 |

### 術語表交付（`v2/drift/`）

16 題繁中題，描述畫面而不寫出目標詞（「app 為了加快載入而暫存在裝置上的資料」，不寫 快取）；五種詞表交付方式、四個模型、每格兩次抽樣，共 640 次生成；僅以 skill 的 linter 規則評分。

### 第一版工具（`run_eval.py`、`fixtures.json`、`results/`）

九題、四個 arm，以 linter 與各題的 require／forbid 樣式評分。保留作為最初量測的紀錄；題目與評分器和受評 skill 共用文字，其結果為開發階段證據，本文件的表格不依賴它。

## 結果

### skill 對 control（同組模型）

淨通過差 = (b − c)/n，通過定義為「無多餘且必要事實齊全」；CI 為以題為叢集的 bootstrap。僅計入 v1 與 v2 皆有的管道（Claude Haiku 與 Sonnet、deepseek、gemma、nemotron）；judge 不評自家族。

| judge | 題目 | rules | exemplar | schema | skill v1 | skill v2 |
| --- | --- | --- | --- | --- | --- | --- |
| gemma | 全部 32 | +12 [+2, +21] | +7 [−4, +18] | 0 [−6, +8] | +8 [0, +15] | **+8 [+1, +15]** |
| gemma | Claude 出題 | +18 [+6, +31] | +12 [−3, +28] | +2 [−7, +13] | +16 [+8, +25] | +13 [+3, +23] |
| gemma | GPT 出題 | +4 [−9, +15] | −1 [−11, +8] | −3 [−12, +5] | −5 [−16, +3] | 0 [−8, +8] |
| nemotron | 全部 32 | −2 [−14, +11] | −1 [−12, +8] | −8 [−17, +3] | −2 [−12, +7] | **+8 [+1, +15]** |
| nemotron | Claude 出題 | +9 [−13, +29] | +4 [−11, +19] | −4 [−19, +14] | +2 [−11, +14] | +14 [+5, +21] |
| nemotron | GPT 出題 | −12 [−26, −1] | −7 [−23, +6] | −11 [−24, +1] | −8 [−22, +5] | +1 [−8, +9] |

Δ 必要事實（gemma）：rules −6.5、exemplar −8.3、schema −11.6、skill v1 −6.5、skill v2 −3.4；nemotron：−9.7、−2.2、−11.6、−7.9、**+1.1**。GPT 出題的部分，v1 損失 15.7 點必要事實，v2 損失 8.8（gemma）與 1.7（nemotron）。所有以刪減為主的介入均造成事實損失；v2 將事實與語言置於刪減之前。

客觀量：英文題回答含中文的比例，deepseek 53% → 15%、gemma 41% → 0%、nemotron 82% → 0%（v1 → v2）；題目未列事實的備註，control 填入 88%、v1 12%、v2 0%；linter 作為後處理 −1 pp [−3, 0]，Δ 事實 −4.0。judge 間對 surplus 的一致性（gemma 對 nemotron）：κ 0.45，n = 1,276。

### 人工校準

108 條盲評：判定多餘 4 條（3.7%），判定缺資訊 0 條；25 條 control 全數無問題。judge 標記的 27 條中，評分者同意 1 條；judge 精確度 5%，κ ≈ 0。評分者標記的項目為捏造的主張（「不會儲存**或追蹤**」，題目僅述「不儲存」）與一句多餘指示；judge 標記而評分者未標記的項目為 "successfully"、目的子句、onboarding 效益句、錯誤訊息中的範例、確認訊息的驚嘆號。judge 量測的是對教義的嚴格服從度，與提出者的實際判準不同。明細見 [`v2/eval_v2/human_calibration.md`](v2/eval_v2/human_calibration.md)。

### 術語表交付

| arm | 字串數 | 含中國用語 | 95% CI | 標準台灣詞 |
| --- | --- | --- | --- | --- |
| control（僅題目） | 315 | **0.0%** | 0–1% | 42.9% |
| 一句否定指示（不用中國用語） | 333 | **2.4%** | 1–5% | 45.3% |
| 畫面相關的 1–3 列 | 366 | 0.0% | 0–1% | **65.6%** |
| 整份 40 列的表 | 354 | 0.0% | 0–1% | 51.1% |
| 整表加 60 列雜訊 | 360 | 0.3% | 0–2% | 51.9% |

四個模型在 control 條件下無中國用語；唯一出現漏詞的條件為單句否定指示（deepseek 於該題 control 六次寫「解除安裝」，加入指示後六次寫「卸載」）。標準詞使用率的提升來自畫面相關的列；整表的效果約為其一半。各模型與各題明細見 [`v2/drift/results.md`](v2/drift/results.md)。

## 執行

需求：Python 3，無相依套件。生成需模型管道：`ollama:<model>` 需 `localhost:11434` 的 Ollama daemon，`codex` 需 Codex CLI，`cloakgpt:<id>` 需 CloakGPT session。受測 skill 讀取自 `~/.claude/skills/ui-microcopy`（或腳本旁的 `skill_v2/`）。

```sh
# 1. 污染檢查：題目與 skill 無共用字串（雙向）
python3 v2/eval_v2.py contamination --skill-dir ~/.claude/skills/ui-microcopy
python3 v2/eval_v2.py contamination --skill-dir ~/.claude/skills/ui-microcopy --reverse

# 2. 生成：每次一條管道，每題每 arm 兩次抽樣
python3 v2/eval_v2.py generate --channel ollama:deepseek-v4.1-flash:cloud --arms control,rules,exemplar,schema,skill,skill2b --samples 2
python3 v2/eval_v2.py generate --channel codex --arms control,skill --samples 2

# 3. 評分：judge 與受試者為不同模型家族
python3 v2/eval_v2.py judge --judge ollama:gemma4:31b-cloud
python3 v2/eval_v2.py judge --judge ollama:nemotron-3-super:cloud

# 4. 人工校準與報告
python3 v2/eval_v2.py sample-for-human --n 40          # 產生盲評表與解答檔
python3 v2/eval_v2.py human --rated human_sample.rated.md --key human_sample.key.json
python3 v2/eval_v2.py report                            # 配對表、語言洩漏、非空率、κ
python3 v2/final_numbers.py > v2/final_tables.md        # v1 與 v2 同組模型的表 A–D

# 人工驅動的管道（agent 或人）
python3 v2/eval_v2.py dry --channel-label claude-sonnet-rules-in-context --arms control,skill2b
#   填寫 eval_v2/pending/<channel>/<arm>/<probe>.<k>.txt
python3 v2/eval_v2.py ingest --channel-label claude-sonnet-rules-in-context

# 術語表交付
python3 v2/drift/run.py                 # 16 題 × 5 arms × 4 模型 × 2 次
python3 v2/drift/score.py > v2/drift/results.md

# 第一版工具
python3 run_eval.py --channel ollama:glm-5.3:cloud --arms control,rules,skill
python3 run_eval.py --score results/final
```

紀錄路徑：`v2/eval_v2/gen/<channel>/<arm>/<probe>.<k>.json` 與 `v2/eval_v2/judge/<judge>/<channel>/<arm>/<probe>.<k>.json`；`report` 讀取現有全部紀錄。skill 範例變更後須重跑污染檢查；rubric 變更後須重做人工抽樣。

## 結果判讀

- **於管道內配對。** skill 的效果為同一模型、同一題、同一次抽樣、同一欄位的 `control → skill` 差異。絕對通過率混合了覆蓋範圍不同的管道，僅供描述。
- **以兩個 judge 為準。** gemma 與 nemotron 對 v1 的判定相反（+8 與 −2），對 v2 一致。單一 judge 的數字不作為結論。
- **judge 判準嚴於使用者。** 與人工評分的 κ 兩批皆接近零。arm 間差異反映對教義嚴格讀法的服從度，不反映使用者的接受程度。
- **同時檢視事實軸。** 「無多餘」上升而「事實齊全」下降的 arm，效果為刪除。通過定義要求兩者皆成立。
- **Claude 管道非 control。** 本機子代理載有使用者規則檔；其結果回答「skill 對既有規則是否有增量」。
- **開發階段證據。** v2 的語言修正依第一稿在本題組的結果進行；出貨版另有兩處後續修改（範例清洗、備註槽位）未重測。驗證性量測需凍結的 skill 與未使用過的題目。

## 檔案配置

```text
v2/
  eval_v2.py                       held-out 工具：contamination、generate、judge、human、report
  probes_v2/
    probes_claude.json             16 題，Claude 出題
    probes_gpt.json                16 題，GPT 出題
    SCHEMA.md                      題目格式
    judge_rubric.md                judge 使用的兩軸 rubric
    arms/rules_only.md             否定清單 arm
    arms/exemplar_only.md          正例 arm
  eval_v2/
    gen/<channel>/<arm>/           2,016 筆生成
    judge/<judge>/<channel>/<arm>/ 2,746 筆判定
    report.md                      完整表格
  final_numbers.py                 v1 與 v2 同組模型的配對表（表 A–D）
  final_tables.md                  其輸出
    human_calibration.md           兩批盲評與 κ
    human_sample1.rated.md, human_sample2.rated.md
  drift/
    probes.json, run.py, score.py  術語表交付實驗
    gen/                           640 筆生成
    results.md
run_eval.py, fixtures.json, results/   第一版工具與其執行紀錄
```

## 限制

- 32 題、每題 2 次抽樣、32 個叢集單位，可偵測十個百分點以上的效果；驗證性設計約需 120–390 題。
- 人工評分者一位，為問題提出者本人；屬校準而非評分者間信度。
- GPT-6 無 v2 結果（Codex 配額於執行中用盡）；glm 僅執行 Claude 出題的部分。
- judge 的多餘判準與 skill 教義共用分類；通過率不等於介面品質。
- 術語表實驗涵蓋四個開源模型與 16 題；「標準台灣詞」為窄定義（「暫存資料」不計為 快取，亦不計為錯誤）。
