#!/bin/sh

# base path
GIT_DIR="/git/ultimania/investment/"

# script file path
SQL_CRE_BLAND_MS=${GIT_DIR}"/sql/create_table_T_BLAND_MS.sql"
SQL_CRE_CLS_MS=${GIT_DIR}"/sql/create_table_T_CLS_MS.sql"
SQL_CRE_INDUSTRY_MS=${GIT_DIR}"/sql/create_table_T_INDUSTRY_MS.sql"
SQL_CRE_SCALE_MS=${GIT_DIR}"/sql/create_table_T_SCALE_MS.sql"

# database info
DB_NAME="db_investment"

# exec script
mysql -uroot ${DB_NAME} <<EOF
source ${SQL_CRE_CLS_MS}
source ${SQL_CRE_INDUSTRY_MS}
source ${SQL_CRE_SCALE_MS}
source ${SQL_CRE_BLAND_MS}
EOF

