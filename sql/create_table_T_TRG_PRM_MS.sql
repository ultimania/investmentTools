DROP TABLE db_investment.T_TRG_PRM_MS;

CREATE TABLE db_investment.T_TRG_PRM_MS (
    TRG_PRM_CD          INT,                                                -- 対象パラメタコード
    TRG_PRM_NAME        VARCHAR(64)         NOT NULL,                       -- 対象パラメタ名
    FIND_TAG            VARCHAR(64)         ,                               -- 検索タグ
    CLASS_STRING        VARCHAR(128)        ,                               -- クラス文字列
    EXCLUDE_TAGS        VARCHAR(2048)       ,                               -- 除外タグ
    PRIMARY KEY(TRG_PRM_CD)
) ENGINE=INNODB;
