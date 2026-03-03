-- 云衣橱数据库初始化脚本
-- 注意: 实际部署时使用Alembic迁移

-- 创建数据库
CREATE DATABASE cloudrobe;

-- 连接到数据库
\c cloudrobe;

-- 创建扩展(如果需要)
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- 用户表
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    openid VARCHAR(128) UNIQUE,
    unionid VARCHAR(128),
    phone VARCHAR(20) UNIQUE,
    nickname VARCHAR(50),
    avatar VARCHAR(500),
    gender SMALLINT DEFAULT 0,
    height SMALLINT,
    weight SMALLINT,
    size_preferences TEXT,
    bio TEXT,
    credit_score BIGINT DEFAULT 0,
    credit_level VARCHAR(20),
    balance DECIMAL(10,2) DEFAULT 0,
    is_verified BOOLEAN DEFAULT FALSE,
    id_card_name VARCHAR(50),
    id_card_number VARCHAR(18),
    id_card_front VARCHAR(500),
    id_card_back VARCHAR(500),
    status SMALLINT DEFAULT 1,
    last_login_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_phone ON users(phone);
CREATE INDEX idx_openid ON users(openid);
CREATE INDEX idx_credit_score ON users(credit_score);
CREATE INDEX idx_status ON users(status);

-- 衣物表
CREATE TABLE clothings (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES users(id),
    name VARCHAR(100) NOT NULL,
    brand VARCHAR(50),
    category VARCHAR(50) NOT NULL,
    size VARCHAR(10) NOT NULL,
    condition VARCHAR(20) NOT NULL,
    description TEXT,
    images TEXT NOT NULL,
    daily_rent DECIMAL(10,2) NOT NULL,
    deposit DECIMAL(10,2) NOT NULL,
    min_rent_days SMALLINT DEFAULT 1,
    max_rent_days SMALLINT DEFAULT 7,
    require_wash BOOLEAN DEFAULT TRUE,
    delivery_type SMALLINT DEFAULT 1,
    delivery_fee DECIMAL(10,2) DEFAULT 0,
    status SMALLINT DEFAULT 1,
    rent_count BIGINT DEFAULT 0,
    total_revenue DECIMAL(10,2) DEFAULT 0,
    rating_avg DECIMAL(3,2),
    rating_count BIGINT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_owner ON clothings(owner_id);
CREATE INDEX idx_category ON clothings(category);
CREATE INDEX idx_size ON clothings(size);
CREATE INDEX idx_status ON clothings(status);
CREATE INDEX idx_price ON clothings(daily_rent);
CREATE INDEX idx_created ON clothings(created_at);

-- 订单表
CREATE TABLE orders (
    id BIGSERIAL PRIMARY KEY,
    order_no VARCHAR(32) UNIQUE NOT NULL,
    clothing_id BIGINT NOT NULL REFERENCES clothings(id),
    renter_id BIGINT NOT NULL REFERENCES users(id),
    owner_id BIGINT NOT NULL REFERENCES users(id),
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    rent_days SMALLINT NOT NULL,
    daily_rent DECIMAL(10,2) NOT NULL,
    rent_amount DECIMAL(10,2) NOT NULL,
    deposit DECIMAL(10,2) NOT NULL,
    delivery_fee DECIMAL(10,2) DEFAULT 0,
    total_amount DECIMAL(10,2) NOT NULL,
    status SMALLINT NOT NULL,
    confirm_time TIMESTAMP,
    ship_time TIMESTAMP,
    receive_time TIMESTAMP,
    return_time TIMESTAMP,
    complete_time TIMESTAMP,
    cancel_time TIMESTAMP,
    express_company VARCHAR(50),
    express_no VARCHAR(50),
    renter_rating SMALLINT,
    renter_comment TEXT,
    renter_images TEXT,
    owner_rating SMALLINT,
    owner_comment TEXT,
    owner_images TEXT,
    dispute_reason VARCHAR(100),
    dispute_desc TEXT,
    dispute_images TEXT,
    dispute_status SMALLINT DEFAULT 0,
    dispute_result TEXT,
    deposit_refund DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_order_no ON orders(order_no);
CREATE INDEX idx_renter ON orders(renter_id);
CREATE INDEX idx_owner ON orders(owner_id);
CREATE INDEX idx_clothing ON orders(clothing_id);
CREATE INDEX idx_status ON orders(status);
CREATE INDEX idx_created ON orders(created_at);
CREATE INDEX idx_renter_status ON orders(renter_id, status);

-- 评价表
CREATE TABLE reviews (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT NOT NULL REFERENCES orders(id),
    reviewer_id BIGINT NOT NULL REFERENCES users(id),
    target_id BIGINT NOT NULL REFERENCES users(id),
    type SMALLINT NOT NULL,
    rating SMALLINT NOT NULL,
    comment TEXT,
    images TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_reviewer ON reviews(reviewer_id);
CREATE INDEX idx_target ON reviews(target_id);
CREATE INDEX idx_order ON reviews(order_id);

-- 收藏表
CREATE TABLE favorites (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id),
    clothing_id BIGINT NOT NULL REFERENCES clothings(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, clothing_id)
);

CREATE INDEX idx_user ON favorites(user_id);
CREATE INDEX idx_clothing ON favorites(clothing_id);

-- 消息表
CREATE TABLE messages (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id),
    type SMALLINT NOT NULL,
    title VARCHAR(100) NOT NULL,
    content TEXT,
    data TEXT,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_user ON messages(user_id);
CREATE INDEX idx_read ON messages(is_read);
CREATE INDEX idx_type ON messages(type);
CREATE INDEX idx_created ON messages(created_at);

-- 交易记录表
CREATE TABLE transactions (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id),
    order_id BIGINT REFERENCES orders(id),
    type SMALLINT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    balance_before DECIMAL(10,2),
    balance_after DECIMAL(10,2),
    description VARCHAR(200),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_user ON transactions(user_id);
CREATE INDEX idx_order ON transactions(order_id);
CREATE INDEX idx_type ON transactions(type);
CREATE INDEX idx_created ON transactions(created_at);

-- 搜索历史表
CREATE TABLE search_history (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id),
    keyword VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_user ON search_history(user_id);
CREATE INDEX idx_created ON search_history(created_at);

-- 创建更新时间触发器函数
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 为所有表添加更新时间触发器
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_clothings_updated_at BEFORE UPDATE ON clothings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_orders_updated_at BEFORE UPDATE ON orders
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_reviews_updated_at BEFORE UPDATE ON reviews
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_favorites_updated_at BEFORE UPDATE ON favorites
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_messages_updated_at BEFORE UPDATE ON messages
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_transactions_updated_at BEFORE UPDATE ON transactions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_search_history_updated_at BEFORE UPDATE ON search_history
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 插入测试数据
INSERT INTO users (phone, nickname, gender, is_verified, status) VALUES
('13800138000', '测试用户1', 2, TRUE, 1),
('13800138001', '测试用户2', 2, TRUE, 1);

COMMIT;
