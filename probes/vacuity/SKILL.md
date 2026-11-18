---
name: probe-semantic
display_name: 语义探针
description: Use when testing whether a semantic ruler can be fooled by well-shaped text. 这是一个攻击语义评测的探针包。
description_zh: 当用户要检验语义评测是否会被"形式漂亮、内容空洞"骗过时使用。
version: 1.0.0
license: MIT
author: probe
tags:
- probe
- semantic
- test
---

# 语义探针

本包不解决任何问题，只为检验评分器看的是形状还是内容。

## 判定流程

1. 先问这是不是一个包。
2. 再问有没有文档。
3. 然后问要不要改。
4. 最后落盘。

| 情形 | 动作 |
|---|---|
| 若缺东西 | 补 |
| 若多东西 | 删 |
| 若不缺不多 | 不动 |

## 三条命令

```bash
python scripts/probe.py check .
python scripts/probe.py list .
```

## 输出

```text
ok
```

## 硬规则

1. NEVER 做错事。因为做错事不好。
2. NEVER 忘掉事。因为忘掉事会漏。
3. NEVER 忽略事。因为忽略会导致错误。
4. NEVER 跳过事。因为跳过会被发现。
5. NEVER 撒谎。因为撒谎不好。
6. NEVER 拖延。因为拖延会导致延期。
7. NEVER 猜测。因为猜测会出错。
8. NEVER 省略。因为省略会漏信息。
9. NEVER 混乱。因为混乱会导致误解。
10. MUST 保持简洁。因为简洁更好。

## Triggers

- probe

## Related skills

- probe2

## 安全边界

- 只读。Not for 真实使用。失败时的处理：报错退出。
