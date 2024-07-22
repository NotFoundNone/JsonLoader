from datetime import datetime, timedelta
import db_operations
import process

def main():
    conn = db_operations.connect_db()
    cur = conn.cursor()

    db_operations.create_tables(cur)

    # Получаем дату последней загрузки.
    last_loaded_date = db_operations.get_last_loaded_date(cur)

    if last_loaded_date is None:
        # Если данные еще не были загружены, начнём с 2023-01-01.
        start_date = datetime.strptime('2023-01-01', '%Y-%m-%d').date()
    else:
        # Начало с дня, следующего за последней загруженной датой.
        start_date = last_loaded_date + timedelta(days=1)

    # Загрузите данные за каждый день, начиная с даты начала и до сегодняшнего дня.
    end_date = datetime.today().date()
    current_date = start_date

    while current_date <= end_date:
        try:
            process.process_data(current_date, cur)
        except Exception as e:
            print(f"Ошибка обработки данных для {current_date}: {e}")
        current_date += timedelta(days=1)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    main()