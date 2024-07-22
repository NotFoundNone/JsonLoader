import psycopg2
from datetime import datetime
from db_config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
import logging

logger = logging.getLogger(__name__)

def connect_db():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        options='-c client_encoding=UTF8'
    )
    return conn

def create_tables(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS load_log (
            date DATE PRIMARY KEY
        );
    """)

def get_last_loaded_date(cur):
    cur.execute("""
        SELECT MAX(date) FROM load_log;
    """)
    return cur.fetchone()[0]

def log_load(cur, date):
    cur.execute("""
        INSERT INTO load_log (date) VALUES (%s);
    """, (date,))

def update_or_insert_plan(cur, plan):
    try:
        cur.execute("""
            SELECT * FROM plans WHERE id_plan = %s;
        """, (plan['id_plan'],))
        existing_plan = cur.fetchone()

        if existing_plan:
            cur.execute("""
                UPDATE plans SET 
                    plan_num = %s,
                    plan_type = %s,
                    plan_date = %s,
                    plan_name = %s,
                    plan_time = %s,
                    train_count = %s,
                    ont_time_write = %s
                WHERE id_plan = %s;
            """, (
                plan['plan_num'],
                plan['plan_type'],
                datetime.strptime(plan['plan_date'], "%d-%m-%y") if plan['plan_date'] else None,
                plan['plan_name'],
                datetime.strptime(plan['plan_time'], "%d/%m/%y %H:%M") if plan['plan_time'] else None,
                plan['train_count'],
                datetime.strptime(plan['ont_time_write'], "%d/%m/%y %H:%M") if plan['ont_time_write'] else None,
                plan['id_plan']
            ))
            logger.info(f"Updated plan record. Data: {plan}")
        else:
            cur.execute("""
                INSERT INTO plans (id_plan, plan_num, plan_type, plan_date, plan_name, plan_time, train_count, ont_time_write)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """, (
                plan['id_plan'],
                plan['plan_num'],
                plan['plan_type'],
                datetime.strptime(plan['plan_date'], "%d-%m-%y") if plan['plan_date'] else None,
                plan['plan_name'],
                datetime.strptime(plan['plan_time'], "%d/%m/%y %H:%M") if plan['plan_time'] else None,
                plan['train_count'],
                datetime.strptime(plan['ont_time_write'], "%d/%m/%y %H:%M") if plan['ont_time_write'] else None
            ))
            logger.info(f"Inserted new plan record. Data: {plan}")
    except Exception as e:
        logger.error(f"Error when processing plan: {e}, Data: {plan}")


def update_or_insert_train(cur, train):
    try:
        cur.execute("""
            SELECT * FROM trains WHERE id_plan = %s AND train = %s AND num = %s;
        """, (train['id_plan'], train['train'], train['num']))
        existing_train = cur.fetchone()

        if existing_train:
            cur.execute("""
                UPDATE trains SET
                    index_poezd = %s,
                    st_fr = %s,
                    st_nz = %s,
                    date_op = %s,
                    st_poslop = %s,
                    code_poslop = %s,
                    date_poslop = %s,
                    mass = %s,
                    usl_dl = %s,
                    kol_vag = %s,
                    gr_vsego = %s,
                    gr_kr = %s,
                    gr_pl = %s,
                    gr_pv = %s,
                    gr_cs = %s,
                    gr_pr = %s,
                    por_vsego = %s,
                    por_kr = %s,
                    por_pl = %s,
                    por_pv = %s,
                    por_pvzs = %s,
                    por_pvzsfgk = %s,
                    por_cs = %s,
                    por_pr = %s,
                    ont_time_write = %s
                WHERE id_plan = %s AND train = %s AND num = %s;
            """, (
                train['index_poezd'],
                train['st_fr'],
                train['st_nz'],
                datetime.strptime(train['date_op'], "%d/%m/%y %H:%M") if train['date_op'] else None,
                train['st_poslop'],
                train['code_poslop'],
                datetime.strptime(train['date_poslop'], "%d/%m/%y %H:%M") if train['date_poslop'] else None,
                train['mass'],
                train['usl_dl'],
                train['kol_vag'],
                train['gr_vsego'],
                train['gr_kr'],
                train['gr_pl'],
                train['gr_pv'],
                train['gr_cs'],
                train['gr_pr'],
                train['por_vsego'],
                train['por_kr'],
                train['por_pl'],
                train['por_pv'],
                train['por_pvzs'],
                train['por_pvzsfgk'],
                train['por_cs'],
                train['por_pr'],
                datetime.strptime(train['ont_time_write'], "%d/%m/%y %H:%M:%S") if train['ont_time_write'] else None,
                train['id_plan'],
                train['train'],
                train['num']
            ))
            logger.info(f"Updated train record. Data: {train}")
        else:
            cur.execute("""
                INSERT INTO trains (id_plan, train, num, index_poezd, st_fr, st_nz, date_op, st_poslop, code_poslop, date_poslop,
                                    mass, usl_dl, kol_vag, gr_vsego, gr_kr, gr_pl, gr_pv, gr_cs, gr_pr, por_vsego, por_kr, por_pl,
                                    por_pv, por_pvzs, por_pvzsfgk, por_cs, por_pr, ont_time_write)
                VALUES (%s ,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (
                train['id_plan'],
                train['train'],
                train['num'],
                train['index_poezd'],
                train['st_fr'],
                train['st_nz'],
                datetime.strptime(train['date_op'], "%d/%m/%y %H:%M") if train['date_op'] else None,
                train['st_poslop'],
                train['code_poslop'],
                datetime.strptime(train['date_poslop'], "%d/%m/%y %H:%M") if train['date_poslop'] else None,
                train['mass'],
                train['usl_dl'],
                train['kol_vag'],
                train['gr_vsego'],
                train['gr_kr'],
                train['gr_pl'],
                train['gr_pv'],
                train['gr_cs'],
                train['gr_pr'],
                train['por_vsego'],
                train['por_kr'],
                train['por_pl'],
                train['por_pv'],
                train['por_pvzs'],
                train['por_pvzsfgk'],
                train['por_cs'],
                train['por_pr'],
                datetime.strptime(train['ont_time_write'], "%d/%m/%y %H:%M:%S") if train['ont_time_write'] else None
            ))
            logger.info(f"Inserted new train record. Data: {train}")
    except Exception as e:
        logger.error(f"Error when processing train: {e}, Data: {train}")


def update_or_insert_rasp(cur, rasp):
    try:
        cur.execute("""
            SELECT * FROM rasp WHERE id_plan = %s AND train = %s AND esr6 = %s AND dor_sdach = %s AND reg_sdach = %s;
        """, (rasp['id_plan'], rasp['train'], rasp.get('esr6'), rasp.get('dor_sdach'), rasp.get('reg_sdach')))
        existing_rasp = cur.fetchone()

        if existing_rasp:
            cur.execute("""
                UPDATE rasp SET 
                    date_prib = %s,
                    date_otpr = %s,
                    ont_time_write = %s
                WHERE id_plan = %s AND train = %s AND esr6 = %s AND dor_sdach = %s AND reg_sdach = %s;
            """, (
                datetime.strptime(rasp['date_prib'], "%Y-%m-%d %H:%M:%S %z") if rasp.get('date_prib') else None,
                datetime.strptime(rasp['date_otpr'], "%Y-%m-%d %H:%M:%S %z") if rasp.get('date_otpr') else None,
                datetime.strptime(rasp['ont_time_write'], "%d/%m/%y %H:%M:%S") if rasp.get('ont_time_write') else None,
                rasp['id_plan'],
                rasp['train'],
                rasp.get('esr6'),
                rasp.get('dor_sdach'),
                rasp.get('reg_sdach')
            ))
            logger.info(f"Updated rasp record. Data: {rasp}")
        else:
            cur.execute("""
                INSERT INTO rasp (id_plan, train, esr6, dor_sdach, reg_sdach, date_prib, date_otpr, ont_time_write)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """, (
                rasp['id_plan'],
                rasp['train'],
                rasp.get('esr6'),
                rasp.get('dor_sdach'),
                rasp.get('reg_sdach'),
                datetime.strptime(rasp['date_prib'], "%Y-%m-%d %H:%M:%S %z") if rasp.get('date_prib') else None,
                datetime.strptime(rasp['date_otpr'], "%Y-%m-%d %H:%M:%S %z") if rasp.get('date_otpr') else None,
                datetime.strptime(rasp['ont_time_write'], "%d/%m/%y %H:%M:%S") if rasp.get('ont_time_write') else None
            ))
            logger.info(f"Inserted new rasp record. Data: {rasp}")
    except Exception as e:
        logger.error(f"Error when processing rasp: {e}, Data: {rasp}")
