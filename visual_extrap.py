import matplotlib.pyplot as plt
import pandas as pd

# Define threads and points
threads = [2, 4, 8, 16, 64]  # Exclude 32 threads
points = [100, 1000, 10000, 100000, 1000000, 10000000, 100000000, 1000000000]

# C++ data
cpp_times = (
    pd.read_excel("Results.xlsx", sheet_name="C++")
    .groupby("Threads")
    .apply(lambda x: x["Time (seconds)"].tolist())
    .tolist()
)

# Go data
go_times = (
    pd.read_excel("Results.xlsx", sheet_name="Go")
    .groupby("Threads")
    .apply(lambda x: x["Time (seconds)"].tolist())
    .tolist()
)

# Python data
python_times = (
    pd.read_excel("Results.xlsx", sheet_name="Python")
    .groupby("Threads")
    .apply(lambda x: x["Time (seconds)"].tolist())
    .tolist()
)

# Plot
fig, ax = plt.subplots()

# Plot C++ data with solid lines
for i in range(len(threads)):
    ax.scatter(
        points, cpp_times[i], label=f"C++ - {threads[i]} Threads", marker="o"
    )
    ax.plot(
        points, cpp_times[i], linestyle="-", color="red"
    )  # Solid red lines for C++

# Plot Go data with blue lines
for i in range(len(threads)):
    ax.scatter(
        points, go_times[i], label=f"Go - {threads[i]} Threads", marker="x"
    )
    ax.plot(
        points, go_times[i], linestyle="-", color="blue"
    )  # Solid blue lines for Go

# Plot Python data with dashed lines
for i in range(len(threads)):
    ax.scatter(
        points,
        python_times[i],
        label=f"Python - {threads[i]} Threads",
        marker="^",
    )
    ax.plot(
        points, python_times[i], linestyle="--", color="green"
    )  # Dashed green lines for Python

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("Number of Points")
ax.set_ylabel("Time (seconds)")
ax.set_title("Comparison of Time vs Number of Points (C++ vs Go vs Python)")
ax.legend()
plt.grid(True, which="both", ls="--", lw=0.5)
plt.tight_layout()
plt.show()
