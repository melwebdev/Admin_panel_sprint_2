#Deployment

1. Один раз запускаем из ./Admin_panel_sprint_2/tasks $ docker-compose build
2. Распаковываем базу с тестовыми данными:
gzip -d ./Admin_panel_sprint_2/tasks/sql/movies_schema_dump.sql.gz
3. Редактируем файл ./Admin_panel_sprint_2/tasks/movies_admin/config/settings/.env
   (пример в ./Admin_panel_sprint_2/tasks/movies_admin/config/settings/.env_template)
   Ключ можно сгенерить, например такой: gir%u3s%^hfi1a_u@+!ipmukc5^#$d31fr!j9kxr^op=%(h3&a
  Скрипт генерации:
   from django.core.management.utils import get_random_secret_key  
   get_random_secret_key()
   
4. Запускаем из папки ./Admin_panel_sprint_2/tasks $ docker-compose up -d
Контейнеры поднимутся, но база postgres будет заполняться данными несколько минут,
   прежде чем будет готова принимать подключения. Её статус можно смотреть в логах командой $ docker-compose logs pg_db
   
5. Заходим http://127.0.0.1/admin
    user: admin
    password: pass123
   
6. Осановка контейнеров $ docker-compose stop