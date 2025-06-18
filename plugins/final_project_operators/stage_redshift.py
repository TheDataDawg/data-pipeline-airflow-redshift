from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.models import Variable


class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 s3_bucket="",
                 s3_key="",
                 json_path="auto",
                 region="us-east-1",
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.json_path = json_path
        self.region = region

    def execute(self, context):
        self.log.info("Staging data from S3 to Redshift...")

        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        rendered_key = self.s3_key.format(**context)
        s3_path = f"s3://{self.s3_bucket}/{rendered_key}"

        # Retrieve AWS credentials directly from Airflow Variables
        aws_access_key = Variable.get("AWS_ACCESS_KEY_ID")
        aws_secret_key = Variable.get("AWS_SECRET_ACCESS_KEY")

        copy_sql = f"""
        COPY {self.table}
        FROM '{s3_path}'
        ACCESS_KEY_ID '{aws_access_key}'
        SECRET_ACCESS_KEY '{aws_secret_key}'
        REGION '{self.region}'
        FORMAT AS JSON '{self.json_path}'
        TRUNCATECOLUMNS
        BLANKSASNULL
        EMPTYASNULL
        ACCEPTINVCHARS
        MAXERROR 100;
        """

        self.log.info(f"Executing COPY command:\n{copy_sql}")
        redshift.run(f"TRUNCATE TABLE {self.table};")
        redshift.run(copy_sql)
        self.log.info(f"COPY command complete for {self.table}")
