FROM python:latest

RUN mkdir /apps
ADD movies_admin /apps/movies_admin
RUN pip3 install -r /apps/movies_admin/requirements/dev.txt

CMD ["python3","/apps/movies_admin/manage.py","print_settings"]
CMD ["python3","/apps/movies_admin/manage.py","migrate","--fake"]
CMD ["python3","/apps/movies_admin/manage.py","runserver", "0.0.0.0:8000"]
