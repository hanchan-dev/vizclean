import matplotlib.pyplot as plt
from matplotlib.pyplot import legend


def apply_limit(data, limit):

    # limit data
    if limit is None:
        return data

    try:
        limit = int(limit)
        if limit > 0:
            return data.head(limit)
    except:
        pass

    return data


def line(ax, df, title, x_label, y_label, col, color1="red",
         marker="o", markersize=6, linestyle="solid", linewidth=2,
         grid=False, limit=None):

    data = df[col].value_counts()
    data = apply_limit(data, limit)

    ax.plot(data.index.astype(str), data.values,
            color=color1,
            marker=marker,
            markersize=markersize,
            linestyle=linestyle,
            linewidth=linewidth)

    ax.set_title(title, fontsize=18, fontweight="bold")
    ax.set_xlabel(x_label, fontsize=12)
    ax.set_ylabel(y_label, fontsize=12)

    ax.tick_params(axis='x', rotation=30)

    if grid:
        ax.grid(axis="y", color="lightgray", linestyle="--", alpha=0.7)


def bar(ax, df, title, x_label, y_label, col, color1="blue",
        grid=False, limit=None):

    data = df[col].value_counts()
    data = apply_limit(data, limit)

    ax.bar(data.index, data.values, color=color1)

    ax.set_title(title, fontsize=18, fontweight="bold")
    ax.set_xlabel(x_label, fontsize=12)
    ax.set_ylabel(y_label, fontsize=12)

    ax.tick_params(axis='x', rotation=30)

    if grid:
        ax.grid(axis="y", color="lightgray", linestyle="--", alpha=0.7)


def pie(ax, df, title, col, limit=None):

    data = df[col].value_counts()
    data = apply_limit(data, limit)

    ax.pie(data.values, labels=data.index.astype(str), autopct="%1.1f%%")
    ax.set_title(title, fontsize=18, fontweight="bold")


def histogram(ax, df, title, col, x_label, y_label,
              bins=10, color1="blue", grid=False, limit=None):


    values = df[col].dropna()
    values = apply_limit(values, limit)

    ax.hist(values, bins=bins, color=color1, edgecolor="black")

    ax.set_title(title, fontsize=18, fontweight="bold")
    ax.set_xlabel(x_label, fontsize=12)
    ax.set_ylabel(y_label, fontsize=12)

    ax.tick_params(axis='x', rotation=30)

    if grid:
        ax.grid(axis="y", color="lightgray", linestyle="--", alpha=0.7)


def scatter(ax, df, title, col_x, col_y,
            label_x, label_y,
            color1="red", marker="o", size=10,
            color2="blue", marker2="x", legend1=None, legend2=None,
            grid=False, limit=None):


    #   COL X = value_counts → jadi (index, value)
    #   COL Y = value_counts → jadi (index, value)

    data_x = df[col_x].value_counts()
    data_y = df[col_y].value_counts()

    if limit is not None:
        try:
            limit = int(limit)
            if limit > 0:
                data_x = data_x.head(limit)
                data_y = data_y.head(limit)
        except:
            pass

    m = min(len(data_x), len(data_y))
    data_x = data_x.head(m)
    data_y = data_y.head(m)

    # scatter pertama
    ax.scatter(
        data_x.index.astype(str), data_x.values,
        color=color1,
        marker=marker,
        s=size,
        alpha=0.8,
        label=legend1
    )

    # scatter kedua
    ax.scatter(
        data_y.index.astype(str), data_y.values,
        color=color2,
        marker=marker2,
        s=size,
        alpha=0.8,
        label=legend2,
    )

    ax.set_title(title, fontsize=18, fontweight="bold")
    ax.set_xlabel(label_x, fontsize=12)
    ax.set_ylabel(label_y, fontsize=12)
    ax.tick_params(axis='x', rotation=30)
    ax.legend()

    if grid:
        ax.grid(axis="both", color="lightgray", linestyle="--", alpha=0.7)




#   WRAPPER UTAMA


def create_chart(chart_type, df, fig=None, *,
                 title="", col=None,
                 col_1=None, col_2=None,
                 x_label="", y_label="",
                 color1="blue",
                 marker="o", markersize=6,
                 linestyle="solid", linewidth=2,
                 bins=10, grid=False,
                 color2="red",
                 marker2="o",
                 legend1="",
                 legend2="",
                 limit=None):

    if fig is None:
        fig = plt.figure()

    ax = fig.add_subplot(111)

    if chart_type == "line":
        line(ax, df, title, x_label, y_label,
             col=col,
             color1=color1,
             marker=marker,
             markersize=markersize,
             linestyle=linestyle,
             linewidth=linewidth,
             grid=grid,
             limit=limit)

    elif chart_type == "bar":
        bar(ax, df, title, x_label, y_label,
            col=col, color1=color1, grid=grid, limit=limit)

    elif chart_type == "pie":
        pie(ax, df, title, col=col, limit=limit)

    elif chart_type == "histogram":
        histogram(ax, df, title, col,
                  x_label, y_label,
                  bins=bins, color1=color1, grid=grid, limit=limit)

    elif chart_type == "scatter":
        scatter(
            ax, df, title,
            col_1, col_2,
            x_label, y_label,
            color1=color1,
            marker=marker,
            size=markersize,
            color2=color2,
            marker2=marker2,
            legend1=legend1,
            legend2=legend2,
            grid=grid,
            limit=limit
        )

    fig.tight_layout()
    return fig
