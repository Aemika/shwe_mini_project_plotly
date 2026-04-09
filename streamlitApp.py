import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import json
from copy import deepcopy

st.write("Hello WOrld")

# df= pd.read_csv("../data/mpg.csv")
# st.dataframe(df) # nice way of interacting to view df

@st.cache_data # stramlit to cache this func meaning whenevr called its called its keeping tracking and track of output for same set of inputs and return already exec val
def load_data(path):
    df= pd.read_csv(path)
    return df


mpg_df_raw = load_data("./data/mpg.csv")
mpg_df = deepcopy(mpg_df_raw)

st.title("Introduction to Streamlit")
st.header("MPG Data Exploration")

#st.table(data = mpg_df)

if st.checkbox("Show Dataframe"):
    st.subheader("This is my dataset:")
    st.dataframe(mpg_df)

# left_column, right_column = st.columns(2)
# left_column.write("This is the left column")
# right_column.write("This is the right column")

left_column, middle_column, right_column = st.columns([3,1,1])
# [3,1,1]: sum = 5
# first column: 3/5 of the whole display width
# second column: 1/5 ...

# left_column.write("Left column here")
# middle_column.write("Middle")
# right_column.write("Right")
# with right_column:
#     st.write("This will be put into the right column")

years = ["All"] + sorted(pd.unique(mpg_df["year"]))
year = left_column.selectbox("Choose a year", years)

show_means = middle_column.radio("Show Class Means", ["Yes", "No"])

plot_types = ["Matplotlib", "Plotly"]
plot_type = right_column.radio("Choose Plot type", plot_types)

if year == "All":
    reduced_df = mpg_df
else:
    reduced_df = mpg_df[mpg_df["year"] == year]

means = reduced_df.groupby("class").mean(numeric_only=True)

# matplotlib
m_fig, ax = plt.subplots(figsize = (10,8))
ax.scatter(reduced_df["displ"], reduced_df["hwy"], alpha = 0.7)
ax.set_title("Engine Size vs Highway Size Fuelage")
ax.set_xlabel("Displacement (Liters)")
ax.set_ylabel("MPG")

if show_means == "Yes":
    ax.scatter(means["displ"], means["hwy"], alpha = 0.7, color = "red", label = "Class Means")

#st.pyplot(m_fig)


#plotly
p_fig = px.scatter(reduced_df, x = "displ", y="hwy", opacity = 0.5,
                   range_x = [1,8], range_y = [10,50],
                   width = 750, height = 600,
                   labels = {"displ" : "Displacement (Liters)", "hwy" : "MPG"},
                   title = "Engine Size vs Highway Size Fuelage"
                   )
p_fig.update_layout(title_font_size = 22)

if show_means == "Yes":
    p_fig.add_trace(go.Scatter(x=means["displ"], y = means ["hwy"],
                                mode = "markers", marker = {"color" : "red"}))
    p_fig.update_layout(showlegend = False)

#st.plotly_chart(p_fig)

if plot_type == "Matplotlib":
    st.pyplot(m_fig)
else:
    st.plotly_chart(p_fig)

st.subheader("Streamlit Map")

url = "https://archive.ics.uci.edu/ml/datasets/auto+mpg"
st.write("Data Source:", url)

# "This works too", url

st.subheader("Streamlit Map")

ds_geo = px.data.carshare()
ds_geo["lat"] = ds_geo["centroid_lat"]  # if not given gives err as it doesnt knw the axis
ds_geo["lon"] = ds_geo["centroid_lon"]

st.dataframe(ds_geo.head())

st.map(ds_geo)


####

TOTAL_clicked = 0
if st.button("press me"):
    TOTAL_clicked += 1

st.write(TOTAL_clicked)
st.session_state
