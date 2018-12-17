SELECT
    investment_t_trg_prm_ms.trg_prm_cd      ,
    investment_t_trg_prm_ms.trg_prm_name    ,
    investment_t_trg_prm_ms.find_tag        ,
    investment_t_trg_prm_ms.class_string    ,
    investment_t_trg_prm_ms.exclude_tags    ,
    investment_t_trg_prm_ms.created_at  
FROM   
    investment_t_trg_prm_ms
WHERE
    investment_t_trg_prm_ms.trg_prm_cd <> 0
;

