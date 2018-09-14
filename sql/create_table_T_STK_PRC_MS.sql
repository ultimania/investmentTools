DROP TABLE db_investment.T_STK_PRC_TR;

CREATE TABLE db_investment.T_STK_PRC_TR (
    BLAND_CD            INT,                                                -- 銘柄コード
    MARKET_PROD_CLS     VARCHAR(64)         NOT NULL,                       -- 市場・商品区分
    CURRENT_PRICE       INT                 ,                               -- 現在値
    DAY_BEFORE_RATIO    INT                 ,                               -- 前日比
    OPENING_PRICE       INT                 ,                               -- 始値
    HIGH_PRICE          INT                 ,                               -- 高値
    LOW_PRICE           INT                 ,                               -- 安値
    SALES_VOLUME        INT ,                                               -- 売買高
    CREATE_TIMESTAMP    DATETIME,                                           -- 取得日時
    PRIMARY KEY(BLAND_CD,CREATE_TIMESTAMP),
    FOREIGN KEY(BLAND_CD)         REFERENCES T_BLAND_MS(BLAND_CD),          -- 銘柄マスタ.銘柄コード
) ENGINE=INNODB;
