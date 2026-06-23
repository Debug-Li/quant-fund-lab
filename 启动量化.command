#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="/Users/qml/Desktop/workspace/quant-fund-lab"
cd "$PROJECT_DIR"

if [[ -t 1 && -n "${TERM:-}" && "${TERM:-}" != "dumb" ]]; then
  clear
fi
echo "Quant Fund Lab 快捷启动"
echo "项目目录: $PROJECT_DIR"
echo
echo "默认将启动新版量观 Quant Lab：FastAPI 后端 + React 前端"
echo "打开地址: http://localhost:5173"
echo

run_cmd() {
  echo
  echo "运行: $*"
  echo
  "$@"
}

case "${1:-quant-lab}" in
  quant-lab|start)
    run_cmd uv run quant-lab
    ;;
  api)
    run_cmd uv run quant-lab-api
    ;;
  web)
    run_cmd npm run dev --prefix apps/web
    ;;
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
  menu|legacy)
    echo "请选择要执行的操作:"
    echo "1) 启动新版量观 Quant Lab"
    echo "2) 只启动 FastAPI 后端"
    echo "3) 只启动 React 前端"
    echo "4) 启动旧版 Streamlit UI"
    echo "5) 启动 Jupyter Lab"
    echo "6) 运行轻量回测演示"
    echo "7) 生成演示 ETF 数据"
    echo "8) 下载真实 AKShare 数据"
    echo "9) 运行基金轮动回测"
    echo "10) 生成最新模拟信号"
    echo "11) 运行测试"
    echo "0) 退出"
    echo
    read -r -p "输入序号: " choice
    case "$choice" in
      1) run_cmd uv run quant-lab ;;
      2) run_cmd uv run quant-lab-api ;;
      3) run_cmd npm run dev --prefix apps/web ;;
      4) run_cmd uv run qfl-ui ;;
      5) run_cmd uv run jupyter lab ;;
      6) run_cmd uv run qfl-market-demo ;;
      7) run_cmd uv run qfl-demo-data ;;
      8) run_cmd uv run qfl-data ;;
      9) run_cmd uv run qfl-backtest ;;
      10) run_cmd uv run qfl-signal ;;
      11) run_cmd uv run pytest ;;
      0) exit 0 ;;
      *) echo "无效选择: $choice" ;;
    esac
    ;;
  *)
    echo "用法:"
    echo "  ./启动量化.command           # 一键启动新版量观 Quant Lab"
    echo "  ./启动量化.command start     # 一键启动新版量观 Quant Lab"
    echo "  ./启动量化.command api       # 只启动 FastAPI 后端"
    echo "  ./启动量化.command web       # 只启动 React 前端"
    echo "  ./启动量化.command legacy    # 打开旧工具菜单"
    echo "  ./启动量化.command ui        # 启动旧版 Streamlit UI"
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
