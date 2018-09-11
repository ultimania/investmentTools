DROP TABLE DB_INVESTMENT.T_CLS_MS;

CREATE TABLE DB_INVESTMENT.T_CLS_MS (
    CLS_CD            INT,                                                    -- 業種コード
    CLS_NAME          VARCHAR(128)    NOT NULL,                               -- 業種名
    PRIMARY KEY(CLS_CD)
) ENGINE=INNODB;
