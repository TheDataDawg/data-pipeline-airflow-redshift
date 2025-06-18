from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 test_queries=None,
                 expected_results=None,
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.test_queries = test_queries or []
        self.expected_results = expected_results or []

    def execute(self, context):
        self.log.info("Starting data quality checks...")

        if not self.test_queries or not self.expected_results:
            raise ValueError("Both test_queries and expected_results must be provided")

        if len(self.test_queries) != len(self.expected_results):
            raise ValueError("The number of test queries must match the number of expected results")

        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        for i, query in enumerate(self.test_queries):
            self.log.info(f"Running data quality check {i+1}: {query}")
            records = redshift.get_records(query)

            if not records or records[0][0] != self.expected_results[i]:
                raise ValueError(f"Data quality check {i+1} failed.\nExpected {self.expected_results[i]}, got {records[0][0]}")

            self.log.info(f"Data quality check {i+1} passed.")