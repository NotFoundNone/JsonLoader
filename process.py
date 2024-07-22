import db_operations
import file_operations

def process_data(date, cur):
    data = file_operations.load_json(date)

    # Загрузка записей плана
    for plan in data['data']['plans']:
        db_operations.update_or_insert_plan(cur, plan)

    # Загрузка записей поездов
    for train in data['data']['trains']:
        db_operations.update_or_insert_train(cur, train)

        # Загрузка записей расписания
        for rasp in train['rasp']:
            db_operations.update_or_insert_rasp(cur, rasp)

    # Запись успешной загрузки
    db_operations.log_load(cur, date)