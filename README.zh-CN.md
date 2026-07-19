# SecretTrail Graph

SecretTrail Graph 将同一 secret 在提交、CI 日志与制品中的出现串成时间线，帮助安全与平台团队定位可能根因和完整清理范围。

## 快速开始

```bash
python -m pip install -e '.[dev]'
make demo
```

演示会生成离线可查看的 `dist-release/demo-report.html`。报告仅保留不可逆指纹和掩码片段，不输出原始 token。

## 功能

- 导入 Gitleaks、Trivy、Git log JSON 与制品清单。
- 还原传播、重复出现、首次与最后出现的时间线。
- 生成根因候选、影响范围和修复清单。
- 使用随仓库提交的虚构 token 完全离线复现四条路径和两次复发。

## 使用

```bash
python -m leakloom.cli analyze --gitleaks examples/gitleaks.json --trivy examples/trivy.json --git-log examples/git-log.json --artifacts examples/artifacts.json --workspace examples/current --html report.html --json report.json
```

移除 `examples/current/active.txt` 内的样例 token 后再次扫描会显示 `resolved`。该工具不替代凭据轮换、历史清理或保密库。

更多英文说明见 [README.md](README.md)，包括架构、测试、隐私边界、竞品差异和贡献方式。
