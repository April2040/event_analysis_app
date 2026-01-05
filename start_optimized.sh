#!/bin/bash

# 财经事件分析系统 v6.0.0+ - 优化启动脚本
# ===========================================
# 集成高级HTML自动生成功能 + 智能服务管理
# 支持: AI分析 + 新闻爬虫 + 专业可视化

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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
    echo "🚀 ${PROJECT_NAME} ${VERSION}"
    echo "========================================"
    echo ""
}

# 检查端口占用
check_port() {
    if lsof -Pi :${PORT} -sTCP:LISTEN -t >/dev/null 2>&1; then
        local pid=$(lsof -Pi :${PORT} -sTCP:LISTEN -t)
        log_warning "端口 ${PORT} 已被占用 (PID: ${pid})"
        echo ""
        echo "🔄 自动处理选项:"
        echo "1) 停止现有服务并重新启动 [推荐]"
        echo "2) 查看现有服务状态"
        echo "3) 退出"
        echo ""
        read -t 10 -p "请选择 (1-3，10秒后自动选择1): " choice
        
        # 如果超时，默认选择1
        if [ -z "$choice" ]; then
            choice=1
            echo "⏰ 超时，自动选择重新启动..."
        fi
        
        case $choice in
            1)
                log_info "停止现有服务..."
                kill -TERM $pid 2>/dev/null
                sleep 3
                if lsof -Pi :${PORT} -sTCP:LISTEN -t >/dev/null 2>&1; then
                    log_warning "服务未正常停止，强制终止..."
                    kill -KILL $pid 2>/dev/null
                    sleep 1
                fi
                log_success "现有服务已停止，准备重新启动..."
                ;;
            2)
                log_info "现有服务状态:"
                ps aux | grep $pid | grep -v grep
                echo ""
                log_info "服务运行中，访问地址: http://localhost:${PORT}"
                exit 0
                ;;
            3)
                log_info "退出启动"
                exit 0
                ;;
            *)
                log_error "无效选择，退出"
                exit 1
                ;;
        esac
    fi
}

# 系统环境检查
check_environment() {
    log_info "检查系统环境..."
    
    # 检查主程序文件
    if [ ! -f "main_integrated.py" ]; then
        log_error "找不到主程序文件 main_integrated.py"
        log_error "请确保在正确的项目目录中运行此脚本"
        exit 1
    fi
    
    # 检查虚拟环境
    if [ ! -d "venv" ]; then
        log_error "找不到虚拟环境目录 venv"
        log_info "自动创建虚拟环境..."
        python3 -m venv venv
        if [ $? -ne 0 ]; then
            log_error "创建虚拟环境失败"
            exit 1
        fi
        log_success "虚拟环境创建完成"
    fi
    
    # 激活虚拟环境
    log_info "激活虚拟环境..."
    source venv/bin/activate
    
    # 检查关键依赖
    log_info "检查依赖包..."
    python -c "import fastapi, uvicorn" 2>/dev/null
    if [ $? -ne 0 ]; then
        log_warning "缺少关键依赖包，开始安装..."
        pip install fastapi uvicorn python-multipart jinja2 requests beautifulsoup4 lxml openai python-dotenv
        if [ $? -ne 0 ]; then
            log_error "依赖包安装失败"
            exit 1
        fi
        log_success "依赖包安装完成"
    fi
    
    # 检查环境变量
    if [ ! -f ".env" ]; then
        log_warning "找不到 .env 文件"
        log_warning "请确保设置了 DEEPSEEK_API_KEY"
    else
        log_success "环境配置文件存在"
    fi
    
    log_success "环境检查完成"
}

# 显示功能介绍
show_features() {
    echo ""
    echo "🎯 系统功能:"
    echo "  • AI深度事件分析 (DeepSeek)"
    echo "  • RSS新闻实时爬取"
    echo "  • 高级HTML可视化报告"
    echo "  • 四模块专业分析框架"
    echo "  • 动态投资策略提取"
    echo "  • 标准化HTML模板渲染"
    echo ""
    echo "🌐 访问地址:"
    echo "  • 主页面: http://localhost:${PORT}"
    echo "  • 新闻页面: http://localhost:${PORT}/news"
    echo "  • API接口: http://localhost:${PORT}/api/news"
    echo ""
    echo "💡 使用提示:"
    echo "  • 完整模式: 生成分析 + 专业HTML报告"
    echo "  • 快速模式: 仅生成分析，节省50%时间"
    echo "  • 停止服务: 按 Ctrl+C 或运行 ./stop.sh"
}

# 启动服务
start_service() {
    echo ""
    log_info "启动Web服务器..."
    
    # 记录启动时间
    echo "$(date): 启动服务" >> server.log
    
    # 启动主程序
    python main_integrated.py &
    SERVER_PID=$!
    
    # 保存PID
    echo $SERVER_PID > $PID_FILE
    
    # 等待服务启动
    log_info "等待服务启动..."
    sleep 5
    
    # 检查服务状态
    if kill -0 $SERVER_PID 2>/dev/null; then
        if curl -s "http://localhost:${PORT}" >/dev/null 2>&1; then
            log_success "服务启动成功！"
            echo ""
            echo "🌟 服务运行状态:"
            echo "  • PID: $SERVER_PID"
            echo "  • 端口: $PORT"
            echo "  • 状态: 运行中"
            echo ""
            echo "📱 快速访问:"
            echo "  curl http://localhost:${PORT}"
            echo ""
            log_success "系统已就绪，可以开始使用！"
            
            # 等待服务
            wait $SERVER_PID
        else
            log_error "服务启动失败 - 端口无响应"
            kill $SERVER_PID 2>/dev/null
            rm -f $PID_FILE
            exit 1
        fi
    else
        log_error "服务进程启动失败"
        rm -f $PID_FILE
        exit 1
    fi
}

# 清理函数
cleanup() {
    echo ""
    log_info "正在停止服务..."
    if [ -f $PID_FILE ]; then
        local pid=$(cat $PID_FILE)
        kill -TERM $pid 2>/dev/null
        sleep 3
        if kill -0 $pid 2>/dev/null; then
            kill -KILL $pid 2>/dev/null
        fi
        rm -f $PID_FILE
        log_success "服务已停止"
    fi
    echo "$(date): 停止服务" >> server.log
    exit 0
}

# 设置信号处理
trap cleanup SIGINT SIGTERM

# 主执行流程
main() {
    show_header
    check_environment
    check_port
    show_features
    start_service
}

# 执行主函数
main "$@"
