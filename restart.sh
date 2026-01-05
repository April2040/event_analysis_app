#!/bin/bash

# 财经事件分析系统 - 快速重启脚本
# 作者: 系统管理员
# 版本: v1.0.0

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 项目配置
PROJECT_NAME="财经事件分析系统"
VERSION="v6.0.0+"
PORT=8002
PID_FILE="server.pid"

# 日志函数
log_info() {
    echo -e "${BLUE}ℹ️  ${1}${NC}"
}

log_success() {
    echo -e "${GREEN}✅ ${1}${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  ${1}${NC}"
}

log_error() {
    echo -e "${RED}❌ ${1}${NC}"
}

# 显示标题
show_header() {
    echo "🔄 ${PROJECT_NAME} - 快速重启"
    echo "================================"
    echo ""
}

# 停止服务
stop_service() {
    log_info "正在停止现有服务..."
    
    # 尝试优雅停止
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if kill -0 $pid 2>/dev/null; then
            kill -TERM $pid 2>/dev/null
            log_info "发送停止信号，等待服务优雅退出..."
            
            # 等待最多10秒
            for i in {1..10}; do
                if ! kill -0 $pid 2>/dev/null; then
                    break
                fi
                sleep 1
            done
            
            # 如果还在运行，强制终止
            if kill -0 $pid 2>/dev/null; then
                log_warning "优雅停止超时，强制终止..."
                kill -KILL $pid 2>/dev/null
            fi
        fi
        rm -f "$PID_FILE"
    fi
    
    # 清理端口占用
    if lsof -Pi :${PORT} -sTCP:LISTEN -t >/dev/null 2>&1; then
        local port_pid=$(lsof -Pi :${PORT} -sTCP:LISTEN -t)
        log_warning "发现端口占用 (PID: ${port_pid})，清理中..."
        kill -KILL $port_pid 2>/dev/null || true
    fi
    
    log_success "服务已停止"
}

# 启动服务
start_service() {
    log_info "启动新服务..."
    
    # 检查启动脚本
    if [ ! -f "start_optimized.sh" ]; then
        log_error "找不到启动脚本 start_optimized.sh"
        exit 1
    fi
    
    # 以非交互模式启动
    echo "1" | bash start_optimized.sh
}

# 主函数
main() {
    show_header
    
    log_info "开始快速重启流程..."
    echo ""
    
    stop_service
    echo ""
    
    log_info "等待2秒确保端口释放..."
    sleep 2
    
    start_service
}

# 执行主函数
main "$@"
