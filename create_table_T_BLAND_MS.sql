DROP TABLE db_investment.T_BLAND_MS;

CREATE TABLE db_investment.T_BLAND_MS (
    BLAND_CD            INT,                                                    -- 銘柄コード
    BLAND_NAME          VARCHAR(128)    NOT NULL,                               -- 銘柄名
    MARKET_PROD_CLS     VARCHAR(64)     NOT NULL,                               -- 市場・商品区分
    INDUSTRY_CD         INT             NOT NULL,                               -- 業種コード
    INDUSTRY_NAME       VARCHAR(64)     NOT NULL,                               -- 業種区分
    SUB_INDUSTRY_CD     INT             NOT NULL,                               -- サブ業種コード
    SUB_INDUSTRY_NAME   VARCHAR(64)     NOT NULL,                               -- サブ業種区分
    SCALE_CD            INT             NOT NULL,                               -- 規模コード
    SCALE_NAME          VARCHAR(64)     NOT NULL,                               -- 規模区分
    FETCH_FLG           INT             NOT NULL,                               -- 取込フラグ
    PRIMARY KEY(BLAND_CD),
    FOREIGN KEY(INDUSTRY_CD)         REFERENCES T_INDUSTRY_MS(INDUSTRY_CD),     -- 業種マスタ.業種コード
    FOREIGN KEY(SUB_INDUSTRY_CD)     REFERENCES T_INDUSTRY_MS(INDUSTRY_CD),     -- 業種マスタ.業種コード
    FOREIGN KEY(SCALE_CD)            REFERENCES T_SCALE_MS(SCALE_CD),           -- 規模マスタ.規模コード
) ENGINE=INNODB;
