# JsonLoader

JsonLoader is a project designed to load JSON data into a PostgreSQL database. This project includes scripts to handle the insertion of data into specific tables, namely `plans`, `trains`, and `rasp`, with a predefined sequence for generating unique identifiers.

## Project Structure

```
JsonLoader/
│
├── files/
│   ├── data_YYYY-MM-DD.json
│   └── data_YYYY-MM-DD.json
│
├── db_config.py
├── db_operations.py
├── file_operations.py
├── main.py
├── process.py
├── requirements.txt
├── utils.txt
└── local.env
```

## Prerequisites

- Python 3.7+
- PostgreSQL
- Required Python packages listed in `requirements.txt`

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/NotFoundNone/JsonLoader.git
    cd JsonLoader
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the PostgreSQL database:
    - Create a new PostgreSQL database.
    - Run the DDL statements provided below to create the necessary tables and sequence.

5. Configure the database connection:
    - Update the `.env` file with your database credentials.

## Database DDL

Run the following DDL statements to set up your PostgreSQL database:

```sql
CREATE TABLE ssp_plans (
    id INT8 default nextval('id_sequence') PRIMARY KEY,
    id_plan INT8 NOT NULL UNIQUE,
    plan_num TEXT NOT NULL,
    plan_type INT8 NOT NULL,
    plan_date DATE NOT NULL,
    plan_name TEXT NOT NULL,
    plan_time TIMESTAMP NOT NULL,
    train_count INT NOT NULL,
    ont_time_write TIMESTAMP
);

COMMENT ON COLUMN ssp_plans.id_plan IS 'Глобальный идентификатор плана с источника';
COMMENT ON COLUMN ssp_plans.plan_num IS 'Бизнес-номер, представляет день месяца для первой версии';
COMMENT ON COLUMN ssp_plans.plan_type IS 'Тип плана: 0 – основной, 1 – первая корректировка, 2 – вторая корректировка';
COMMENT ON COLUMN ssp_plans.plan_date IS 'Дата плановых ж/д суток, начинается после 18:00 предыдущей календарной даты';
COMMENT ON COLUMN ssp_plans.plan_name IS 'Наименование для отображения плана';
COMMENT ON COLUMN ssp_plans.plan_time IS 'Время формирования плана, например, 08:30';
COMMENT ON COLUMN ssp_plans.train_count IS 'Количество уникальных поездов в плане; может быть 0, что в текущем контексте указывает на сбойный план';
COMMENT ON COLUMN ssp_plans.ont_time_write IS 'Время записи строки в БД, формируется автоматически';

COMMENT ON TABLE ssp_plans IS 'Таблица для хранения информации о планах';

CREATE TABLE ssp_trains (
    id INT8 default nextval('id_sequence') PRIMARY KEY,
    id_plan INT8 NOT NULL,
    train INT8 NOT NULL,
    num INT8 NOT NULL,
    index_poezd TEXT NOT NULL,
    st_fr INT8 NOT NULL,
    st_nz INT8 NOT NULL,
    date_op TIMESTAMP,
    st_poslop INT8,
    code_poslop TEXT,
    date_poslop TIMESTAMP,
    mass INT8 NOT NULL,
    usl_dl INT8 NOT NULL,
    kol_vag INT8 NOT NULL,
    gr_vsego INT8,
    gr_kr INT8,
    gr_pl INT8,
    gr_pv INT8,
    gr_cs INT8,
    gr_pr INT8,
    por_vsego INT8,
    por_kr INT8,
    por_pl INT8,
    por_pv INT8,
    por_pvzs INT8,
    por_pvzsfgk INT8,
    por_cs INT8,
    por_pr INT8,
    ont_time_write TIMESTAMP,
    UNIQUE (id_plan, train),
    FOREIGN KEY (id_plan) REFERENCES ssp_plans(id_plan)
);

COMMENT ON COLUMN ssp_trains.id IS 'Внутренний идентификатор, формируется автоматически';
COMMENT ON COLUMN ssp_trains.id_plan IS 'Внутренний идентификатор плана на источнике, внешний ключ';
COMMENT ON COLUMN ssp_trains.train IS 'Порядковый номер в плане (от 1 и далее ориентировочно до 7000)';
COMMENT ON COLUMN ssp_trains.num IS 'Номер поезда';
COMMENT ON COLUMN ssp_trains.index_poezd IS 'Индекс поезда, блоки 6-3-6 цифр с лидирующими нулями, всего 15 символов';
COMMENT ON COLUMN ssp_trains.st_fr IS 'Станция формирования, ЕСР6';
COMMENT ON COLUMN ssp_trains.st_nz IS 'Станция назначения, ЕСР6';
COMMENT ON COLUMN ssp_trains.date_op IS 'Время операции';
COMMENT ON COLUMN ssp_trains.st_poslop IS 'Станция последней операции, ЕСР6';
COMMENT ON COLUMN ssp_trains.code_poslop IS 'Мнемокод последней операции';
COMMENT ON COLUMN ssp_trains.date_poslop IS 'Время последней операции';
COMMENT ON COLUMN ssp_trains.mass IS 'Масса, т';
COMMENT ON COLUMN ssp_trains.usl_dl IS 'Условная длина, вагонов';
COMMENT ON COLUMN ssp_trains.kol_vag IS 'Количество вагонов';
COMMENT ON COLUMN ssp_trains.gr_vsego IS 'Груженые всего';
COMMENT ON COLUMN ssp_trains.gr_kr IS 'Груженые крытые';
COMMENT ON COLUMN ssp_trains.gr_pl IS 'Груженые платформы';
COMMENT ON COLUMN ssp_trains.gr_pv IS 'Груженые полувагоны';
COMMENT ON COLUMN ssp_trains.gr_cs IS 'Груженые цистерны';
COMMENT ON COLUMN ssp_trains.gr_pr IS 'Груженые прочие';
COMMENT ON COLUMN ssp_trains.por_vsego IS 'Порожние всего';
COMMENT ON COLUMN ssp_trains.por_kr IS 'Порожние крытые';
COMMENT ON COLUMN ssp_trains.por_pl IS 'Порожние платформы';
COMMENT ON COLUMN ssp_trains.por_pv IS 'Порожние полувагоны';
COMMENT ON COLUMN ssp_trains.por_pvzs IS 'Порожние полувагоны в т.ч. на З-СИБ';
COMMENT ON COLUMN ssp_trains.por_pvzsfgk IS 'Порожние полувагоны в т.ч. на З-СИБ, из них ФГК';
COMMENT ON COLUMN ssp_trains.por_cs IS 'Порожние цистерны';
COMMENT ON COLUMN ssp_trains.por_pr IS 'Порожние прочие';
COMMENT ON COLUMN ssp_trains.ont_time_write IS 'Время записи строки в базу данных, формируется автоматически';

COMMENT ON TABLE ssp_trains IS 'Таблица для хранения атрибутов поездов';

CREATE TABLE ssp_rasp (
    id INT8 default nextval('id_sequence') PRIMARY KEY,
    id_plan INT8,
    train INT8,
    esr6 INT8,
    dor_sdach INT8,
    reg_sdach INT8,
    date_prib TIMESTAMP,
    date_otpr TIMESTAMP,
    ont_time_write TIMESTAMP,
    FOREIGN KEY (id_plan) REFERENCES ssp_plans(id_plan),
    FOREIGN KEY (id_plan, train) REFERENCES ssp_trains(id_plan, train)
);

COMMENT ON COLUMN ssp_rasp.id IS 'Внутренний идентификатор, формируется автоматически';
COMMENT ON COLUMN ssp_rasp.id_plan IS 'Внутренний идентификатор плана на источнике, внешний ключ';
COMMENT ON COLUMN ssp_rasp.train IS 'Порядковый номер в плане, внешний ключ';
COMMENT ON COLUMN ssp_rasp.esr6 IS 'ЕСР6 станции';
COMMENT ON COLUMN ssp_rasp.dor_sdach IS 'Код дороги сдачи поезда, только для стыковых пунктов дорог и пограничных переходов. В случае пограничного перехода, указывается код государства';
COMMENT ON COLUMN ssp_rasp.reg_sdach IS 'Код региона сдачи поезда, только для внутридорожных стыковых пунктов';
COMMENT ON COLUMN ssp_rasp.date_prib IS 'Время прибытия, есть только при наличии стоянки на станции или на конечной станции';
COMMENT ON COLUMN ssp_rasp.date_otpr IS 'Время отправления, есть всегда кроме конечной станции';
COMMENT ON COLUMN ssp_rasp.ont_time_write IS 'Время записи строки в базу данных, формируется автоматически';

COMMENT ON TABLE ssp_rasp IS 'Таблица для хранения расписаний поездов';
```
