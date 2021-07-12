FROM python
WORKDIR /tests_project/
COPY requirements.txt .
RUN pip install -U pip
RUN pip install -r requirements.txt
ENV ENV=dev
CMD python -m pytest -s -v --alluredir=test_results/ /tests_project/day_4/day_4_improvements/tests/
