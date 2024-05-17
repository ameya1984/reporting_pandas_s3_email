# Specify your AWS credentials and region
aws_access_key_id = 'YOUR_ACCESS_KEY_ID'
aws_secret_access_key = 'YOUR_SECRET_ACCESS_KEY'
aws_region = 'YOUR_REGION'

# Specify AWS S3 bucket name and filename
bucket_name = 'daily_lessons_bucket'
filename = 'daily_lessons_completed'

# Specify the sender and recipient email addresses
sender = 'daily_monitoring_service@mindtickle.com'
recipient = 'monitoring_stakeholders@example.com' # mailing list for monitoring stake holders


# Specify the email subject and body
subject = 'Daily number of lessons report'
body_text = 'Please check file attached.'

# Specify database credentials
mysql_conf = 'mysql+pymysql://root:password@localhost:55008/mt-mysql'

postgresql_conf = 'postgresql+psycopg2://user:password@localhost:55006/mt-pg'