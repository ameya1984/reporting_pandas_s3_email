import pandas as pd
from utilities import target_db, source_db, send_email
import io
import config
import datetime


def get_lesson_completion_df():
    my_engine = source_db.get_mt_mysql_db()
    return pd.read_sql('SELECT * FROM lesson_completion', my_engine)


def get_user_df():
    # Create a connection to the database
    pg_engine = source_db.get_mt_postgresql_db()
    return pd.read_sql("SELECT * FROM mindtickle_users WHERE active_status = 'active'", pg_engine)


def run_analytics(lesson_completion_df, users_df):

    # Convert completion_date to datetime obj
    lesson_completion_df['completion_date'] = pd.to_datetime(lesson_completion_df['completion_date'])
    
    # Group by lessons completed
    daily_lessons_completed = lesson_completion_df.groupby(['user_id', lesson_completion_df['completion_date'].dt.date]).size().reset_index(name='lessons_completed')

    # Merge with users_df to get user names of active users only
    result_df = daily_lessons_completed.merge(users_df, on='user_id')

    # Rename columns
    result_df.rename(columns={'user_name': 'Name', 'lessons_completed': 'Number of lessons completed', 'completion_date': 'completion_date'}, inplace=True)

    # Reorder columns
    result_df = result_df[['Name', 'Number of lessons completed', 'completion_date']]

    return result_df

def main():
    lesson_completion_df = get_lesson_completion_df()
    users_df = get_user_df()

    result_df = run_analytics(lesson_completion_df, users_df)

    # Save the result to buffer
    csv_buffer = io.StringIO()
    result_df.to_csv(csv_buffer, index=False)

    filename = f'{config.filename}_{str(datetime.datetime.now(datetime.UTC))}.csv'

    try:
        target_db.upload_to_s3(config.bucket_name, filename, csv_buffer)
    except: # If file is not uploaded to S3, then write it locally
        result_df.to_csv(filename, index=False)
        print("File is not uploaded to S3. Stored on disk")
    else:
        print("File uploaded to S3")
        try:
            send_email.send_email_with_s3(config.bucket_name, filename)
        except Exception as e:
            print(f"Error in send_email: {e}")
        else:
            print("Email is sent")


if __name__ == '__main__':
    main()
