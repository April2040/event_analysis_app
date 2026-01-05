#!/bin/bash

# 财经事件分析系统 - 优化停止脚本
# ==================================

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置
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

echo "🛑 财经事件分析系统 - 停止服务"
echo "================================"
echo ""

# 检查PID文件
if [ -f "$PID_FILE" ]; then
    PID=$(cat $PID_FILE)
    log_info "发现PID文件: $PID"
    
    if kill -0 $PID 2>/dev/null; then
        log_info "正在停止服务 (PID: $PID)..."
        kill -TERM $PID
        
        # 等待优雅停止
        for i in {1..10}; do
            if ! kill -0 $PID 2>/dev/null; then
                break
            fi
            sleep 1
            echo -n "."
        done
        echo ""
        
        # 检查是否还在运行
        if kill -0 $PID 2>/dev/null; then
            log_warning "服务未响应TERM信号，强制终止..."
            kill -KILL $PID
            sleep 1
        fi
        
        # 验证停止
        if ! kill -0 $PID 2>/dev/null; then
            log_success "服务已停止"
            rm -f $PID_FILE
        else
            log_error "无法停止服务"
            exit 1
        fi
    else
        log_warning "PID文件存在但进程不存在，清理PID文件"
        rm -f $PID_FILE
    fi
else
    log_info "未找到PID文件，检查端口占用..."
fi

# 检查端口占用
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    PORT_PID=$(lsof -Pi :$PORT -sTCP:LISTEN -t)
    log_warning "端口 $PORT 仍被占用 (PID: $PORT_PID)"
    
    read -p "是否强制停止占用端口的进程? (y/N): " confirm
    if [[ $confirm =~ ^[Yy]$ ]]; then
        kill -TERM $PORT_PID
        sleep 3
        if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
            kill -KILL $PORT_PID
        fi
        log_success "端口已释放"
    fi
else
    log_success "端口 $PORT 未被占用"
fi

# 记录日志
echo "$(date): 停止服务" >> server.log

echo ""
log_success "停止操作完成"
