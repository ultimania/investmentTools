DROP TABLE db_investment.T_INDUSTRY_MS;

CREATE TABLE db_investment.T_INDUSTRY_MS (
    INDUSTRY_CD            INT,                                                    -- 業種コード
    INDUSTRY_NAME          VARCHAR(128)    NOT NULL,                               -- 業種名
    PRIMARY KEY(INDUSTRY_CD)
) ENGINE=INNODB;
