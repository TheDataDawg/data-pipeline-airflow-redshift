from datetime import timedelta
import pendulum
from airflow.decorators import dag
from airflow.operators.dummy_operator import DummyOperator
from airflow.models import Variable
from final_project_operators.stage_redshift import StageToRedshiftOperator
from final_project_operators.load_fact import LoadFactOperator
from final_project_operators.load_dimension import LoadDimensionOperator
from final_project_operators.data_quality import DataQualityOperator
from udacity.common import final_project_sql_statements

default_args = {
    'owner': 'udacity',
    'depends_on_past': False,
    'start_date': pendulum.now(),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
}

@dag(
    default_args=default_args,
    description='Load and transform data in Redshift with Airflow',
    schedule_interval='0 * * * *'
)
def final_project():

    start_operator = DummyOperator(task_id='Begin_execution')

    stage_events_to_redshift = StageToRedshiftOperator(
        task_id='Stage_events',
        redshift_conn_id="redshift",
        table="staging_events",
        s3_bucket=Variable.get("s3_bucket"),
        s3_key=f"{Variable.get('s3_prefix')}/log-data",
        json_path=f"s3://{Variable.get('s3_bucket')}/{Variable.get('s3_prefix')}/log_json_path.json"
    )

    stage_songs_to_redshift = StageToRedshiftOperator(
        task_id='Stage_songs',
        redshift_conn_id="redshift",
        table="staging_songs",
        s3_bucket=Variable.get("s3_bucket"),
        s3_key=f"{Variable.get('s3_prefix')}/song-data",
        json_path="auto",
        region="us-east-1"
    )

    load_songplays_table = LoadFactOperator(
        task_id='Load_songplays_fact_table',
        redshift_conn_id='redshift',
        table='songplays',
        sql_query=final_project_sql_statements.SqlQueries.songplay_table_insert
    )

    load_user_dimension_table = LoadDimensionOperator(
        task_id='Load_user_dim_table',
        redshift_conn_id='redshift',
        table='users',
        sql_query=final_project_sql_statements.SqlQueries.user_table_insert,
        truncate_insert=True
    )

    load_song_dimension_table = LoadDimensionOperator(
        task_id='Load_song_dim_table',
        redshift_conn_id='redshift',
        table='songs',
        sql_query=final_project_sql_statements.SqlQueries.song_table_insert,
        truncate_insert=True
    )

    load_artist_dimension_table = LoadDimensionOperator(
        task_id='Load_artist_dim_table',
        redshift_conn_id='redshift',
        table='artists',
        sql_query=final_project_sql_statements.SqlQueries.artist_table_insert,
        truncate_insert=True
    )

    load_time_dimension_table = LoadDimensionOperator(
        task_id='Load_time_dim_table',
        redshift_conn_id='redshift',
        table='times',
        sql_query=final_project_sql_statements.SqlQueries.time_table_insert,
        truncate_insert=True
    )

    run_quality_checks = DataQualityOperator(
        task_id='Run_data_quality_checks',
        redshift_conn_id='redshift',
        test_queries=[
            "SELECT COUNT(*) FROM songplays WHERE playid IS NULL",
            "SELECT COUNT(*) FROM users WHERE userid IS NULL"
        ],
        expected_results=[0, 0]
    )

    end_operator = DummyOperator(task_id='Stop_execution')

    start_operator >> [stage_events_to_redshift, stage_songs_to_redshift]
    [stage_events_to_redshift, stage_songs_to_redshift] >> load_songplays_table
    load_songplays_table >> [
        load_user_dimension_table,
        load_song_dimension_table,
        load_artist_dimension_table,
        load_time_dimension_table
    ]
    [load_user_dimension_table, load_song_dimension_table, load_artist_dimension_table,
     load_time_dimension_table] >> run_quality_checks >> end_operator

final_project_dag = final_project()
