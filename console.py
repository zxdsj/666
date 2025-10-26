#!/usr/bin/env python3
"""
console.py - Windows-MCP 代理服务器

主要功能：
1. 监听指定端口（默认 18989），可通过参数修改
2. 在 /console 路径提供 console.html 文件
3. 代理所有 MCP API 请求到真实的 Windows-MCP 服务器（http://localhost:8000）
4. 解决 CORS 跨域问题
5. 实现自动重试机制（3次，间隔10秒）
"""

import asyncio
import argparse
from pathlib import Path
from aiohttp import web, ClientSession, ClientTimeout, TCPConnector
from aiohttp.web import Request, Response, StreamResponse
from aiohttp.client_exceptions import ClientConnectionResetError
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

MCP_BACKEND_URL = 'http://localhost:8000'
MAX_RETRIES = 3
RETRY_DELAY = 10

def get_cors_headers():
    """返回 CORS 头部"""
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Max-Age': '3600',
    }

async def handle_console(request: Request) -> Response:
    """处理 /console 路径，返回 console.html"""
    html_path = Path(__file__).parent / 'console.html'
    
    if not html_path.exists():
        logger.error(f'console.html 文件不存在: {html_path}')
        return web.Response(
            text='console.html 文件不存在',
            status=404,
            headers=get_cors_headers()
        )
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    port = request.app['port']
    html_content = html_content.replace(
        'http://localhost:8000',
        f'http://localhost:{port}'
    )
    
    return web.Response(
        text=html_content,
        content_type='text/html',
        headers=get_cors_headers()
    )

async def proxy_sse(request: Request) -> StreamResponse:
    """代理 SSE 连接到后端 MCP 服务器，支持重试"""
    response = web.StreamResponse(
        status=200,
        headers={
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            **get_cors_headers()
        }
    )
    await response.prepare(request)
    
    retry_count = 0
    
    while retry_count < MAX_RETRIES:
        try:
            backend_url = f'{MCP_BACKEND_URL}/sse'
            logger.info(f'正在连接到后端 SSE: {backend_url} (尝试 {retry_count + 1}/{MAX_RETRIES})')
            
            timeout = ClientTimeout(total=None, connect=10, sock_read=None)
            connector = TCPConnector(limit=100, limit_per_host=30)
            
            async with ClientSession(timeout=timeout, connector=connector) as session:
                async with session.get(backend_url) as backend_resp:
                    if backend_resp.status != 200:
                        raise Exception(f'后端返回错误状态: {backend_resp.status}')
                    
                    logger.info('SSE 连接成功建立')
                    retry_count = 0
                    
                    async for data in backend_resp.content.iter_any():
                        if data:
                            try:
                                await response.write(data)
                            except ClientConnectionResetError:
                                logger.info('客户端连接已关闭，停止 SSE 转发')
                                return response
                    
        except asyncio.CancelledError:
            logger.info('SSE 连接被取消')
            break
        except ClientConnectionResetError:
            logger.info('客户端连接已关闭')
            break
        except Exception as e:
            retry_count += 1
            logger.error(f'SSE 连接错误 (尝试 {retry_count}/{MAX_RETRIES}): {str(e)}')
            
            if retry_count < MAX_RETRIES:
                logger.info(f'将在 {RETRY_DELAY} 秒后重试...')
                error_msg = f'data: {{"error": "连接失败，{RETRY_DELAY}秒后重试 ({retry_count}/{MAX_RETRIES})"}}\n\n'
                try:
                    await response.write(error_msg.encode('utf-8'))
                except ClientConnectionResetError:
                    logger.info('无法发送错误消息，客户端已断开')
                    break
                await asyncio.sleep(RETRY_DELAY)
            else:
                logger.error('达到最大重试次数，停止重试')
                error_msg = f'data: {{"error": "连接失败，已达到最大重试次数 ({MAX_RETRIES})"}}\n\n'
                try:
                    await response.write(error_msg.encode('utf-8'))
                except ClientConnectionResetError:
                    logger.info('无法发送错误消息，客户端已断开')
                break
    
    return response

async def proxy_messages(request: Request) -> Response:
    """代理 POST /messages 请求到后端 MCP 服务器，支持重试"""
    retry_count = 0
    last_error = None
    
    body = await request.read()
    
    while retry_count < MAX_RETRIES:
        try:
            backend_url = f'{MCP_BACKEND_URL}/messages'
            logger.info(f'正在转发消息到后端: {backend_url} (尝试 {retry_count + 1}/{MAX_RETRIES})')
            
            timeout = ClientTimeout(total=30)
            
            async with ClientSession(timeout=timeout) as session:
                async with session.post(
                    backend_url,
                    data=body,
                    headers={'Content-Type': 'application/json'}
                ) as backend_resp:
                    response_body = await backend_resp.read()
                    
                    return web.Response(
                        body=response_body,
                        status=backend_resp.status,
                        content_type='application/json',
                        headers=get_cors_headers()
                    )
                    
        except Exception as e:
            retry_count += 1
            last_error = str(e)
            logger.error(f'消息转发错误 (尝试 {retry_count}/{MAX_RETRIES}): {last_error}')
            
            if retry_count < MAX_RETRIES:
                logger.info(f'将在 {RETRY_DELAY} 秒后重试...')
                await asyncio.sleep(RETRY_DELAY)
    
    return web.json_response(
        {'error': f'请求失败，已重试 {MAX_RETRIES} 次: {last_error}'},
        status=502,
        headers=get_cors_headers()
    )

async def handle_options(request: Request) -> Response:
    """处理 OPTIONS 预检请求"""
    return web.Response(
        status=200,
        headers=get_cors_headers()
    )

def create_app(port: int) -> web.Application:
    """创建并配置 web 应用"""
    app = web.Application()
    app['port'] = port
    
    app.router.add_route('OPTIONS', '/{path:.*}', handle_options)
    app.router.add_get('/console', handle_console)
    app.router.add_get('/sse', proxy_sse)
    app.router.add_post('/messages', proxy_messages)
    
    return app

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Windows-MCP 代理服务器 - 解决 CORS 问题并提供 console.html'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=18989,
        help='监听端口（默认: 18989）'
    )
    
    args = parser.parse_args()
    
    app = create_app(args.port)
    
    logger.info('=' * 60)
    logger.info(f'Windows-MCP 代理服务器启动')
    logger.info(f'监听端口: {args.port}')
    logger.info(f'Console 地址: http://localhost:{args.port}/console')
    logger.info(f'后端 MCP 地址: {MCP_BACKEND_URL}')
    logger.info(f'重试配置: 最多 {MAX_RETRIES} 次，间隔 {RETRY_DELAY} 秒')
    logger.info('=' * 60)
    
    web.run_app(app, host='0.0.0.0', port=args.port)

if __name__ == '__main__':
    main()
