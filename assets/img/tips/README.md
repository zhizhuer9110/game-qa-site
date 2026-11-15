# 交付物示例图（占位）

用于「04 交付保障」列表中带虚线 / 红点的文字：桌面鼠标悬停、键盘 Tab 聚焦、手机轻触时弹出预览。

## 文件对应

| 文件 | 触发文字 |
| --- | --- |
| `test-plan.jpg` | 测试计划 |
| `daily-report.jpg` | 测试日报 |
| `weekly-report.jpg` | 周报推送 |
| `test-report.jpg` | 测试报告 |
| `bug-list.jpg` | bug 清单 |
| `process-docs.jpg` | 过程文档 |
| `special-report.jpg` | 专项测试报告 |
| `quality-report.jpg` | 版本质量评估报告 |
| `test-cases.jpg` | 测试用例库 |
| `automation.jpg` | 自动化脚本沉淀 |
| `retro.jpg` | 线上问题复盘与改进建议 |

## 替换图片

直接用同名图片覆盖即可，**不需要改 HTML**。建议：

- 尺寸 `900 × 560`（16:10），JPG / WebP，单张 < 200 KB。
- 当前样式按 900:560 居中裁切；其他比例会被裁掉边缘。
- 需要重新生成占位图：`python3 tools/make-tip-placeholders.py`。

## 新增触发项

在 `index.html` 中给文字包一层按钮：

```html
<button class="doc-tip" type="button"
  data-tip="assets/img/tips/xxx.jpg"
  data-tip-title="图片说明"
  aria-haspopup="dialog" aria-expanded="false">要显示的文字</button>
```

图片预览的弹层、定位、触摸关闭等交互由 `assets/js/main.js` 统一处理。
