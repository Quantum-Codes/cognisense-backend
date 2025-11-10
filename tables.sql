CREATE TABLE page_view_sessions (
    session_id INT PRIMARY KEY,  -- A unique ID for this specific page view
    user_id UUID NOT NULL,            -- Foreign key to your Users table
    url TEXT NOT NULL,                -- The exact URL the user visited
    domain VARCHAR(255) NOT NULL,     -- The domain (e.g., 'youtube.com'), extracted from the URL
    start_time TIMESTAMPTZ NOT NULL,  -- When the user opened this page
    end_time TIMESTAMPTZ NOT NULL,      -- When the user left this page (navigated away or closed tab)
    
    -- "get all data for one user on one day"
    INDEX idx_user_day (user_id, DATE(start_time))
);

CREATE TABLE content_analysis (
    analysis_id INT PRIMARY KEY,
    user_id UUID NOT NULL,          -- Foreign key to your Users table
    page_url TEXT NOT NULL UNIQUE,       -- The URL of the content that was analyzed (acts as a key)
    scraped_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), -- When the content was analyzed
    
    happy_score DECIMAL(5, 4) DEFAULT 0.0,
    sad_score DECIMAL(5, 4) DEFAULT 0.0,
    angry_score DECIMAL(5, 4) DEFAULT 0.0,
    neutral_score DECIMAL(5, 4) DEFAULT 0.0,
    dominant_emotion VARCHAR(50),  -- 'happy', 'sad', 'angry', 'neutral'

    -- This field would store a *suggested* high-level category based on content (AI-driven)
    -- This might be 'Productivity', 'Entertainment', 'Learning', 'Social', 'Shopping'
    -- It's NOT the user's override, but the system's best guess for the content itself.
    system_suggested_category VARCHAR(50),
    
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_user_url (user_id, page_url) -- if referring from the above table
);

CREATE TABLE user_domain_categories (
    user_category_id INT PRIMARY KEY,
    user_id UUID NOT NULL,
    domain_pattern VARCHAR(255) NOT NULL, -- e.g., 'youtube.com', 'news.google.com', 'github.com/my-project/*'
    category VARCHAR(50) NOT NULL,        -- 'Productivity', 'Entertainment', 'Learning', 'Social', 'Uncategorized'
    priority INT DEFAULT 1,               -- Higher priority means this rule overrides lower priority rules. [eg crunchyroll is always entertainment so better dont check with ai. also if user specified categories manually then that comes here too]
                                          -- (e.g. URL pattern > generic ai identified domain)
    
    UNIQUE (user_id, domain_pattern), -- A user can only categorize a pattern once
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    
    INDEX idx_user_domain (user_id, domain_pattern)
);