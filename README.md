# Module 1 Homework

## Question 1: Understanding Docker Images

**Question:**  
Run Docker with the `python:3.13` image. Use an entrypoint `bash` to interact with the container.

What is the version of `pip` in the image?

**Command used:**

```bash
docker run --rm python:3.13 pip --version
```

**Answer:**

```text
pip 26.0.1 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)
```

---

## Question 2: Understanding Docker Networking and Docker Compose

**Question:**  
Given the Docker Compose setup, what hostname and port should PgAdmin use to connect to the Postgres database?

**Answer:**

```text
postgres:5432
```

**Explanation:**  
Inside the Docker Compose network, PgAdmin should connect to the Postgres container using the service/container hostname and the internal container port.

The mapped port `5433:5432` is only used when connecting from the host machine.  
Between containers, the correct port is `5432`.

---

## Question 3: Counting Short Trips

**Question:**  
For trips in November 2025, where `lpep_pickup_datetime` is between `2025-11-01` and `2025-12-01`, how many trips had a `trip_distance` less than or equal to `1` mile?

**SQL query:**

```sql
SELECT COUNT(trip_distance)
FROM green_tripdata_2025_11
WHERE lpep_pickup_datetime >= '2025-11-01'
  AND lpep_pickup_datetime < '2025-12-01'
  AND trip_distance <= 1;
```

**Answer:**

```text
8007
```

---

## Question 4: Longest Trip for Each Day

**Question:**  
Which pickup day had the longest trip distance?  
Only consider trips with `trip_distance` less than `100` miles to exclude data errors.

**SQL query:**

```sql
SELECT *
FROM green_tripdata_2025_11
WHERE trip_distance = (
  SELECT MAX(trip_distance)
  FROM green_tripdata_2025_11
  WHERE trip_distance < 100
);
```

**Result:**

```text
trip_distance: 88.03
pickup_datetime: 2025-11-14 15:36:27
```

**Answer:**

```text
2025-11-14
```

---

## Question 5: Biggest Pickup Zone

**Question:**  
Which pickup zone had the largest `total_amount` on November 18th, 2025?

**SQL query:**

```sql
SELECT
  t."PULocationID",
  z."Zone",
  SUM(t.total_amount) AS total_amount_sum
FROM green_tripdata_2025_11 t
JOIN taxi_zone_lookup z
  ON t."PULocationID" = z."LocationID"
WHERE t.lpep_pickup_datetime >= '2025-11-18'
  AND t.lpep_pickup_datetime < '2025-11-19'
GROUP BY t."PULocationID", z."Zone"
ORDER BY total_amount_sum DESC
LIMIT 3;
```

**Result:**

```text
PULocationID: 74
Zone: East Harlem North
total_amount_sum: 9281.92
```

**Answer:**

```text
East Harlem North
```

---

## Question 6: Largest Tip

**Question:**  
For passengers picked up in the zone named `East Harlem North` in November 2025, which drop-off zone had the largest tip?

**SQL query:**

```sql
SELECT
  t."DOLocationID",
  dz."Zone" AS dropoff_zone,
  MAX(t.tip_amount) AS max_tip
FROM green_tripdata_2025_11 t
JOIN taxi_zone_lookup pz
  ON t."PULocationID" = pz."LocationID"
JOIN taxi_zone_lookup dz
  ON t."DOLocationID" = dz."LocationID"
WHERE t.lpep_pickup_datetime >= '2025-11-01'
  AND t.lpep_pickup_datetime < '2025-12-01'
  AND pz."Zone" = 'East Harlem North'
GROUP BY t."DOLocationID", dz."Zone"
ORDER BY max_tip DESC
LIMIT 5;
```

**Result:**

```text
DOLocationID: 263
dropoff_zone: Yorkville West
max_tip: 81.89
```

**Answer:**

```text
Yorkville West
```

---

## Question 7: Terraform Workflow

**Question:**  
Which sequence describes the workflow for:

1. Downloading provider plugins and setting up the backend
2. Generating proposed changes and auto-executing the plan
3. Removing all resources managed by Terraform

**Answer:**

```text
terraform init, terraform apply -auto-approve, terraform destroy
```