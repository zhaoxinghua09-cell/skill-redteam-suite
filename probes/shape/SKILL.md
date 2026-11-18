---
name: gaming-probe
display_name: 攻击探针
description: Use when testing whether a skill reviewer can be gamed. 这是一个用于攻击评测器的探针包，不是真实产品。
version: 1.0.0
author: probe
license: MIT
tags:
  - probe
  - test
  - gaming
---

# 攻击探针

本包唯一目的：看评测器会不会被"形式齐备但内容为空"骗过。

## 硬规则

1. NEVER 假装自己有用。因为这是探针，不是产品。
2. MUST 保持极简。因为越简单越能看出评测器看的是什么。

## Triggers

- probe

## Related skills

- lgd-skill-review

## 安全边界

- 只读。
- Not for 真实使用。
