SELECT
 investment_t_url_ms.url_cd  , 
 investment_t_url_ms.url_str , 
 investment_t_url_ms.tag_cd  , 
 investment_t_url_ms.pages
FROM   
    investment_t_url_ms
WHERE
    investment_t_url_ms.get_flg = 1
;

