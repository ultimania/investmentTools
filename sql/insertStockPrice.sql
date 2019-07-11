insert into {TABLE_NAME} (
    market_prod_cls ,
    current_price ,
    day_before_ratio ,
    opening_price ,
    high_orice ,
    low_price ,
    sales_volume ,
    created_at ,
    bland_cd_id
) values (
    '{MARKET_PROD_CLS}', 
    {CURRENT_PRICE},
    {DAY_BEFORE_RATIO},
    {OPENING_PRICE},
    {HIGH_PRICE},
    {LOW_PRICE},
    {SALES_VOLUME},
    '{CREATE_TIMESTAMP}',
    {BLAND_CD}
);

