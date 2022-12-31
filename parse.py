import pandas as pd

keyMap = {
    "ci": "checkin_time",
    "co": "checkout_time",
    "memb_no": "member_no",
    "memb_name": "member_name",
    "loc": "location",
}

df = pd.read_json("clean.json")
df.rename(columns=keyMap, inplace=True)
df["checkin_time"] = pd.to_datetime(df["checkin_time"])
df["checkout_time"] = pd.to_datetime(df["checkout_time"])
df["duration"] = df["checkout_time"] - df["checkin_time"]
df["duration_minutes"] = df["duration"].dt.total_seconds() / 60
df["duration_hours"] = df["duration_minutes"] / 60
df["date"] = df["checkin_time"].dt.date
df["year"] = df["checkin_time"].dt.year
df["month"] = df["checkin_time"].dt.month
df["day"] = df["checkin_time"].dt.day

# print(df)

import plotly.express as px

# duration stats
print(df["duration"].aggregate(["min", "max", "mean", "sum"]))

# duration by date
fig = px.line(
    df,
    x="date",
    y="duration_hours",
    title="Visit durations",
    labels={"duration_hours": "Duration (hour)"},
)
fig.write_image("duration_by_date.png")
fig.write_html("duration_by_date.html")

# no. of visits by location
visits = df.groupby(["year", "month", "location"])["checkin_time"].count().reset_index()
visits.rename(columns={"checkin_time": "count"}, inplace=True)
fig = px.bar(
    visits, "month", "count", color="location", title="Number of visits by month"
)
fig.write_image("visits_by_location.png")
fig.write_html("visits_by_location.html")
