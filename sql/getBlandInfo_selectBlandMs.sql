SELECT
    investment_t_bland_ms.bland_cd,
    investment_t_bland_ms.bland_name,
    investment_t_bland_ms.market_prod_cls,
    investment_t_bland_ms.industry_cd_id,
    investment_t_industry_ms.industry_name,
    investment_t_bland_ms.sub_industry_cd,
    T_SUB_INDUSTRY_MS.industry_name,
    investment_t_bland_ms.scale_cd_id,
    investment_t_scale_ms.scale_name,
    investment_t_bland_ms.access_url_string
FROM   
    investment_t_bland_ms
LEFT OUTER JOIN investment_t_industry_ms
    ON investment_t_industry_ms.industry_cd = investment_t_bland_ms.industry_cd_id
LEFT OUTER JOIN investment_t_industry_ms AS T_SUB_INDUSTRY_MS
    ON T_SUB_INDUSTRY_MS.industry_cd = investment_t_bland_ms.sub_industry_cd
LEFT OUTER JOIN investment_t_scale_ms
    ON investment_t_scale_ms.scale_cd = investment_t_bland_ms.scale_cd_id
WHERE
    investment_t_bland_ms.fetch_flg = 0
;
