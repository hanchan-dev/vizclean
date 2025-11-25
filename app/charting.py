# import matplotlib.pyplot as plt
# import numpy as np
#
# def line(df, title, x_label, y_label, x_col, y_col, color="red", markerfacecolor="blue", marker=".", markersize=10, linestyle="solid", linewidth=5, grid=False):
#
#     style = {
#         "marker": marker,
#         "markersize": markersize,
#         "markeredgecolor": "black",
#         "linestyle": linestyle,
#         "linewidth": linewidth,
#     }
#
#     plt.plot(df[x_col], df[y_col], color=color, markerfacecolor=markerfacecolor, **style)
#
#     plt.title(title,
#               fontsize=25,
#               family="sans-serif",
#               fontweight="bold",
#               color="black",)
#
#     plt.xlabel(x_label,
#                fontsize=20,
#                family="sans-serif",
#                fontweight="bold",
#                color="black")
#
#     plt.ylabel(y_label,
#                fontsize=20,
#                family="sans-serif",
#                fontweight="bold",
#                color="black")
#
#     # plt.xticks(np.arange(df[x_col].iloc[0], df[x_col].iloc[-1], step=1))
#     # plt.yticks(np.arange(df[y_col].iloc[0], df[y_col].iloc[-1], step=1))
#     plt.tick_params(axis="both",
#                     labelsize=10,
#                     color="black")
#
#     if grid:
#         plt.grid(axis="y",
#                  color="lightgray",
#                  linestyle="-",
#                  alpha=0.7)
#
#     plt.show()
#
#
# def bar(df, title, x_label, y_label, x_col, y_col, color="blue", grid=False):
#
#     plt.bar(df[x_col], df[y_col], color=color)
#
#     plt.title(title,
#               fontsize=25,
#               family="sans-serif",
#               fontweight="bold",
#               color="black", )
#
#     plt.xlabel(x_label,
#                fontsize=20,
#                family="sans-serif",
#                fontweight="bold",
#                color="black")
#
#     plt.ylabel(y_label,
#                fontsize=20,
#                family="sans-serif",
#                fontweight="bold",
#                color="black")
#
#     # plt.xticks(np.arange(df[x_col].iloc[0], df[x_col].iloc[-1], step=1))
#     # plt.yticks(np.arange(df[y_col].iloc[0], df[y_col].iloc[-1], step=1))
#     plt.tick_params(axis="both",
#                     labelsize=10,
#                     color="black")
#
#     if grid:
#         plt.grid(axis="y",
#                  color="lightgray",
#                  linestyle="-",
#                  alpha=0.7)
#
#     plt.show()
#
#
# def pie(df, title, pie_col, labels_col):
#
#     plt.pie(df[pie_col],
#             labels=df[labels_col],
#             autopct="%1.1f%%")
#
#     plt.title(title,
#               fontsize=25,
#               family="sans-serif",
#               fontweight="bold",
#               color="black", )
#
#     plt.show()
#
# def scatter(df, title, x_col1, y_col1, x_col2, y_col2, legend1, legend2, x_label, y_label, color1="red", color2="red", marker="o", markersize=50, markeredgecolor="black", grid=False):
#
#     plt.scatter(df[x_col1], df[y_col1],
#                 color=color1,
#                 marker=marker,
#                 s=markersize,
#                 label=legend1,
#                 alpha=0.8,
#                 markeredgecolor=markeredgecolor)
#
#     plt.scatter(df[x_col2], df[y_col2],
#                 color=color2,
#                 marker=marker,
#                 s=markersize,
#                 label=legend2,
#                 alpha=0.8,
#                 markeredgecolor=markeredgecolor)
#
#     plt.title(title)
#     plt.xlabel(x_label)
#     plt.ylabel(y_label)
#
#     if grid:
#         plt.grid(axis="y",
#                  color="lightgray",
#                  linestyle="-",
#                  alpha=0.7)
#
#     plt.legend()
#     plt.show()
#
# def histogram(df, title, col, x_label, y_label, bins=10, color="blue", grid=False):
#     plt.hist(df[col],
#              bins=bins,
#              color=color,
#              edgecolor="black")
#
#     plt.title(title,
#               fontsize=25,
#               family="sans-serif",
#               fontweight="bold",
#               color="black", )
#
#     plt.xlabel(x_label,
#                fontsize=20,
#                family="sans-serif",
#                fontweight="bold",
#                color="black")
#
#     plt.ylabel(y_label,
#                fontsize=20,
#                family="sans-serif",
#                fontweight="bold",
#                color="black")
#
#     if grid:
#         plt.grid(axis="y",
#                  color="lightgray",
#                  linestyle="-",
#                  alpha=0.7)
#
#     plt.show()
#
#
#
# def create_chart(chart_type, df, title, x_col, y_col=None, x_col1 = None, y_col2 = None, x_label="", y_label="", color1="red", color2="blue", legend1="", legend2="", marker=None, markersize=10, markerfacecolor="blue", linestyle="solid", linewidth=5, bins=10, grid=False):
#     if chart_type == "line":
#         line(df=df,
#              title=title,
#              x_col=x_col,
#              y_col=y_col,
#              x_label=x_label,
#              y_label=y_label,
#              color=color1,
#              marker=marker,
#              markersize=markersize,
#              markerfacecolor=markerfacecolor,
#              linestyle=linestyle,
#              linewidth=linewidth,
#              grid=grid)
#
#     elif chart_type == "bar":
#         bar(df=df,
#             title=title,
#             x_col=x_col,
#             y_col=y_col,
#             x_label=x_label,
#             y_label=y_label,
#             color=color1,
#             grid=grid)
#
#     elif chart_type == "pie":
#         pie(df=df,
#             title=title,
#             pie_col=y_col,
#             labels_col=x_col)
#
#     elif chart_type == "scatter":
#         scatter(df=df,
#                 title=title,
#                 x_col1=x_col,
#                 y_col1=y_col,
#                 x_col2=x_col1,
#                 y_col2=y_col2,
#                 legend1=legend1,
#                 legend2=legend2,
#                 x_label=x_label,
#                 y_label=y_label,
#                 color1=color1,
#                 color2=color2,
#                 marker=marker,
#                 markersize=markersize,
#                 markeredgecolor="black",
#                 grid=grid)
#
#
#     elif chart_type == "histogram":
#         histogram(df=df,
#                   title=title,
#                   col=x_col,
#                   x_label=x_label,
#                   y_label=y_label,
#                   bins=bins,
#                   color=color1,
#                   grid=grid)


# import matplotlib.pyplot as plt
# import numpy as np
#
#
# # ================================================================
# #  SETIAP CHART MENGGUNAKAN FIG DAN AX, BUKAN plt GLOBAL
# # ================================================================
#
# def line(ax, df, title, x_label, y_label, x_col, y_col,
#          color="red", markerfacecolor="blue", marker=".",
#          markersize=10, linestyle="solid", linewidth=5, grid=False):
#
#     style = {
#         "marker": marker,
#         "markersize": markersize,
#         "markeredgecolor": "black",
#         "linestyle": linestyle,
#         "linewidth": linewidth,
#     }
#
#     ax.plot(df[x_col], df[y_col], color=color,
#             markerfacecolor=markerfacecolor, **style)
#
#     ax.set_title(title, fontsize=20, fontweight="bold")
#     ax.set_xlabel(x_label, fontsize=12, fontweight="bold")
#     ax.set_ylabel(y_label, fontsize=12, fontweight="bold")
#     ax.tick_params(axis="both", labelsize=10)
#
#     if grid:
#         ax.grid(axis="y", color="lightgray", linestyle="-", alpha=0.7)
#
#
#
# def bar(ax, df, title, x_label, y_label, x_col, y_col,
#         color="blue", grid=False):
#
#     data = df[x_col].value_counts()
#
#     ax.bar(data.index, data.values, color=color)
#
#     ax.set_title(title, fontsize=20, fontweight="bold")
#     ax.set_xlabel(x_label, fontsize=12, fontweight="bold")
#     ax.set_ylabel(y_label, fontsize=12, fontweight="bold")
#     ax.tick_params(axis="both", labelsize=10)
#
#     if grid:
#         ax.grid(axis="y", color="lightgray", linestyle="-", alpha=0.7)
#
#
#
# def pie(ax, df, title, pie_col, labels_col):
#     ax.pie(df[pie_col], labels=df[labels_col], autopct="%1.1f%%")
#     ax.set_title(title, fontsize=20, fontweight="bold")
#
#
#
# def scatter(ax, df, title, x_col1, y_col1, x_col2, y_col2,
#             legend1, legend2, x_label, y_label,
#             color1="red", color2="blue",
#             marker="o", markersize=50, markeredgecolor="black",
#             grid=False):
#
#     ax.scatter(df[x_col1], df[y_col1],
#                color=color1, marker=marker,
#                s=markersize, label=legend1,
#                alpha=0.8, edgecolor=markeredgecolor)
#
#     ax.scatter(df[x_col2], df[y_col2],
#                color=color2, marker=marker,
#                s=markersize, label=legend2,
#                alpha=0.8, edgecolor=markeredgecolor)
#
#     ax.set_title(title, fontsize=20, fontweight="bold")
#     ax.set_xlabel(x_label, fontsize=12, fontweight="bold")
#     ax.set_ylabel(y_label, fontsize=12, fontweight="bold")
#
#     if grid:
#         ax.grid(axis="y", color="lightgray", linestyle="-", alpha=0.7)
#
#     ax.legend()
#
#
#
# def histogram(ax, df, title, col, x_label, y_label,
#               bins=10, color="blue", grid=False):
#
#     ax.hist(df[col], bins=bins, color=color, edgecolor="black")
#
#     ax.set_title(title, fontsize=20, fontweight="bold")
#     ax.set_xlabel(x_label, fontsize=12, fontweight="bold")
#     ax.set_ylabel(y_label, fontsize=12, fontweight="bold")
#
#     if grid:
#         ax.grid(axis="y", color="lightgray", linestyle="-", alpha=0.7)
#
#
#
# # ================================================================
# #  FUNGSI PEMBUNGKUS UTAMA → MENGHASILKAN FIG + AX
# # ================================================================
#
# def create_chart(chart_type, df, fig=None, *,
#                  title="", x_col=None, y_col=None,
#                  x_col1=None, y_col2=None,
#                  x_label="", y_label="",
#                  color1="red", color2="blue",
#                  legend1="", legend2="",
#                  marker=None, markersize=10,
#                  markerfacecolor="blue",
#                  linestyle="solid", linewidth=5,
#                  bins=10, grid=False):
#
#     # Buat fig jika belum ada
#     if fig is None:
#         fig = plt.figure()
#
#     ax = fig.add_subplot(111)
#
#     # Routing chart
#     if chart_type == "line":
#         line(ax, df, title, x_label, y_label,
#              x_col, y_col, color1, markerfacecolor,
#              marker, markersize, linestyle, linewidth, grid)
#
#     elif chart_type == "bar":
#         bar(ax, df, title, x_label, y_label,
#             x_col, y_col, color1, grid)
#
#     elif chart_type == "pie":
#         pie(ax, df, title, y_col, x_col)
#
#     elif chart_type == "scatter":
#         scatter(ax, df, title,
#                 x_col, y_col,
#                 x_col1, y_col2,
#                 legend1, legend2,
#                 x_label, y_label,
#                 color1, color2,
#                 marker, markersize,
#                 "black", grid)
#
#     elif chart_type == "histogram":
#         histogram(ax, df, title,
#                   x_col, x_label,
#                   y_label, bins,
#                   color1, grid)
#
#     fig.tight_layout()
#     return fig


# import matplotlib.pyplot as plt
#
#
# # ================================================================
# #   CHART MODEL BARU: 1 COLUMN INPUT → AUTO VALUE.COUNTS()
# # ================================================================
#
# def line(ax, df, title, x_label, y_label, col, color="red",
#          marker="o", markersize=6, linestyle="solid", linewidth=2, grid=False):
#
#     data = df[col].value_counts()
#
#     ax.plot(data.index, data.values,
#             color=color,
#             marker=marker,
#             markersize=markersize,
#             linestyle=linestyle,
#             linewidth=linewidth)
#
#     ax.set_title(title, fontsize=18, fontweight="bold")
#     ax.set_xlabel(x_label, fontsize=12)
#     ax.set_ylabel(y_label, fontsize=12)
#
#     if grid:
#         ax.grid(axis="y", color="lightgray", linestyle="--", alpha=0.7)
#
#
# def bar(ax, df, title, x_label, y_label, col, color="blue", grid=False):
#
#     data = df[col].value_counts()
#
#     ax.bar(data.index, data.values, color=color)
#
#     ax.set_title(title, fontsize=18, fontweight="bold")
#     ax.set_xlabel(x_label, fontsize=12)
#     ax.set_ylabel(y_label, fontsize=12)
#
#     if grid:
#         ax.grid(axis="y", color="lightgray", linestyle="--", alpha=0.7)
#
#
# def pie(ax, df, title, col):
#
#     data = df[col].value_counts()
#
#     ax.pie(data.values, labels=data.index, autopct="%1.1f%%")
#     ax.set_title(title, fontsize=18, fontweight="bold")
#
#
# def histogram(ax, df, title, col, x_label, y_label,
#               bins=10, color="blue", grid=False):
#
#     ax.hist(df[col].dropna(), bins=bins, color=color, edgecolor="black")
#
#     ax.set_title(title, fontsize=18, fontweight="bold")
#     ax.set_xlabel(x_label, fontsize=12)
#     ax.set_ylabel(y_label, fontsize=12)
#
#     if grid:
#         ax.grid(axis="y", color="lightgray", linestyle="--", alpha=0.7)
#
#
# def scatter(ax, df, title,
#             col_x, col_y, label_x, label_y,
#             color="red", marker="o", size=50, grid=False):
#
#     ax.scatter(df[col_x], df[col_y],
#                color=color, marker=marker, s=size, alpha=0.8)
#
#     ax.set_title(title, fontsize=18, fontweight="bold")
#     ax.set_xlabel(label_x, fontsize=12)
#     ax.set_ylabel(label_y, fontsize=12)
#
#     if grid:
#         ax.grid(axis="both", color="lightgray", linestyle="--", alpha=0.7)
#
#
# # ================================================================
# #   WRAPPER UTAMA
# # ================================================================
#
# def create_chart(chart_type, df, fig=None, *,
#                  title="", col=None,
#                  col_x=None, col_y=None,
#                  x_label="", y_label="",
#                  color="blue",
#                  marker="o", markersize=6,
#                  linestyle="solid", linewidth=2,
#                  bins=10, grid=False):
#
#     if fig is None:
#         fig = plt.figure()
#
#     ax = fig.add_subplot(111)
#
#     if chart_type == "line":
#         line(ax, df, title, x_label, y_label,
#              col=col,
#              color=color,
#              marker=marker,
#              markersize=markersize,
#              linestyle=linestyle,
#              linewidth=linewidth,
#              grid=grid)
#
#     elif chart_type == "bar":
#         bar(ax, df, title, x_label, y_label,
#             col=col, color=color, grid=grid)
#
#     elif chart_type == "pie":
#         pie(ax, df, title, col=col)
#
#     elif chart_type == "histogram":
#         histogram(ax, df, title, col,
#                   x_label, y_label,
#                   bins=bins, color=color, grid=grid)
#
#     elif chart_type == "scatter":
#         scatter(ax, df, title,
#                 col_x, col_y,
#                 x_label, y_label,
#                 color=color,
#                 marker=marker,
#                 size=markersize * 10,
#                 grid=grid)
#
#     fig.tight_layout()
#     return fig
#




import matplotlib.pyplot as plt


# ================================================================
#   CHART MODEL BARU: 1 COLUMN INPUT → AUTO VALUE.COUNTS()
#   + PATCH LIMIT
# ================================================================

def apply_limit(data, limit):
    """Potong data jika limit diberikan dan valid."""
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

    ax.plot(data.index, data.values,
            color=color1,
            marker=marker,
            markersize=markersize,
            linestyle=linestyle,
            linewidth=linewidth)

    ax.set_title(title, fontsize=18, fontweight="bold")
    ax.set_xlabel(x_label, fontsize=12)
    ax.set_ylabel(y_label, fontsize=12)

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

    if grid:
        ax.grid(axis="y", color="lightgray", linestyle="--", alpha=0.7)


def pie(ax, df, title, col, limit=None):

    data = df[col].value_counts()
    data = apply_limit(data, limit)

    ax.pie(data.values, labels=data.index, autopct="%1.1f%%")
    ax.set_title(title, fontsize=18, fontweight="bold")


def histogram(ax, df, title, col, x_label, y_label,
              bins=10, color1="blue", grid=False, limit=None):

    # histogram tidak pakai value_counts()
    # limit tidak relevan untuk histogram
    values = df[col].dropna()

    ax.hist(values, bins=bins, color=color1, edgecolor="black")

    ax.set_title(title, fontsize=18, fontweight="bold")
    ax.set_xlabel(x_label, fontsize=12)
    ax.set_ylabel(y_label, fontsize=12)

    if grid:
        ax.grid(axis="y", color="lightgray", linestyle="--", alpha=0.7)


# def scatter(ax, df, title, col_x, col_y,
#             label_x, label_y,
#             color="red", marker="o", size=50, grid=False, limit=None):
#
#     # Scatter tidak memakai value_counts
#     # Limit tidak relevan
#     ax.scatter(df[col_x], df[col_y],
#                color=color, marker=marker, s=size, alpha=0.8)
#
#     ax.set_title(title, fontsize=18, fontweight="bold")
#     ax.set_xlabel(label_x, fontsize=12)
#     ax.set_ylabel(label_y, fontsize=12)
#
#     if grid:
#         ax.grid(axis="both", color="lightgray", linestyle="--", alpha=0.7)

def scatter(ax, df, title, col_x, col_y,
            label_x, label_y,
            color1="red", marker="o", size=10,
            color2="blue", marker2="x", legend1=None, legend2=None,
            grid=False, limit=None):

    # =================================================================
    #   COL X = value_counts → jadi (index, value)
    #   COL Y = value_counts → jadi (index, value)
    # =================================================================

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

    # scatter pertama
    ax.scatter(
        data_x.index, data_x.values,
        color=color1,
        marker=marker,
        s=size,
        alpha=0.8,
        label=legend1
    )

    # scatter kedua
    ax.scatter(
        data_y.index, data_y.values,
        color=color2,
        marker=marker2,
        s=size,
        alpha=0.8,
        label=legend2,
    )

    ax.set_title(title, fontsize=18, fontweight="bold")
    ax.set_xlabel(label_x, fontsize=12)
    ax.set_ylabel(label_y, fontsize=12)
    ax.legend()

    if grid:
        ax.grid(axis="both", color="lightgray", linestyle="--", alpha=0.7)



# ================================================================
#   WRAPPER UTAMA
# ================================================================

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
                  bins=bins, color1=color1, grid=grid)

    elif chart_type == "scatter":
        scatter(
            ax, df, title,
            col_1, col_2,  # kolom scatter x & y
            x_label, y_label,
            color1=color1,  # warna set 1
            marker=marker,  # marker set 1
            size=markersize,
            color2=color2,  # warna set 2
            marker2=marker2,  # marker set 2
            grid=grid,
            limit=limit
        )

    fig.tight_layout()
    return fig
