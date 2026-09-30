# ui-microcopy 對照組結果

執行時間：2026-09-30 21:05

| 模型 / 管道 | 組別 | 通過 probe | 禁止樣式命中 | linter error 筆數 |
| --- | --- | --- | --- | --- |
| cloakgpt-gpt-web | control | 1/1 | 0 | 0 |
| codex-gpt | control | 5/9 | 7 | 1 |
| codex-gpt | patched | 1/1 | 0 | 0 |
| codex-gpt | rules | 4/9 | 1 | 1 |
| codex-gpt | skill | 8/9 | 0 | 0 |
| ollama-deepseek-v4.1-flash | control | 4/9 | 6 | 0 |
| ollama-deepseek-v4.1-flash | patched | 1/1 | 0 | 0 |
| ollama-deepseek-v4.1-flash | rules | 6/9 | 3 | 1 |
| ollama-deepseek-v4.1-flash | skill | 8/9 | 0 | 0 |
| ollama-gemma4:31b-cloud | control | 3/9 | 10 | 4 |
| ollama-gemma4:31b-cloud | patched | 1/1 | 0 | 0 |
| ollama-gemma4:31b-cloud | rules | 5/9 | 1 | 1 |
| ollama-gemma4:31b-cloud | skill | 9/9 | 0 | 0 |
| ollama-glm-5.3-flash:cloud | control | 4/9 | 8 | 3 |
| ollama-glm-5.3-flash:cloud | patched | 1/1 | 0 | 0 |
| ollama-glm-5.3-flash:cloud | rules | 4/9 | 4 | 1 |
| ollama-glm-5.3-flash:cloud | skill | 8/9 | 0 | 0 |
| ollama-nemotron-3-super:cloud | control | 2/9 | 10 | 3 |
| ollama-nemotron-3-super:cloud | patched | 1/1 | 0 | 0 |
| ollama-nemotron-3-super:cloud | rules | 7/9 | 2 | 0 |
| ollama-nemotron-3-super:cloud | skill | 7/9 | 2 | 0 |
| subagent-gpt-6-luna | control | 2/3 | 1 | 1 |
| subagent-gpt-6-luna | skill | 3/3 | 0 | 0 |

## 逐題結果

| probe | cloakgpt-gpt-web | codex-gpt | ollama-deepseek-v4.1-flash | ollama-gemma4:31b-cloud | ollama-glm-5.3-flash:cloud | ollama-nemotron-3-super:cloud | subagent-gpt-6-luna |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | C✓ | C✓ R✗ S✗ | C✓ R✓ S✓ | C✗ R✗ S✓ | C✓ R✗ S✗ | C✗ R✗ S✓ | C✓ S✓ |
| P2 | — | C✓ R✓ S✓ | C✓ R✓ S✓ | C✓ R✓ S✓ | C✓ R✓ S✓ | C✓ R✓ S✓ | — |
| P3 | — | P✓ C✗ R✓ S✓ | P✓ C✗ R✗ S✓ | P✓ C✗ R✓ S✓ | P✓ C✗ R✗ S✓ | P✓ C✗ R✗ S✓ | C✓ S✓ |
| P4 | — | C✓ R✗ S✓ | C✗ R✓ S✓ | C✗ R✗ S✓ | C✗ R✓ S✓ | C✗ R✓ S✓ | — |
| P5 | — | C✗ R✓ S✓ | C✗ R✓ S✓ | C✗ R✓ S✓ | C✗ R✓ S✓ | C✗ R✓ S✗ | — |
| P6 | — | C✗ R✓ S✓ | C✗ R✓ S✓ | C✗ R✓ S✓ | C✗ R✓ S✓ | C✗ R✓ S✓ | — |
| P7 | — | C✗ R✗ S✓ | C✓ R✗ S✓ | C✓ R✗ S✓ | C✓ R✗ S✓ | C✓ R✓ S✓ | C✗ S✓ |
| P8 | — | C✓ R✗ S✓ | C✓ R✓ S✓ | C✗ R✓ S✓ | C✗ R✗ S✓ | C✗ R✓ S✓ | — |
| P9 | — | C✓ R✗ S✓ | C✗ R✗ S✗ | C✓ R✗ S✓ | C✓ R✗ S✓ | C✗ R✓ S✗ | — |

C = control（只給任務）、R = rules（專案既有規則）、S = skill（ui-microcopy）、P = patched（修訂後的 app 內 prompt）。
