DROP TABLE db_investment.T_SCALE_MS;

CREATE TABLE db_investment.T_SCALE_MS (
    SCALE_CD            INT,                                                    -- 規模コード
    SCALE_NAME          VARCHAR(128)    NOT NULL,                               -- 規模名
    PRIMARY KEY(SCALE_CD)
) ENGINE=INNODB;
