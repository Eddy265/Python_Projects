import pandas as pd
import psycopg2
import sys
import warnings

warnings.filterwarnings("ignore")


def get_plan_data(from_date: str, to_date: str, plan: str):
    # Connect to the database
    conn = psycopg2.connect(
        host="hostname", database="db_name", user="postgres", password="password"
    )

    query1 = f"""With table1 as(SELECT
            accounts.id account_id,
            contracts.tier,
            TO_CHAR(publications.first_online_at, 'mm/yyyy') AS year_month,
        COUNT(publications.id) AS publications_count
        FROM accounts
        INNER JOIN groups on groups.account_id = accounts.id
        INNER JOIN publications on groups.id = publications.group_id
        INNER JOIN contracts on accounts.id = contracts.account_id
        WHERE publications.first_online_at IS NOT NULL 
            AND DATE_TRUNC('year', publications.first_online_at) BETWEEN '2021-01-01' 
            AND '2022-12-31'
            AND state = 'online' 
            AND tier IN ('free', 'bronze', 'silver', 'gold', 'enterprise')
        GROUP BY
        accounts.id,
        contracts.tier,
        year_month
        ORDER BY tier, TO_DATE('01/' || TO_CHAR(publications.first_online_at, 'mm/yyyy'), 'DD/MM/YYYY'))
        SELECT * FROM table1
        WHERE tier = '{plan}' and TO_DATE('01/' ||year_month, 'DD/MM/YYYY') BETWEEN TO_DATE('01/' || '{from_date}', 'DD/MM/YYY')
        AND TO_DATE('01/' || '{to_date}', 'DD/MM/YYYY')"""
    df = pd.read_sql(query1, conn)
    df.to_csv("C:/Users/euzoe/OneDrive/Desktop/DATA_ANALYSIS/data.csv", index=False)
    with open(
        "C:/Users/euzoe/OneDrive/Desktop/DATA_ANALYSIS/data.txt", "w"
    ) as publitas:
        pb = [",".join(i) for i in df.astype(str).values]
        publitas.writelines(",".join(df.columns))
        publitas.write("\n")
        for i in pb:
            publitas.write(i)
            publitas.write("\n")


get_plan_data(sys.argv[1], sys.argv[2], sys.argv[3])
