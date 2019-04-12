pushd  ./sql/atomic-tables/
PGPASSWORD="YOUR_PASSWORD_HERE" psql -h YOUR_REDSHIFT_ENDPOINT -U YOUR_REDSHIFT_USERNAME -d YOUR_REDSHIFT_DB -p 5439 -f atomic-def.sql
PGPASSWORD="YOUR_PASSWORD_HERE" psql -h YOUR_REDSHIFT_ENDPOINT -U YOUR_REDSHIFT_USERNAME -d YOUR_REDSHIFT_DB -p 5439 -f manifest-def.sql
popd

pushd  ./sql/com.snowplowanalytics.snowplow/
for file in *.sql
do
	PGPASSWORD="YOUR_PASSWORD_HERE" psql -h YOUR_REDSHIFT_ENDPOINT -U YOUR_REDSHIFT_USERNAME -d YOUR_REDSHIFT_DB -p 5439 -f "$file"
done

popd

pushd  ./sql/com.your_company/
for file in *.sql
do
	PGPASSWORD="YOUR_PASSWORD_HERE" psql -h YOUR_REDSHIFT_ENDPOINT -U YOUR_REDSHIFT_USERNAME -d YOUR_REDSHIFT_DB -p 5439 -f "$file"
done
popd