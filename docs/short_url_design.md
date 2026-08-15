# 短链服务（TinyURL）系统设计

## 1. 需求
- 核心功能：长链接 → 短链接（唯一、可读）、短链接 → 长链接（重定向）
- 非功能性：高可用、低延迟、支持海量数据

## 2. 架构图
[用 Mermaid 画图]
客户端 → 负载均衡器 → Web 服务器集群 → 数据库/缓存

## 3. 关键设计
### 哈希算法
- 使用 Base62（数字+大小写字母），6 位可生成 ~560 亿个短码
- 碰撞处理：如果碰撞，追加随机字符重试

### 数据库设计
```sql
CREATE TABLE short_urls (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    short_code VARCHAR(10) UNIQUE NOT NULL,
    long_url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    click_count INT DEFAULT 0
);
CREATE INDEX idx_short_code ON short_urls(short_code);