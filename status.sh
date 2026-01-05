#!/bin/bash

# 财经事件分析系统 - 服务状态检查
# ===============================

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

echo "📊 财经事件分析系统 - 服务状态"
echo "=============================="
echo ""

# 检查PID文件
if [ -f "$PID_FILE" ]; then
    PID=$(cat $PID_FILE)
    if kill -0 $PID 2>/dev/null; then
        log_success "服务运行中 (PID: $PID)"
        RUNNING=true
    else
        log_warning "PID文件存在但进程不存在"
        RUNNING=false
    fi
else
    log_info "未找到PID文件"
    RUNNING=false
fi

# 检查端口占用
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    PORT_PID=$(lsof -Pi :$PORT -sTCP:LISTEN -t)
    log_success "端口 $PORT 被占用 (PID: $PORT_PID)"
    PORT_USED=true
else
    log_warning "端口 $PORT 未被占用"
    PORT_USED=false
fi

# 服务响应测试
echo ""
log_info "测试服务响应..."
if curl -s --max-time 5 "http://localhost:$PORT" >/dev/null 2>&1; then
    log_success "HTTP服务响应正常"
    HTTP_OK=true
    
    # 测试API
    if curl -s --max-time 5 "http://localhost:$PORT/api/news" >/dev/null 2>&1; then
        log_success "API接口响应正常"
        API_OK=true
    else
        log_warning "API接口无响应"
        API_OK=false
    fi
else
    log_error "HTTP服务无响应"
    HTTP_OK=false
    API_OK=false
fi

# 显示详细状态
echo ""
echo "📋 详细状态报告:"
echo "=================="

if [ "$RUNNING" = true ] && [ "$PORT_USED" = true ] && [ "$HTTP_OK" = true ]; then
    log_success "✅ 服务状态: 完全正常"
    STATUS="健康"
elif [ "$PORT_USED" = true ] && [ "$HTTP_OK" = true ]; then
    log_warning "⚠️  服务状态: 运行中但PID文件异常"
    STATUS="警告"
elif [ "$PORT_USED" = true ]; then
    log_warning "⚠️  服务状态: 端口占用但无HTTP响应"
    STATUS="异常"
else
    log_error "❌ 服务状态: 未运行"
    STATUS="停止"
fi

echo ""
echo "🔍 系统信息:"
echo "  • 服务状态: $STATUS"
echo "  • 端口: $PORT $([ "$PORT_USED" = true ] && echo "✅ 占用" || echo "❌ 空闲")"
echo "  • HTTP响应: $([ "$HTTP_OK" = true ] && echo "✅ 正常" || echo "❌ 异常")"
echo "  • API响应: $([ "$API_OK" = true ] && echo "✅ 正常" || echo "❌ 异常")"
if [ "$RUNNING" = true ]; then
    echo "  • 进程PID: $PID"
    echo "  • CPU使用: $(ps -p $PID -o %cpu= 2>/dev/null | xargs)%"
    echo "  • 内存使用: $(ps -p $PID -o %mem= 2>/dev/null | xargs)%"
fi

# 显示最近日志
if [ -f "server.log" ]; then
    echo ""
    echo "📝 最近日志 (最后5行):"
    tail -5 server.log | while read line; do
        echo "  $line"
    done
fi

# 显示访问地址
if [ "$HTTP_OK" = true ]; then
    echo ""
    echo "🌐 访问地址:"
    echo "  • 主页面: http://localhost:$PORT"
    echo "  • 新闻页面: http://localhost:$PORT/news"
    echo "  • API接口: http://localhost:$PORT/api/news"
fi

echo ""
