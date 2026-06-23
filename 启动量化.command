#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="/Users/qml/Desktop/workspace/quant-fund-lab"
cd "$PROJECT_DIR"

if [[ -t 1 ]]; then
  clear
fi
echo "Quant Fund Lab 快捷启动"
echo "项目目录: $PROJECT_DIR"
echo

run_cmd() {
  echo
  echo "运行: $*"
  echo
  "$@"
}

case "${1:-menu}" in
  app)
    run_cmd uv run python app/main.py
    ;;
  demo)
    run_cmd uv run qfl-market-demo
    ;;
  jupyter)
    run_cmd uv run jupyter lab
    ;;
  ui)
    run_cmd uv run qfl-ui
    ;;
  data)
    run_cmd uv run qfl-demo-data
    ;;
  live-data)
    run_cmd uv run qfl-data
    ;;
  backtest)
    run_cmd uv run qfl-backtest
    ;;
  signal)
    run_cmd uv run qfl-signal
    ;;
  test)
    run_cmd uv run pytest
    ;;
  menu)
    echo "请选择要执行的操作:"
    echo "1) 启动应用核心入口"
    echo "2) 启动本地浏览器 UI"
    echo "3) 启动 Jupyter Lab"
    echo "4) 运行轻量回测演示"
    echo "5) 生成演示 ETF 数据"
    echo "6) 下载真实 AKShare 数据"
    echo "7) 运行基金轮动回测"
    echo "8) 生成最新模拟信号"
    echo "9) 运行测试"
    echo "0) 退出"
    echo
    read -r -p "输入序号: " choice
    case "$choice" in
      1) run_cmd uv run python app/main.py ;;
      2) run_cmd uv run qfl-ui ;;
      3) run_cmd uv run jupyter lab ;;
      4) run_cmd uv run qfl-market-demo ;;
      5) run_cmd uv run qfl-demo-data ;;
      6) run_cmd uv run qfl-data ;;
      7) run_cmd uv run qfl-backtest ;;
      8) run_cmd uv run qfl-signal ;;
      9) run_cmd uv run pytest ;;
      0) exit 0 ;;
      *) echo "无效选择: $choice" ;;
    esac
    ;;
  *)
    echo "用法:"
    echo "  ./启动量化.command app       # 启动应用核心入口"
    echo "  ./启动量化.command ui        # 启动本地浏览器 UI"
    echo "  ./启动量化.command jupyter   # 启动 Jupyter Lab"
    echo "  ./启动量化.command demo      # 运行轻量回测演示"
    echo "  ./启动量化.command data      # 生成演示 ETF 数据"
    echo "  ./启动量化.command live-data # 下载真实 AKShare 数据"
    echo "  ./启动量化.command backtest  # 运行基金轮动回测"
    echo "  ./启动量化.command signal    # 生成最新模拟信号"
    echo "  ./启动量化.command test      # 运行测试"
    exit 1
    ;;
esac

echo
if [[ -t 0 ]]; then
  read -r -p "执行完成，按回车关闭窗口..." _
fi
