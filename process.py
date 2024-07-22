import db_operations
import file_operations

def process_data(date, cur):
    data = file_operations.load_json(date)

    # Обработка плана
    for plan in data['data']['plans']:
        try:
            db_operations.update_or_insert_plan(cur, plan)
        except Exception as e:
            print(f"Ошибка при обработке plan: {e}, Данные: {plan}")

    # Обработка поездов
    for train in data['data']['trains']:
        try:
            db_operations.update_or_insert_train(cur, train)
        except Exception as e:
            print(f"Ошибка при обработке train: {e}, Данные: {train}")

        # Обработка расписания
        for rasp in train['rasp']:
            try:
                db_operations.update_or_insert_rasp(cur, rasp)
            except Exception as e:
                print(f"Ошибка при обработке rasp: {e}, Данные: {rasp}")

    # Запись успешной загрузки
    db_operations.log_load(cur, date)