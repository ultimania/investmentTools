DROP TABLE DB_INVESTMENT.T_BLAND_MS;

CREATE TABLE DB_INVESTMENT.T_BLAND_MS (
    BLAND_CD            INT,                                                    -- 銘柄コード
    BLAND_NAME          VARCHAR(128)    NOT NULL,                               -- 銘柄名
    MARKET_PROD_CLS     VARCHAR(64)     NOT NULL,                               -- 市場・商品区分
    INDUSTRY_CD         INT,                                                    -- 業種コード
    INDUSTRY_NAME       VARCHAR(64),                                            -- 業種区分
    SUB_INDUSTRY_CD     INT,                                                    -- サブ業種コード
    SUB_INDUSTRY_NAME   VARCHAR(64),                                            -- サブ業種区分
    SCALE_CD            INT,                                                    -- 規模コード
    SCALE_NAME          VARCHAR(64),                                            -- 規模区分
    FETCH_FLG           INT NOT NULL,                                           -- 取込フラグ
    PRIMARY KEY(BLAND_ID),
    FOREIGN KEY(MARKET_PROD_CLS)     REFERENCET T_CLS_MS(VALUE),                -- 区分マスタ.値
    FOREIGN KEY(INDUSTRY_CD)         REFERENCET T_INDUSTRY_MS(INDUSTRY_CD),     -- 業種マスタ.業種コード
    FOREIGN KEY(INDUSTRY_NAME)       REFERENCET T_INDUSTRY_MS(INDUSTRY_NAME),   -- 業種マスタ.業種名
    FOREIGN KEY(SUB_INDUSTRY_CD)     REFERENCET T_INDUSTRY_MS(INDUSTRY_CD),     -- 業種マスタ.業種コード
    FOREIGN KEY(SUB_INDUSTRY_NAME)   REFERENCET T_INDUSTRY_MS(INDUSTRY_NAME),   -- 業種マスタ.業種名
    FOREIGN KEY(SCALE_CD)            REFERENCET T_SCALE_MS(SCALE_CD),           -- 規模マスタ.規模コード
    FOREIGN KEY(SCALE_NAME)          REFERENCET T_SCALE_MS(SCALE_NAME)          -- 規模マスタ.規模名
) ENGINE=INNODB;
