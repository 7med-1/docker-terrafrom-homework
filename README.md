# Question 1. Understanding Docker images

Run docker with the python:3.13 image. Use an entrypoint bash to interact with the container.

What's the version of pip in the image? 

**answer = > docker run --rm my-python-app pip --version pip 26.0.1 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)**

# Question 2. Understanding Docker networking and docker-compose
Given the following docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database?

services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data


**answer = postgres:5433**


# Question 3. Counting short trips
For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound), how many trips had a trip_distance of less than or equal to 1 mile?


```
ny_taxi=# select count(trip_distance) from green_tripdata_2025_11 
where lpep_pickup_datetime >= '2025-11-01' 
and lpep_pickup_datetime <'2025-12-01' 
and trip_distance <= 1;  
 count                                                                                                        
-------
  8007
(1 row)
```

**answer = 8007**

# Question 4. Longest trip for each day
Which was the pick up day with the longest trip distance? Only consider trips with trip_distance less than 100 miles (to exclude data errors).

Use the pick up time for your calculations.


ny_taxi=# select max(trip_distance) from green_tripdata_2025_11 where trip_distance < 100 ;       
  max                                                                                                       
-------
 88.03
(1 row)

ny_taxi=# select * from green_tripdata_2025_11 where trip_distance = 88.03;                     
 VendorID | lpep_pickup_datetime | lpep_dropoff_datetime | store_and_fwd_flag | RatecodeID | PULocationID | DOLocationID | passenger_count | trip_distance | fare_amount | extra | mta_tax | tip_amount | tolls_amount | ehail_fee | improvement_surcharge | total_amount | payment_type | trip_type | congestion_surcharge | cbd_congestion_fee 
----------+----------------------+-----------------------+--------------------+------------+--------------+--------------+-----------------+---------------+-------------+-------+---------+------------+--------------+-----------+-----------------------+--------------+--------------+-----------+----------------------+--------------------
        2 | 2025-11-14 15:36:27  | 2025-11-14 18:40:48   | N                  |          4 |          130 |          265 |               2 |         88.03 |       610.6 |     0 |     0.5 |          0 |            0 |           |                     1 |        612.1 |            2 |         1 |                    0 |                  0
(1 row)

**answer = 2025-11-14**

# Question 5. Biggest pickup zone
Which was the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025?

select
    "PULocationID",
    sum(total_amount) as total_amount_sum
from green_tripdata_2025_11
where lpep_pickup_datetime >= '2025-11-18'
  and lpep_pickup_datetime <  '2025-11-19'
group by "PULocationID"
order by total_amount_sum desc
minit 3;

-[ RECORD 1 ]----+-------------------                                                                         
PULocationID     | 74
total_amount_sum | 9281.919999999996
-[ RECORD 2 ]----+-------------------
PULocationID     | 75
total_amount_sum | 6696.130000000003
-[ RECORD 3 ]----+-------------------
PULocationID     | 43
total_amount_sum | 2378.7899999999995


select * from taxi_zone_lookup where "LocationID" = 74 ;   

-[ RECORD 1 ]+------------------                                                                              
LocationID   | 74
Borough      | Manhattan
Zone         | East Harlem North
service_zone | Boro Zone


**answer = East Harlem North**


# Question 6. Largest tip
For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip?

Note: it's tip , not trip. We need the name of the zone, not the ID.


ny_taxi=# select  t."DOLocationID",max(t.tip_amount) as max_tip from green_tripdata_2025_11 t join taxi_zone_lookup z on t."PULocationID" = z."LocationID" where t.lpep_pickup_datetime >= '2025-11-01'  and t.lpep_pickup_datetime < '2025-12-01' and z."Zone" = 'East Harlem North' goupe by t."DOLocationID" order by max_tip desc limit 5;
 
 DOLocationID | max_tip                                                                                       
--------------+---------
          263 |   81.89
          138 |      50
           74 |      45
          146 |   34.25
          265 |    28.9
(5 rows)

ny_taxi=# select * from taxi_zone_lookup where "LocationID" = 263 ;
 LocationID |  Borough  |      Zone      | service_zone                                                       
------------+-----------+----------------+--------------
        263 | Manhattan | Yorkville West | Yellow Zone
(1 row)

**answer = Yorkville West**

# Question 7. Terraform Workflow
Which of the following sequences, respectively, describes the workflow for:

Downloading the provider plugins and setting up backend
Generating proposed changes and auto-executing the plan
Remove all resources managed by terraform


**answer = terraform import, terraform apply -y, terraform destroy**