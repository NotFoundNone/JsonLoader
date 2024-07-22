# JsonLoader

JsonLoader is a project designed to load JSON data into a PostgreSQL database. This project includes scripts to handle the insertion of data into specific tables, namely `plans`, `trains`, and `rasp`, with a predefined sequence for generating unique identifiers.

## Project Structure

```
JsonLoader/
│
├── data/
│   ├── data_YYYY-MM-DD.json
│   └── data_YYYY-MM-DD.json
│
├── config.py
├── db_operations.py
├── file_operations.py
├── main.py
├── settings.py
├── utils.py
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
CREATE SEQUENCE id_sequence
START WITH 1
INCREMENT BY 1;

-- Таблица для планов
CREATE TABLE plans (
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

-- Таблица для поездов
CREATE TABLE trains (
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
    FOREIGN KEY (id_plan) REFERENCES plans(id_plan)
);

CREATE TABLE rasp (
    id INT8 default nextval('id_sequence') PRIMARY KEY,
    id_plan INT8,
    train INT8,
    esr6 INT8,
    dor_sdach INT8,
    reg_sdach INT8,
    date_prib TIMESTAMP,
    date_otpr TIMESTAMP,
    ont_time_write TIMESTAMP,
    FOREIGN KEY (id_plan) REFERENCES plans(id_plan),
    FOREIGN KEY (id_plan, train) REFERENCES trains(id_plan, train)
);
```
