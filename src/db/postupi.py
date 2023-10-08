import db

async def get_postupi_vuzes() -> list[list[str]]:
    connection = await db.connect_to_mysql()
    async with connection.cursor() as cursor:
        await cursor.execute(
            """select  
            vuz.name AS 'Наименование', 
            vuz.city  AS 'Город', 
            program.level AS 'Уровень', 
            spec.name AS 'Наименование специальности', 
            spec.code AS 'Код специальности', 
            spec.direction AS 'Подназвание', 
            program.name AS 'Наименование программы', 
            program.cost AS 'Стоимость', 
            IF(program.is_payment = 1, 'Есть платное обучение', 'Только бюджет') AS 'Плат / бюджет', 
            program.form AS 'Тип обучения', 
            program.duration_in_months AS 'Срок обучения в месяцах', 
            program.free_places AS 'Количество бюджетных мест', 
            program.payment_places AS 'Количество платных мест', 
            program.subjects AS 'Предметы'
            FROM short_vuz AS vuz
            LEFT JOIN short_specialization AS spec ON spec.vuz_id = vuz.id
            LEFT JOIN short_program AS program ON program.spec_id = spec.id""".strip())
        
        data = await cursor.fetchall()
        return data
    connection.close()