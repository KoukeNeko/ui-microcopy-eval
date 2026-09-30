# Held-out 結果 v2

6481 條字串判定，2 個 judge。

## 依介入（全部模型）

| arm | judge | 字串數 | 無多餘 | 事實齊全 | 兩者皆是（通過） | 通過率 95% CI |
| --- | --- | --- | --- | --- | --- | --- |
| control | ollama-gemma4-31b-cloud | 772 | 78% | 79% | 59% | 55%–62% |
| control | ollama-nemotron-3-super-cloud | 352 | 90% | 88% | 81% | 77%–85% |
| exemplar | ollama-gemma4-31b-cloud | 602 | 88% | 71% | 61% | 57%–65% |
| exemplar | ollama-nemotron-3-super-cloud | 261 | 92% | 83% | 77% | 71%–81% |
| postfilter | ollama-gemma4-31b-cloud | 124 | 73% | 69% | 48% | 39%–56% |
| postfilter | ollama-nemotron-3-super-cloud | 65 | 78% | 74% | 65% | 52%–75% |
| rules | ollama-gemma4-31b-cloud | 604 | 92% | 72% | 66% | 62%–70% |
| rules | ollama-nemotron-3-super-cloud | 225 | 93% | 82% | 79% | 73%–84% |
| schema | ollama-gemma4-31b-cloud | 604 | 82% | 69% | 54% | 50%–58% |
| schema | ollama-nemotron-3-super-cloud | 242 | 88% | 76% | 69% | 63%–74% |
| skill | ollama-gemma4-31b-cloud | 772 | 94% | 74% | 68% | 65%–71% |
| skill | ollama-nemotron-3-super-cloud | 372 | 94% | 83% | 81% | 77%–85% |
| skill2 | ollama-gemma4-31b-cloud | 336 | 92% | 89% | 82% | 77%–85% |
| skill2 | ollama-nemotron-3-super-cloud | 252 | 95% | 84% | 80% | 75%–85% |
| skill2b | ollama-gemma4-31b-cloud | 504 | 88% | 87% | 78% | 75%–82% |
| skill2b | ollama-nemotron-3-super-cloud | 394 | 96% | 89% | 87% | 84%–90% |

## 依模型 × 介入

| model / arm | judge | 字串數 | 無多餘 | 事實齊全 | 兩者皆是（通過） | 通過率 95% CI |
| --- | --- | --- | --- | --- | --- | --- |
| claude-haiku-rules-in-context / control | ollama-gemma4-31b-cloud | 84 | 90% | 85% | 76% | 66%–84% |
| claude-haiku-rules-in-context / control | ollama-nemotron-3-super-cloud | 61 | 98% | 87% | 87% | 76%–93% |
| claude-haiku-rules-in-context / postfilter | ollama-gemma4-31b-cloud | 14 | 79% | 86% | 64% | 39%–84% |
| claude-haiku-rules-in-context / postfilter | ollama-nemotron-3-super-cloud | 6 | 100% | 50% | 50% | 19%–81% |
| claude-haiku-rules-in-context / skill | ollama-gemma4-31b-cloud | 84 | 94% | 81% | 75% | 65%–83% |
| claude-haiku-rules-in-context / skill | ollama-nemotron-3-super-cloud | 59 | 92% | 81% | 78% | 66%–87% |
| claude-haiku-rules-in-context / skill2b | ollama-gemma4-31b-cloud | 84 | 94% | 83% | 77% | 67%–85% |
| claude-haiku-rules-in-context / skill2b | ollama-nemotron-3-super-cloud | 65 | 92% | 91% | 86% | 76%–93% |
| claude-sonnet-rules-in-context / control | ollama-gemma4-31b-cloud | 84 | 92% | 87% | 80% | 70%–87% |
| claude-sonnet-rules-in-context / control | ollama-nemotron-3-super-cloud | 54 | 96% | 89% | 87% | 76%–94% |
| claude-sonnet-rules-in-context / postfilter | ollama-gemma4-31b-cloud | 14 | 79% | 93% | 71% | 45%–88% |
| claude-sonnet-rules-in-context / postfilter | ollama-nemotron-3-super-cloud | 11 | 82% | 82% | 73% | 43%–90% |
| claude-sonnet-rules-in-context / skill | ollama-gemma4-31b-cloud | 84 | 99% | 88% | 87% | 78%–93% |
| claude-sonnet-rules-in-context / skill | ollama-nemotron-3-super-cloud | 70 | 96% | 79% | 77% | 66%–85% |
| claude-sonnet-rules-in-context / skill2b | ollama-gemma4-31b-cloud | 84 | 93% | 95% | 88% | 79%–93% |
| claude-sonnet-rules-in-context / skill2b | ollama-nemotron-3-super-cloud | 56 | 100% | 98% | 98% | 91%–100% |
| codex / control | ollama-gemma4-31b-cloud | 168 | 90% | 36% | 26% | 20%–33% |
| codex / exemplar | ollama-gemma4-31b-cloud | 166 | 95% | 34% | 29% | 23%–36% |
| codex / postfilter | ollama-gemma4-31b-cloud | 28 | 93% | 29% | 21% | 10%–40% |
| codex / rules | ollama-gemma4-31b-cloud | 168 | 95% | 35% | 30% | 23%–37% |
| codex / schema | ollama-gemma4-31b-cloud | 168 | 90% | 35% | 24% | 19%–31% |
| codex / skill | ollama-gemma4-31b-cloud | 168 | 96% | 34% | 30% | 23%–37% |
| ollama-deepseek-v4.1-flash-cloud / control | ollama-gemma4-31b-cloud | 168 | 73% | 95% | 70% | 63%–77% |
| ollama-deepseek-v4.1-flash-cloud / control | ollama-nemotron-3-super-cloud | 114 | 85% | 88% | 77% | 69%–84% |
| ollama-deepseek-v4.1-flash-cloud / exemplar | ollama-gemma4-31b-cloud | 168 | 86% | 87% | 75% | 68%–81% |
| ollama-deepseek-v4.1-flash-cloud / exemplar | ollama-nemotron-3-super-cloud | 128 | 94% | 86% | 81% | 74%–87% |
| ollama-deepseek-v4.1-flash-cloud / postfilter | ollama-gemma4-31b-cloud | 28 | 64% | 89% | 61% | 42%–76% |
| ollama-deepseek-v4.1-flash-cloud / postfilter | ollama-nemotron-3-super-cloud | 23 | 70% | 83% | 70% | 49%–84% |
| ollama-deepseek-v4.1-flash-cloud / rules | ollama-gemma4-31b-cloud | 168 | 93% | 90% | 86% | 80%–90% |
| ollama-deepseek-v4.1-flash-cloud / rules | ollama-nemotron-3-super-cloud | 106 | 93% | 86% | 81% | 73%–87% |
| ollama-deepseek-v4.1-flash-cloud / schema | ollama-gemma4-31b-cloud | 168 | 80% | 82% | 67% | 59%–73% |
| ollama-deepseek-v4.1-flash-cloud / schema | ollama-nemotron-3-super-cloud | 130 | 82% | 79% | 66% | 58%–74% |
| ollama-deepseek-v4.1-flash-cloud / skill | ollama-gemma4-31b-cloud | 168 | 93% | 87% | 81% | 74%–86% |
| ollama-deepseek-v4.1-flash-cloud / skill | ollama-nemotron-3-super-cloud | 119 | 96% | 85% | 82% | 75%–88% |
| ollama-deepseek-v4.1-flash-cloud / skill2 | ollama-gemma4-31b-cloud | 168 | 94% | 90% | 85% | 78%–89% |
| ollama-deepseek-v4.1-flash-cloud / skill2 | ollama-nemotron-3-super-cloud | 129 | 98% | 87% | 85% | 78%–90% |
| ollama-deepseek-v4.1-flash-cloud / skill2b | ollama-gemma4-31b-cloud | 168 | 87% | 89% | 80% | 74%–86% |
| ollama-deepseek-v4.1-flash-cloud / skill2b | ollama-nemotron-3-super-cloud | 145 | 99% | 91% | 91% | 85%–95% |
| ollama-gemma4-31b-cloud / control | ollama-nemotron-3-super-cloud | 123 | 89% | 88% | 79% | 71%–85% |
| ollama-gemma4-31b-cloud / exemplar | ollama-nemotron-3-super-cloud | 133 | 89% | 80% | 72% | 64%–79% |
| ollama-gemma4-31b-cloud / postfilter | ollama-nemotron-3-super-cloud | 25 | 80% | 68% | 60% | 41%–77% |
| ollama-gemma4-31b-cloud / rules | ollama-nemotron-3-super-cloud | 119 | 92% | 78% | 77% | 69%–84% |
| ollama-gemma4-31b-cloud / schema | ollama-nemotron-3-super-cloud | 112 | 95% | 73% | 72% | 63%–80% |
| ollama-gemma4-31b-cloud / skill | ollama-nemotron-3-super-cloud | 124 | 93% | 85% | 84% | 76%–89% |
| ollama-gemma4-31b-cloud / skill2 | ollama-nemotron-3-super-cloud | 123 | 92% | 80% | 75% | 66%–82% |
| ollama-gemma4-31b-cloud / skill2b | ollama-nemotron-3-super-cloud | 128 | 93% | 83% | 79% | 71%–85% |
| ollama-glm-5.3-flash-cloud / control | ollama-gemma4-31b-cloud | 100 | 63% | 92% | 55% | 45%–64% |
| ollama-glm-5.3-flash-cloud / exemplar | ollama-gemma4-31b-cloud | 100 | 87% | 84% | 71% | 61%–79% |
| ollama-glm-5.3-flash-cloud / postfilter | ollama-gemma4-31b-cloud | 12 | 67% | 67% | 33% | 14%–61% |
| ollama-glm-5.3-flash-cloud / rules | ollama-gemma4-31b-cloud | 100 | 95% | 86% | 82% | 73%–88% |
| ollama-glm-5.3-flash-cloud / schema | ollama-gemma4-31b-cloud | 100 | 73% | 86% | 61% | 51%–70% |
| ollama-glm-5.3-flash-cloud / skill | ollama-gemma4-31b-cloud | 100 | 93% | 87% | 80% | 71%–87% |
| ollama-nemotron-3-super-cloud / control | ollama-gemma4-31b-cloud | 168 | 68% | 92% | 64% | 57%–71% |
| ollama-nemotron-3-super-cloud / exemplar | ollama-gemma4-31b-cloud | 168 | 85% | 83% | 73% | 65%–79% |
| ollama-nemotron-3-super-cloud / postfilter | ollama-gemma4-31b-cloud | 28 | 57% | 71% | 46% | 30%–64% |
| ollama-nemotron-3-super-cloud / rules | ollama-gemma4-31b-cloud | 168 | 86% | 83% | 73% | 65%–79% |
| ollama-nemotron-3-super-cloud / schema | ollama-gemma4-31b-cloud | 168 | 83% | 82% | 68% | 61%–75% |
| ollama-nemotron-3-super-cloud / skill | ollama-gemma4-31b-cloud | 168 | 90% | 81% | 73% | 66%–79% |
| ollama-nemotron-3-super-cloud / skill2 | ollama-gemma4-31b-cloud | 168 | 89% | 88% | 79% | 72%–84% |
| ollama-nemotron-3-super-cloud / skill2b | ollama-gemma4-31b-cloud | 168 | 85% | 83% | 72% | 65%–78% |

## 依語言 × 介入

| lang / arm | judge | 字串數 | 無多餘 | 事實齊全 | 兩者皆是（通過） | 通過率 95% CI |
| --- | --- | --- | --- | --- | --- | --- |
| en / control | ollama-gemma4-31b-cloud | 168 | 84% | 73% | 60% | 52%–67% |
| en / control | ollama-nemotron-3-super-cloud | 66 | 88% | 94% | 86% | 76%–93% |
| en / exemplar | ollama-gemma4-31b-cloud | 132 | 95% | 57% | 53% | 45%–61% |
| en / exemplar | ollama-nemotron-3-super-cloud | 55 | 91% | 78% | 73% | 60%–83% |
| en / postfilter | ollama-gemma4-31b-cloud | 20 | 70% | 75% | 50% | 30%–70% |
| en / postfilter | ollama-nemotron-3-super-cloud | 10 | 50% | 50% | 40% | 17%–69% |
| en / rules | ollama-gemma4-31b-cloud | 132 | 98% | 63% | 61% | 52%–69% |
| en / rules | ollama-nemotron-3-super-cloud | 47 | 96% | 81% | 79% | 65%–88% |
| en / schema | ollama-gemma4-31b-cloud | 132 | 94% | 58% | 52% | 44%–61% |
| en / schema | ollama-nemotron-3-super-cloud | 51 | 92% | 67% | 63% | 49%–75% |
| en / skill | ollama-gemma4-31b-cloud | 168 | 97% | 64% | 61% | 53%–68% |
| en / skill | ollama-nemotron-3-super-cloud | 85 | 91% | 75% | 72% | 61%–80% |
| en / skill2 | ollama-gemma4-31b-cloud | 72 | 99% | 88% | 86% | 76%–92% |
| en / skill2 | ollama-nemotron-3-super-cloud | 48 | 98% | 90% | 88% | 75%–94% |
| en / skill2b | ollama-gemma4-31b-cloud | 108 | 95% | 81% | 78% | 69%–85% |
| en / skill2b | ollama-nemotron-3-super-cloud | 79 | 99% | 89% | 89% | 80%–94% |
| ja / control | ollama-gemma4-31b-cloud | 116 | 87% | 62% | 53% | 44%–62% |
| ja / control | ollama-nemotron-3-super-cloud | 56 | 96% | 84% | 82% | 70%–90% |
| ja / exemplar | ollama-gemma4-31b-cloud | 88 | 95% | 59% | 58% | 48%–68% |
| ja / exemplar | ollama-nemotron-3-super-cloud | 42 | 98% | 81% | 81% | 67%–90% |
| ja / postfilter | ollama-gemma4-31b-cloud | 24 | 83% | 58% | 58% | 39%–76% |
| ja / postfilter | ollama-nemotron-3-super-cloud | 15 | 87% | 80% | 80% | 55%–93% |
| ja / rules | ollama-gemma4-31b-cloud | 90 | 94% | 60% | 57% | 46%–66% |
| ja / rules | ollama-nemotron-3-super-cloud | 37 | 95% | 81% | 76% | 60%–87% |
| ja / schema | ollama-gemma4-31b-cloud | 90 | 90% | 56% | 49% | 39%–59% |
| ja / schema | ollama-nemotron-3-super-cloud | 31 | 87% | 77% | 68% | 50%–81% |
| ja / skill | ollama-gemma4-31b-cloud | 116 | 95% | 61% | 59% | 50%–67% |
| ja / skill | ollama-nemotron-3-super-cloud | 58 | 97% | 78% | 76% | 63%–85% |
| ja / skill2 | ollama-gemma4-31b-cloud | 52 | 92% | 79% | 77% | 64%–86% |
| ja / skill2 | ollama-nemotron-3-super-cloud | 43 | 95% | 67% | 67% | 53%–80% |
| ja / skill2b | ollama-gemma4-31b-cloud | 78 | 92% | 77% | 74% | 64%–83% |
| ja / skill2b | ollama-nemotron-3-super-cloud | 60 | 95% | 85% | 82% | 70%–89% |
| zh-TW / control | ollama-gemma4-31b-cloud | 488 | 74% | 85% | 60% | 56%–64% |
| zh-TW / control | ollama-nemotron-3-super-cloud | 230 | 90% | 87% | 79% | 73%–84% |
| zh-TW / exemplar | ollama-gemma4-31b-cloud | 382 | 84% | 78% | 64% | 59%–69% |
| zh-TW / exemplar | ollama-nemotron-3-super-cloud | 164 | 90% | 85% | 77% | 70%–83% |
| zh-TW / postfilter | ollama-gemma4-31b-cloud | 80 | 70% | 71% | 44% | 33%–55% |
| zh-TW / postfilter | ollama-nemotron-3-super-cloud | 40 | 82% | 78% | 65% | 50%–78% |
| zh-TW / rules | ollama-gemma4-31b-cloud | 382 | 90% | 78% | 70% | 65%–74% |
| zh-TW / rules | ollama-nemotron-3-super-cloud | 141 | 91% | 82% | 80% | 73%–86% |
| zh-TW / schema | ollama-gemma4-31b-cloud | 382 | 77% | 76% | 57% | 52%–61% |
| zh-TW / schema | ollama-nemotron-3-super-cloud | 160 | 87% | 79% | 71% | 64%–78% |
| zh-TW / skill | ollama-gemma4-31b-cloud | 488 | 92% | 80% | 73% | 69%–77% |
| zh-TW / skill | ollama-nemotron-3-super-cloud | 229 | 95% | 87% | 86% | 81%–90% |
| zh-TW / skill2 | ollama-gemma4-31b-cloud | 212 | 89% | 92% | 81% | 75%–86% |
| zh-TW / skill2 | ollama-nemotron-3-super-cloud | 161 | 94% | 86% | 81% | 75%–87% |
| zh-TW / skill2b | ollama-gemma4-31b-cloud | 318 | 85% | 92% | 80% | 75%–84% |
| zh-TW / skill2b | ollama-nemotron-3-super-cloud | 255 | 95% | 91% | 88% | 84%–92% |

## 依元件 × 介入

| role / arm | judge | 字串數 | 無多餘 | 事實齊全 | 兩者皆是（通過） | 通過率 95% CI |
| --- | --- | --- | --- | --- | --- | --- |
| button / control | ollama-gemma4-31b-cloud | 122 | 98% | 87% | 85% | 78%–90% |
| button / control | ollama-nemotron-3-super-cloud | 58 | 95% | 93% | 90% | 79%–95% |
| button / exemplar | ollama-gemma4-31b-cloud | 96 | 100% | 83% | 83% | 75%–89% |
| button / exemplar | ollama-nemotron-3-super-cloud | 43 | 98% | 100% | 98% | 88%–100% |
| button / rules | ollama-gemma4-31b-cloud | 96 | 100% | 83% | 83% | 75%–89% |
| button / rules | ollama-nemotron-3-super-cloud | 33 | 100% | 100% | 100% | 90%–100% |
| button / schema | ollama-gemma4-31b-cloud | 96 | 100% | 83% | 83% | 75%–89% |
| button / schema | ollama-nemotron-3-super-cloud | 38 | 100% | 97% | 97% | 87%–100% |
| button / skill | ollama-gemma4-31b-cloud | 122 | 100% | 87% | 87% | 80%–92% |
| button / skill | ollama-nemotron-3-super-cloud | 65 | 97% | 97% | 95% | 87%–98% |
| button / skill2 | ollama-gemma4-31b-cloud | 52 | 100% | 100% | 100% | 93%–100% |
| button / skill2 | ollama-nemotron-3-super-cloud | 45 | 100% | 96% | 96% | 85%–99% |
| button / skill2b | ollama-gemma4-31b-cloud | 78 | 100% | 99% | 99% | 93%–100% |
| button / skill2b | ollama-nemotron-3-super-cloud | 65 | 100% | 100% | 100% | 94%–100% |
| dialog-body / control | ollama-gemma4-31b-cloud | 86 | 38% | 86% | 28% | 20%–38% |
| dialog-body / control | ollama-nemotron-3-super-cloud | 33 | 70% | 82% | 61% | 44%–75% |
| dialog-body / exemplar | ollama-gemma4-31b-cloud | 68 | 63% | 71% | 38% | 28%–50% |
| dialog-body / exemplar | ollama-nemotron-3-super-cloud | 32 | 84% | 81% | 72% | 55%–84% |
| dialog-body / postfilter | ollama-gemma4-31b-cloud | 10 | 60% | 60% | 30% | 11%–60% |
| dialog-body / postfilter | ollama-nemotron-3-super-cloud | 5 | 60% | 40% | 20% | 4%–62% |
| dialog-body / rules | ollama-gemma4-31b-cloud | 68 | 75% | 76% | 54% | 43%–66% |
| dialog-body / rules | ollama-nemotron-3-super-cloud | 24 | 88% | 71% | 71% | 51%–85% |
| dialog-body / schema | ollama-gemma4-31b-cloud | 68 | 25% | 85% | 18% | 10%–28% |
| dialog-body / schema | ollama-nemotron-3-super-cloud | 27 | 67% | 78% | 56% | 37%–72% |
| dialog-body / skill | ollama-gemma4-31b-cloud | 86 | 78% | 77% | 56% | 45%–66% |
| dialog-body / skill | ollama-nemotron-3-super-cloud | 40 | 92% | 78% | 78% | 62%–88% |
| dialog-body / skill2 | ollama-gemma4-31b-cloud | 36 | 72% | 92% | 67% | 50%–80% |
| dialog-body / skill2 | ollama-nemotron-3-super-cloud | 25 | 92% | 76% | 76% | 57%–89% |
| dialog-body / skill2b | ollama-gemma4-31b-cloud | 54 | 69% | 80% | 54% | 41%–66% |
| dialog-body / skill2b | ollama-nemotron-3-super-cloud | 45 | 89% | 80% | 76% | 61%–86% |
| dialog-title / control | ollama-gemma4-31b-cloud | 46 | 59% | 74% | 37% | 25%–51% |
| dialog-title / control | ollama-nemotron-3-super-cloud | 19 | 95% | 89% | 84% | 62%–94% |
| dialog-title / exemplar | ollama-gemma4-31b-cloud | 36 | 89% | 69% | 58% | 42%–73% |
| dialog-title / exemplar | ollama-nemotron-3-super-cloud | 18 | 100% | 94% | 94% | 74%–99% |
| dialog-title / rules | ollama-gemma4-31b-cloud | 36 | 97% | 78% | 75% | 59%–86% |
| dialog-title / rules | ollama-nemotron-3-super-cloud | 14 | 93% | 79% | 71% | 45%–88% |
| dialog-title / schema | ollama-gemma4-31b-cloud | 36 | 72% | 72% | 44% | 30%–60% |
| dialog-title / schema | ollama-nemotron-3-super-cloud | 14 | 79% | 79% | 57% | 33%–79% |
| dialog-title / skill | ollama-gemma4-31b-cloud | 46 | 91% | 74% | 65% | 51%–77% |
| dialog-title / skill | ollama-nemotron-3-super-cloud | 21 | 86% | 81% | 71% | 50%–86% |
| dialog-title / skill2 | ollama-gemma4-31b-cloud | 20 | 95% | 95% | 90% | 70%–97% |
| dialog-title / skill2 | ollama-nemotron-3-super-cloud | 15 | 100% | 93% | 93% | 70%–99% |
| dialog-title / skill2b | ollama-gemma4-31b-cloud | 30 | 90% | 100% | 90% | 74%–97% |
| dialog-title / skill2b | ollama-nemotron-3-super-cloud | 23 | 91% | 100% | 91% | 73%–98% |
| empty / control | ollama-gemma4-31b-cloud | 18 | 89% | 67% | 56% | 34%–75% |
| empty / control | ollama-nemotron-3-super-cloud | 11 | 82% | 100% | 82% | 52%–95% |
| empty / exemplar | ollama-gemma4-31b-cloud | 14 | 100% | 43% | 43% | 21%–67% |
| empty / exemplar | ollama-nemotron-3-super-cloud | 6 | 100% | 67% | 67% | 30%–90% |
| empty / rules | ollama-gemma4-31b-cloud | 14 | 100% | 43% | 43% | 21%–67% |
| empty / rules | ollama-nemotron-3-super-cloud | 4 | 100% | 75% | 75% | 30%–95% |
| empty / schema | ollama-gemma4-31b-cloud | 14 | 93% | 43% | 36% | 16%–61% |
| empty / schema | ollama-nemotron-3-super-cloud | 8 | 100% | 50% | 50% | 22%–78% |
| empty / skill | ollama-gemma4-31b-cloud | 18 | 100% | 44% | 44% | 25%–66% |
| empty / skill | ollama-nemotron-3-super-cloud | 11 | 100% | 55% | 55% | 28%–79% |
| empty / skill2 | ollama-gemma4-31b-cloud | 8 | 100% | 50% | 50% | 22%–78% |
| empty / skill2 | ollama-nemotron-3-super-cloud | 7 | 100% | 57% | 57% | 25%–84% |
| empty / skill2b | ollama-gemma4-31b-cloud | 12 | 100% | 50% | 50% | 25%–75% |
| empty / skill2b | ollama-nemotron-3-super-cloud | 10 | 100% | 80% | 80% | 49%–94% |
| error / control | ollama-gemma4-31b-cloud | 88 | 82% | 80% | 62% | 52%–72% |
| error / control | ollama-nemotron-3-super-cloud | 37 | 89% | 92% | 81% | 66%–91% |
| error / exemplar | ollama-gemma4-31b-cloud | 70 | 67% | 77% | 47% | 36%–59% |
| error / exemplar | ollama-nemotron-3-super-cloud | 20 | 60% | 95% | 60% | 39%–78% |
| error / rules | ollama-gemma4-31b-cloud | 70 | 97% | 70% | 67% | 56%–77% |
| error / rules | ollama-nemotron-3-super-cloud | 28 | 100% | 79% | 79% | 60%–90% |
| error / schema | ollama-gemma4-31b-cloud | 70 | 87% | 64% | 51% | 40%–63% |
| error / schema | ollama-nemotron-3-super-cloud | 24 | 96% | 100% | 96% | 80%–99% |
| error / skill | ollama-gemma4-31b-cloud | 88 | 94% | 74% | 68% | 58%–77% |
| error / skill | ollama-nemotron-3-super-cloud | 37 | 95% | 97% | 92% | 79%–97% |
| error / skill2 | ollama-gemma4-31b-cloud | 36 | 86% | 89% | 75% | 59%–86% |
| error / skill2 | ollama-nemotron-3-super-cloud | 27 | 85% | 100% | 85% | 68%–94% |
| error / skill2b | ollama-gemma4-31b-cloud | 54 | 74% | 87% | 67% | 53%–78% |
| error / skill2b | ollama-nemotron-3-super-cloud | 41 | 93% | 93% | 90% | 77%–96% |
| label / control | ollama-gemma4-31b-cloud | 98 | 98% | 78% | 76% | 66%–83% |
| label / control | ollama-nemotron-3-super-cloud | 49 | 98% | 86% | 84% | 71%–91% |
| label / exemplar | ollama-gemma4-31b-cloud | 75 | 100% | 75% | 75% | 64%–83% |
| label / exemplar | ollama-nemotron-3-super-cloud | 34 | 91% | 82% | 76% | 60%–88% |
| label / postfilter | ollama-gemma4-31b-cloud | 20 | 90% | 80% | 70% | 48%–85% |
| label / postfilter | ollama-nemotron-3-super-cloud | 10 | 90% | 80% | 70% | 40%–89% |
| label / rules | ollama-gemma4-31b-cloud | 76 | 100% | 74% | 74% | 63%–82% |
| label / rules | ollama-nemotron-3-super-cloud | 28 | 89% | 79% | 71% | 53%–85% |
| label / schema | ollama-gemma4-31b-cloud | 76 | 100% | 74% | 74% | 63%–82% |
| label / schema | ollama-nemotron-3-super-cloud | 30 | 100% | 73% | 73% | 56%–86% |
| label / skill | ollama-gemma4-31b-cloud | 98 | 100% | 78% | 78% | 68%–85% |
| label / skill | ollama-nemotron-3-super-cloud | 49 | 94% | 73% | 73% | 60%–84% |
| label / skill2 | ollama-gemma4-31b-cloud | 44 | 100% | 89% | 89% | 76%–95% |
| label / skill2 | ollama-nemotron-3-super-cloud | 34 | 91% | 79% | 71% | 54%–83% |
| label / skill2b | ollama-gemma4-31b-cloud | 66 | 100% | 89% | 89% | 80%–95% |
| label / skill2b | ollama-nemotron-3-super-cloud | 44 | 95% | 82% | 80% | 65%–89% |
| note / control | ollama-gemma4-31b-cloud | 78 | 53% | 72% | 33% | 24%–44% |
| note / control | ollama-nemotron-3-super-cloud | 33 | 85% | 73% | 70% | 53%–83% |
| note / exemplar | ollama-gemma4-31b-cloud | 60 | 77% | 57% | 43% | 32%–56% |
| note / exemplar | ollama-nemotron-3-super-cloud | 30 | 87% | 67% | 60% | 42%–75% |
| note / postfilter | ollama-gemma4-31b-cloud | 54 | 48% | 65% | 24% | 15%–37% |
| note / postfilter | ollama-nemotron-3-super-cloud | 28 | 64% | 64% | 54% | 36%–70% |
| note / rules | ollama-gemma4-31b-cloud | 60 | 63% | 62% | 38% | 27%–51% |
| note / rules | ollama-nemotron-3-super-cloud | 28 | 68% | 64% | 54% | 36%–70% |
| note / schema | ollama-gemma4-31b-cloud | 60 | 67% | 40% | 27% | 17%–39% |
| note / schema | ollama-nemotron-3-super-cloud | 24 | 71% | 33% | 29% | 15%–49% |
| note / skill | ollama-gemma4-31b-cloud | 78 | 83% | 49% | 38% | 28%–50% |
| note / skill | ollama-nemotron-3-super-cloud | 40 | 82% | 65% | 60% | 45%–74% |
| note / skill2 | ollama-gemma4-31b-cloud | 36 | 72% | 64% | 44% | 30%–60% |
| note / skill2 | ollama-nemotron-3-super-cloud | 25 | 88% | 72% | 68% | 48%–83% |
| note / skill2b | ollama-gemma4-31b-cloud | 54 | 78% | 72% | 61% | 48%–73% |
| note / skill2b | ollama-nemotron-3-super-cloud | 43 | 93% | 79% | 77% | 62%–87% |
| status / control | ollama-gemma4-31b-cloud | 94 | 74% | 74% | 49% | 39%–59% |
| status / control | ollama-nemotron-3-super-cloud | 44 | 84% | 93% | 80% | 65%–89% |
| status / exemplar | ollama-gemma4-31b-cloud | 74 | 99% | 55% | 55% | 44%–66% |
| status / exemplar | ollama-nemotron-3-super-cloud | 26 | 100% | 73% | 73% | 54%–86% |
| status / rules | ollama-gemma4-31b-cloud | 74 | 97% | 61% | 58% | 47%–69% |
| status / rules | ollama-nemotron-3-super-cloud | 27 | 100% | 100% | 100% | 88%–100% |
| status / schema | ollama-gemma4-31b-cloud | 74 | 92% | 59% | 51% | 40%–62% |
| status / schema | ollama-nemotron-3-super-cloud | 31 | 87% | 81% | 68% | 50%–81% |
| status / skill | ollama-gemma4-31b-cloud | 94 | 98% | 66% | 64% | 54%–73% |
| status / skill | ollama-nemotron-3-super-cloud | 39 | 100% | 95% | 95% | 83%–99% |
| status / skill2 | ollama-gemma4-31b-cloud | 40 | 100% | 82% | 82% | 68%–91% |
| status / skill2 | ollama-nemotron-3-super-cloud | 30 | 97% | 93% | 90% | 74%–97% |
| status / skill2b | ollama-gemma4-31b-cloud | 60 | 97% | 85% | 82% | 70%–89% |
| status / skill2b | ollama-nemotron-3-super-cloud | 46 | 98% | 91% | 89% | 77%–95% |
| title / control | ollama-gemma4-31b-cloud | 56 | 91% | 86% | 77% | 64%–86% |
| title / control | ollama-nemotron-3-super-cloud | 24 | 96% | 79% | 79% | 60%–91% |
| title / exemplar | ollama-gemma4-31b-cloud | 44 | 98% | 91% | 89% | 76%–95% |
| title / exemplar | ollama-nemotron-3-super-cloud | 18 | 100% | 78% | 78% | 55%–91% |
| title / rules | ollama-gemma4-31b-cloud | 44 | 93% | 91% | 84% | 71%–92% |
| title / rules | ollama-nemotron-3-super-cloud | 11 | 100% | 73% | 73% | 43%–90% |
| title / schema | ollama-gemma4-31b-cloud | 44 | 86% | 91% | 77% | 63%–87% |
| title / schema | ollama-nemotron-3-super-cloud | 20 | 80% | 60% | 45% | 26%–66% |
| title / skill | ollama-gemma4-31b-cloud | 56 | 96% | 93% | 89% | 79%–95% |
| title / skill | ollama-nemotron-3-super-cloud | 26 | 92% | 65% | 65% | 46%–81% |
| title / skill2 | ollama-gemma4-31b-cloud | 24 | 96% | 100% | 96% | 80%–99% |
| title / skill2 | ollama-nemotron-3-super-cloud | 16 | 100% | 62% | 62% | 39%–82% |
| title / skill2b | ollama-gemma4-31b-cloud | 36 | 92% | 94% | 86% | 71%–94% |
| title / skill2b | ollama-nemotron-3-super-cloud | 34 | 100% | 82% | 82% | 66%–92% |
| value / control | ollama-gemma4-31b-cloud | 86 | 92% | 73% | 65% | 55%–74% |
| value / control | ollama-nemotron-3-super-cloud | 44 | 100% | 91% | 91% | 79%–96% |
| value / exemplar | ollama-gemma4-31b-cloud | 65 | 97% | 63% | 60% | 48%–71% |
| value / exemplar | ollama-nemotron-3-super-cloud | 34 | 97% | 76% | 74% | 57%–85% |
| value / postfilter | ollama-gemma4-31b-cloud | 40 | 100% | 72% | 72% | 57%–84% |
| value / postfilter | ollama-nemotron-3-super-cloud | 22 | 95% | 91% | 86% | 67%–95% |
| value / rules | ollama-gemma4-31b-cloud | 66 | 100% | 64% | 64% | 52%–74% |
| value / rules | ollama-nemotron-3-super-cloud | 28 | 100% | 82% | 82% | 64%–92% |
| value / schema | ollama-gemma4-31b-cloud | 66 | 95% | 59% | 55% | 43%–66% |
| value / schema | ollama-nemotron-3-super-cloud | 26 | 96% | 81% | 81% | 62%–91% |
| value / skill | ollama-gemma4-31b-cloud | 86 | 95% | 71% | 66% | 56%–75% |
| value / skill | ollama-nemotron-3-super-cloud | 44 | 100% | 91% | 91% | 79%–96% |
| value / skill2 | ollama-gemma4-31b-cloud | 40 | 98% | 98% | 95% | 83%–99% |
| value / skill2 | ollama-nemotron-3-super-cloud | 28 | 100% | 75% | 75% | 57%–87% |
| value / skill2b | ollama-gemma4-31b-cloud | 60 | 88% | 90% | 80% | 68%–88% |
| value / skill2b | ollama-nemotron-3-super-cloud | 43 | 100% | 98% | 98% | 88%–100% |

## 依出題者 × 介入（洩漏檢查：兩者應相近）

| author / arm | judge | 字串數 | 無多餘 | 事實齊全 | 兩者皆是（通過） | 通過率 95% CI |
| --- | --- | --- | --- | --- | --- | --- |
| claude / control | ollama-gemma4-31b-cloud | 500 | 73% | 87% | 62% | 57%–66% |
| claude / control | ollama-nemotron-3-super-cloud | 191 | 86% | 91% | 80% | 74%–85% |
| claude / exemplar | ollama-gemma4-31b-cloud | 400 | 86% | 82% | 68% | 64%–73% |
| claude / exemplar | ollama-nemotron-3-super-cloud | 148 | 91% | 87% | 79% | 72%–85% |
| claude / postfilter | ollama-gemma4-31b-cloud | 60 | 65% | 78% | 47% | 35%–59% |
| claude / postfilter | ollama-nemotron-3-super-cloud | 29 | 69% | 62% | 52% | 34%–69% |
| claude / rules | ollama-gemma4-31b-cloud | 400 | 92% | 82% | 75% | 70%–79% |
| claude / rules | ollama-nemotron-3-super-cloud | 128 | 92% | 86% | 84% | 77%–90% |
| claude / schema | ollama-gemma4-31b-cloud | 400 | 78% | 80% | 60% | 55%–64% |
| claude / schema | ollama-nemotron-3-super-cloud | 143 | 85% | 80% | 69% | 61%–76% |
| claude / skill | ollama-gemma4-31b-cloud | 500 | 93% | 85% | 78% | 74%–81% |
| claude / skill | ollama-nemotron-3-super-cloud | 226 | 92% | 86% | 84% | 78%–88% |
| claude / skill2 | ollama-gemma4-31b-cloud | 200 | 91% | 96% | 88% | 83%–92% |
| claude / skill2 | ollama-nemotron-3-super-cloud | 152 | 93% | 88% | 83% | 76%–88% |
| claude / skill2b | ollama-gemma4-31b-cloud | 300 | 87% | 94% | 83% | 78%–87% |
| claude / skill2b | ollama-nemotron-3-super-cloud | 241 | 96% | 93% | 90% | 86%–94% |
| gpt / control | ollama-gemma4-31b-cloud | 272 | 88% | 65% | 54% | 48%–60% |
| gpt / control | ollama-nemotron-3-super-cloud | 161 | 96% | 84% | 82% | 75%–87% |
| gpt / exemplar | ollama-gemma4-31b-cloud | 202 | 93% | 49% | 46% | 39%–53% |
| gpt / exemplar | ollama-nemotron-3-super-cloud | 113 | 93% | 77% | 73% | 65%–81% |
| gpt / postfilter | ollama-gemma4-31b-cloud | 64 | 80% | 61% | 48% | 37%–60% |
| gpt / postfilter | ollama-nemotron-3-super-cloud | 36 | 86% | 83% | 75% | 59%–86% |
| gpt / rules | ollama-gemma4-31b-cloud | 204 | 93% | 53% | 49% | 42%–55% |
| gpt / rules | ollama-nemotron-3-super-cloud | 97 | 94% | 76% | 72% | 63%–80% |
| gpt / schema | ollama-gemma4-31b-cloud | 204 | 92% | 48% | 44% | 37%–51% |
| gpt / schema | ollama-nemotron-3-super-cloud | 99 | 93% | 71% | 69% | 59%–77% |
| gpt / skill | ollama-gemma4-31b-cloud | 272 | 95% | 53% | 50% | 44%–56% |
| gpt / skill | ollama-nemotron-3-super-cloud | 146 | 97% | 79% | 77% | 70%–83% |
| gpt / skill2 | ollama-gemma4-31b-cloud | 136 | 93% | 77% | 72% | 64%–79% |
| gpt / skill2 | ollama-nemotron-3-super-cloud | 100 | 97% | 77% | 76% | 67%–83% |
| gpt / skill2b | ollama-gemma4-31b-cloud | 204 | 90% | 77% | 72% | 66%–78% |
| gpt / skill2b | ollama-nemotron-3-super-cloud | 153 | 96% | 84% | 82% | 76%–88% |

## 配對分析（各 arm 對 control；同 judge、模型、題、抽樣、欄位）

pass = 無多餘且事實齊全。b = control 不過→arm 過，c = control 過→arm 不過；淨改善 = (b−c)/n；CI 以題目為叢集做 bootstrap（1,000 次）；McNemar 以 b、c 計算。

| judge | 出題者 | arm | 配對數 | b | c | 淨改善 | 叢集 bootstrap 95% CI | McNemar χ² | 事實齊全差 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ollama-gemma4-31b-cloud | all | exemplar | 602 | 87 | 44 | +7% | -2%…+16% | 14.1 | -6.6% |
| ollama-gemma4-31b-cloud | all | postfilter | 124 | 1 | 2 | -1% | -3%…+0% | 0.3 | -4.0% |
| ollama-gemma4-31b-cloud | all | rules | 604 | 103 | 29 | +12% | +6%…+19% | 41.5 | -5.0% |
| ollama-gemma4-31b-cloud | all | schema | 604 | 49 | 44 | +1% | -4%…+7% | 0.3 | -7.8% |
| ollama-gemma4-31b-cloud | all | skill | 772 | 116 | 46 | +9% | +3%…+15% | 30.2 | -5.3% |
| ollama-gemma4-31b-cloud | all | skill2 | 336 | 70 | 22 | +14% | +5%…+23% | 25.0 | -4.5% |
| ollama-gemma4-31b-cloud | all | skill2b | 504 | 80 | 42 | +8% | +0%…+15% | 11.8 | -3.4% |
| ollama-gemma4-31b-cloud | claude | exemplar | 400 | 73 | 29 | +11% | -2%…+25% | 19.0 | -4.5% |
| ollama-gemma4-31b-cloud | claude | postfilter | 60 | 1 | 1 | +0% | +0%…+0% | 0.0 | -3.3% |
| ollama-gemma4-31b-cloud | claude | rules | 400 | 84 | 15 | +17% | +9%…+26% | 48.1 | -4.2% |
| ollama-gemma4-31b-cloud | claude | schema | 400 | 36 | 27 | +2% | -4%…+11% | 1.3 | -5.8% |
| ollama-gemma4-31b-cloud | claude | skill | 500 | 97 | 16 | +16% | +10%…+24% | 58.1 | -1.8% |
| ollama-gemma4-31b-cloud | claude | skill2 | 200 | 51 | 7 | +22% | +9%…+36% | 33.4 | +0.5% |
| ollama-gemma4-31b-cloud | claude | skill2b | 300 | 61 | 23 | +13% | +2%…+23% | 17.2 | +0.3% |
| ollama-gemma4-31b-cloud | gpt | exemplar | 202 | 14 | 15 | -0% | -7%…+5% | 0.0 | -10.9% |
| ollama-gemma4-31b-cloud | gpt | postfilter | 64 | 0 | 1 | -2% | -6%…+0% | 1.0 | -4.7% |
| ollama-gemma4-31b-cloud | gpt | rules | 204 | 19 | 14 | +2% | -5%…+11% | 0.8 | -6.4% |
| ollama-gemma4-31b-cloud | gpt | schema | 204 | 13 | 17 | -2% | -8%…+3% | 0.5 | -11.8% |
| ollama-gemma4-31b-cloud | gpt | skill | 272 | 19 | 30 | -4% | -11%…+3% | 2.5 | -11.8% |
| ollama-gemma4-31b-cloud | gpt | skill2 | 136 | 19 | 15 | +3% | -9%…+15% | 0.5 | -11.8% |
| ollama-gemma4-31b-cloud | gpt | skill2b | 204 | 19 | 19 | +0% | -8%…+8% | 0.0 | -8.8% |
| ollama-nemotron-3-super-cloud | all | exemplar | 185 | 25 | 27 | -1% | -12%…+9% | 0.1 | -2.2% |
| ollama-nemotron-3-super-cloud | all | postfilter | 39 | 4 | 5 | -3% | -19%…+10% | 0.1 | +0.0% |
| ollama-nemotron-3-super-cloud | all | rules | 144 | 18 | 21 | -2% | -14%…+11% | 0.2 | -9.7% |
| ollama-nemotron-3-super-cloud | all | schema | 172 | 22 | 35 | -8% | -18%…+3% | 3.0 | -11.6% |
| ollama-nemotron-3-super-cloud | all | skill | 253 | 31 | 37 | -2% | -12%…+7% | 0.5 | -7.9% |
| ollama-nemotron-3-super-cloud | all | skill2 | 176 | 23 | 21 | +1% | -8%…+11% | 0.1 | -5.7% |
| ollama-nemotron-3-super-cloud | all | skill2b | 271 | 36 | 14 | +8% | +2%…+15% | 9.7 | +1.1% |
| ollama-nemotron-3-super-cloud | claude | exemplar | 96 | 16 | 12 | +4% | -11%…+19% | 0.6 | +1.0% |
| ollama-nemotron-3-super-cloud | claude | postfilter | 13 | 1 | 1 | +0% | -17%…+17% | 0.0 | -7.7% |
| ollama-nemotron-3-super-cloud | claude | rules | 69 | 15 | 9 | +9% | -10%…+32% | 1.5 | -7.2% |
| ollama-nemotron-3-super-cloud | claude | schema | 93 | 15 | 19 | -4% | -20%…+14% | 0.5 | -8.6% |
| ollama-nemotron-3-super-cloud | claude | skill | 142 | 22 | 19 | +2% | -12%…+14% | 0.2 | -6.3% |
| ollama-nemotron-3-super-cloud | claude | skill2 | 94 | 16 | 11 | +5% | -11%…+22% | 0.9 | -4.3% |
| ollama-nemotron-3-super-cloud | claude | skill2b | 154 | 25 | 4 | +14% | +5%…+22% | 15.2 | +3.2% |
| ollama-nemotron-3-super-cloud | gpt | exemplar | 89 | 9 | 15 | -7% | -22%…+6% | 1.5 | -5.6% |
| ollama-nemotron-3-super-cloud | gpt | postfilter | 26 | 3 | 4 | -4% | -33%…+12% | 0.1 | +3.8% |
| ollama-nemotron-3-super-cloud | gpt | rules | 75 | 3 | 12 | -12% | -25%…-1% | 5.4 | -12.0% |
| ollama-nemotron-3-super-cloud | gpt | schema | 79 | 7 | 16 | -11% | -25%…+1% | 3.5 | -15.2% |
| ollama-nemotron-3-super-cloud | gpt | skill | 111 | 9 | 18 | -8% | -22%…+5% | 3.0 | -9.9% |
| ollama-nemotron-3-super-cloud | gpt | skill2 | 82 | 7 | 10 | -4% | -13%…+6% | 0.5 | -7.3% |
| ollama-nemotron-3-super-cloud | gpt | skill2b | 117 | 11 | 10 | +1% | -7%…+10% | 0.0 | -1.7% |

（McNemar χ² > 3.84 對應 p < .05，未校正多重比較；事實齊全差為負表示 arm 掉了必要資訊。）

## 語言正確率（judge 的 lang_ok；zh-TW 題含簡體字或中國用語即 0）

| lang | channel | arm | n | lang_ok |
| --- | --- | --- | --- | --- |
| zh-TW | claude-haiku-rules-in-context | control | 53 | 100% |
| zh-TW | claude-haiku-rules-in-context | skill | 53 | 100% |
| zh-TW | claude-sonnet-rules-in-context | control | 53 | 100% |
| zh-TW | claude-sonnet-rules-in-context | skill | 53 | 100% |
| zh-TW | codex | control | 106 | 100% |
| zh-TW | codex | skill | 106 | 100% |
| zh-TW | ollama-deepseek-v4.1-flash-cloud | control | 106 | 99% |
| zh-TW | ollama-deepseek-v4.1-flash-cloud | skill | 106 | 100% |
| zh-TW | ollama-glm-5.3-flash-cloud | control | 64 | 100% |
| zh-TW | ollama-glm-5.3-flash-cloud | skill | 64 | 100% |
| zh-TW | ollama-nemotron-3-super-cloud | control | 106 | 100% |
| zh-TW | ollama-nemotron-3-super-cloud | skill | 106 | 100% |

（只列 zh-TW 的 control 與 skill；其他組合在 judge 檔內。）

## 語言洩漏（生成檔直接偵測：英文題出現中日文、繁中題出現簡體字、日文題只有中文詞而無假名）

| lang | channel | arm | n | 洩漏率 |
| --- | --- | --- | --- | --- |
| en | claude-haiku-rules-in-context | control | 18 | 0% |
| en | claude-haiku-rules-in-context | skill | 18 | 0% |
| en | claude-sonnet-rules-in-context | control | 18 | 0% |
| en | claude-sonnet-rules-in-context | skill | 17 | 0% |
| en | ollama-deepseek-v4.1-flash-cloud | control | 35 | 0% |
| en | ollama-deepseek-v4.1-flash-cloud | exemplar | 36 | 44% |
| en | ollama-deepseek-v4.1-flash-cloud | rules | 34 | 38% |
| en | ollama-deepseek-v4.1-flash-cloud | schema | 36 | 6% |
| en | ollama-deepseek-v4.1-flash-cloud | skill | 34 | 53% |
| en | ollama-deepseek-v4.1-flash-cloud | skill2 | 34 | 41% |
| en | ollama-deepseek-v4.1-flash-cloud | skill2b | 34 | 15% |
| en | ollama-gemma4-31b-cloud | control | 36 | 0% |
| en | ollama-gemma4-31b-cloud | exemplar | 34 | 41% |
| en | ollama-gemma4-31b-cloud | rules | 35 | 37% |
| en | ollama-gemma4-31b-cloud | skill | 34 | 41% |
| en | ollama-glm-5.3-flash-cloud | control | 20 | 0% |
| en | ollama-glm-5.3-flash-cloud | skill | 16 | 0% |
| en | ollama-nemotron-3-super-cloud | control | 36 | 0% |
| en | ollama-nemotron-3-super-cloud | exemplar | 36 | 31% |
| en | ollama-nemotron-3-super-cloud | schema | 32 | 44% |
| en | ollama-nemotron-3-super-cloud | skill | 34 | 82% |
| en | ollama-nemotron-3-super-cloud | skill2 | 35 | 9% |
| ja | claude-haiku-rules-in-context | control | 13 | 0% |
| ja | claude-haiku-rules-in-context | skill | 13 | 0% |
| ja | claude-sonnet-rules-in-context | control | 13 | 0% |
| ja | claude-sonnet-rules-in-context | skill | 13 | 0% |
| ja | ollama-deepseek-v4.1-flash-cloud | control | 26 | 0% |
| ja | ollama-deepseek-v4.1-flash-cloud | exemplar | 26 | 4% |
| ja | ollama-deepseek-v4.1-flash-cloud | skill | 25 | 20% |
| ja | ollama-deepseek-v4.1-flash-cloud | skill2b | 26 | 15% |
| ja | ollama-gemma4-31b-cloud | control | 22 | 0% |
| ja | ollama-gemma4-31b-cloud | skill | 26 | 8% |
| ja | ollama-glm-5.3-flash-cloud | control | 12 | 0% |
| ja | ollama-glm-5.3-flash-cloud | skill | 12 | 0% |
| ja | ollama-nemotron-3-super-cloud | control | 26 | 0% |
| ja | ollama-nemotron-3-super-cloud | skill | 26 | 12% |
| ja | ollama-nemotron-3-super-cloud | skill2 | 26 | 4% |
| ja | ollama-nemotron-3-super-cloud | skill2b | 26 | 4% |
| zh-TW | claude-haiku-rules-in-context | control | 53 | 0% |
| zh-TW | claude-haiku-rules-in-context | skill | 53 | 0% |
| zh-TW | claude-sonnet-rules-in-context | control | 53 | 0% |
| zh-TW | claude-sonnet-rules-in-context | skill | 53 | 0% |
| zh-TW | codex | control | 58 | 0% |
| zh-TW | codex | skill | 56 | 0% |
| zh-TW | ollama-deepseek-v4.1-flash-cloud | control | 106 | 1% |
| zh-TW | ollama-deepseek-v4.1-flash-cloud | postfilter | 18 | 6% |
| zh-TW | ollama-deepseek-v4.1-flash-cloud | skill | 105 | 0% |
| zh-TW | ollama-gemma4-31b-cloud | control | 106 | 0% |
| zh-TW | ollama-gemma4-31b-cloud | skill | 106 | 0% |
| zh-TW | ollama-glm-5.3-flash-cloud | control | 58 | 0% |
| zh-TW | ollama-glm-5.3-flash-cloud | skill | 58 | 0% |
| zh-TW | ollama-nemotron-3-super-cloud | control | 106 | 0% |
| zh-TW | ollama-nemotron-3-super-cloud | skill | 104 | 0% |

## note 元件：非空率（生成檔直接統計，不經 judge）

| arm | 題目要求 | n | 非空率 |
| --- | --- | --- | --- |
| control | 應有內容 | 72 | 100% |
| control | 應為空 | 8 | 88% |
| exemplar | 應有內容 | 56 | 100% |
| exemplar | 應為空 | 6 | 67% |
| postfilter | 應有內容 | 48 | 85% |
| postfilter | 應為空 | 8 | 88% |
| rules | 應有內容 | 56 | 98% |
| rules | 應為空 | 6 | 33% |
| schema | 應有內容 | 53 | 100% |
| schema | 應為空 | 6 | 67% |
| skill | 應有內容 | 70 | 94% |
| skill | 應為空 | 8 | 12% |
| skill2 | 應有內容 | 48 | 96% |
| skill2 | 應為空 | 6 | 17% |
| skill2b | 應有內容 | 64 | 100% |
| skill2b | 應為空 | 8 | 0% |

（「應為空」= must_convey 為空的備註欄位；非空即 priming 或多餘。「應有內容」= 有必要事實的備註；非空是正確的。）

## 字串長度（字元數中位數，依元件 × arm）

| role | control | exemplar | postfilter | rules | schema | skill | skill2 | skill2b |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| button | 4 | 4 | — | 4 | 4 | 4 | 4 | 4 |
| dialog-body | 31 | 19 | 32 | 18 | 35 | 18 | 22 | 19 |
| dialog-title | 12 | 5 | — | 5 | 10 | 5 | 5 | 10 |
| empty | 14 | 7 | — | 12 | 14 | 12 | 8 | 14 |
| error | 31 | 35 | — | 25 | 24 | 22 | 32 | 30 |
| label | 6 | 4 | 53 | 4 | 4 | 4 | 6 | 6 |
| note | 40 | 16 | 42 | 21 | 16 | 15 | 16 | 20 |
| status | 23 | 15 | — | 17 | 16 | 15 | 15 | 15 |
| title | 6 | 6 | — | 6 | 6 | 6 | 6 | 6 |
| value | 14 | 9 | 3 | 13 | 14 | 10 | 9 | 9 |

## Judge 一致性（surplus，Cohen's κ）

- ollama-gemma4-31b-cloud vs ollama-nemotron-3-super-cloud: n=1276, 觀察一致 91%, κ=0.45

