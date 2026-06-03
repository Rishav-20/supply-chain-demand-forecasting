-- ==========================================
-- PHASE 3: DATABASE SCHEMA DEFINITION (DDL)
-- ==========================================

-- Drop tables if they exist to ensure reproducibility
DROP TABLE IF EXISTS fact_sales;
DROP TABLE IF EXISTS dim_calendar;
DROP TABLE IF EXISTS dim_sell_prices;

-- 1. DIMENSION TABLE: Calendar
-- Tracks historical dates, weekday names, and promotional events (SNAP)
CREATE TABLE dim_calendar (
    date_id TEXT PRIMARY KEY,           -- Matches 'd_1', 'd_2' keys from the sales data
    calendar_date TEXT NOT NULL,         -- Format: YYYY-MM-DD
    weekday_name TEXT NOT NULL,         -- Saturday, Sunday, etc.
    weekday_int INTEGER NOT NULL,       -- Numerical day index
    month_id INTEGER NOT NULL,          -- Numerical month
    year_id INTEGER NOT NULL,           -- Numerical year
    event_name_1 TEXT,                  -- Special event/holiday name (e.g., SuperBowl)
    event_type_1 TEXT,                  -- Category of event (e.g., Sporting)
    event_name_2 TEXT,                  -- Secondary event name
    event_type_2 TEXT,                  -- Secondary event type
    snap_CA INTEGER NOT NULL,           -- SNAP benefits flag for California (0 or 1)
    snap_TX INTEGER NOT NULL,           -- SNAP benefits flag for Texas (0 or 1)
    snap_WI INTEGER NOT NULL            -- SNAP benefits flag for Wisconsin (0 or 1)
);

-- 2. DIMENSION TABLE: Sell Prices
-- Tracks the weekly price changes of items across specific stores
CREATE TABLE dim_sell_prices (
    store_id TEXT NOT NULL,
    item_id TEXT NOT NULL,
    wm_yr_wk INTEGER NOT NULL,          -- Key linking to week index in calendar
    sell_price REAL NOT NULL,           -- Retail price of the item (Floating point decimal)
    PRIMARY KEY (store_id, item_id, wm_yr_wk)
);

-- 3. FACT TABLE: Sales (Optimized & Normal 1NF Format)
-- Houses the tall, unpivoted transactional records for unit sales
CREATE TABLE fact_sales (
    sales_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id TEXT NOT NULL,
    dept_id TEXT NOT NULL,
    cat_id TEXT NOT NULL,
    store_id TEXT NOT NULL,
    state_id TEXT NOT NULL,
    date_id TEXT NOT NULL,              -- Foreign key linking to dim_calendar(date_id)
    units_sold INTEGER NOT NULL,        -- Target metric for forecasting
    FOREIGN KEY (date_id) REFERENCES dim_calendar(date_id)
);