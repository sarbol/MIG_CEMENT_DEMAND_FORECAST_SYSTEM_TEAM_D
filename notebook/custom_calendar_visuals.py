import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
import pandas as pd
import numpy as np
import math
import calendar


def calendar_plot_binary(
    dates,
    data,
    cmap=None,
    title=None,
    figsize=(12, 8),
    ncols=3,
    value_label=False,
    date_label=True,
    month_label=True,
    weeknum_label=False,
):
    """
    Calendar heatmap for binary activity data.

    Parameters
    ----------
    dates : array-like
        Dates corresponding to each activity value.

    data : array-like
        Binary values:
            0 = no activity
            1 = activity

    cmap : matplotlib colormap, optional
        Colormap containing exactly two colours.
        Default:
            0 -> very light grey
            1 -> blue

    title : str, optional
        Overall figure title.

    figsize : tuple
        Figure size.

    ncols : int
        Number of calendar months per row.

    value_label : bool
        Display the activity value inside each day cell.

    date_label : bool
        Display day numbers.

    month_label : bool
        Display month names.

    weeknum_label : bool
        Display week numbers.

    Returns
    -------
    matplotlib.axes.Axes
    """

    # ---------------------------------------------------------
    # Prepare data
    # ---------------------------------------------------------

    df = pd.DataFrame({
        "date": pd.to_datetime(dates),
        "value": np.asarray(data)
    })

    df["value"] = df["value"].astype(int)

    # Make sure data is binary
    if not df["value"].isin([0, 1]).all():
        raise ValueError("calendar_plot_binary expects activity values of only 0 and 1.")

    # If duplicate dates exist, keep the maximum activity.
    # Therefore, if anything happened on a day -> activity = 1.
    df = (
        df.groupby("date", as_index=False)["value"]
        .max()
    )

    activity = dict(
        zip(
            df["date"].dt.normalize(),
            df["value"]
        )
    )

    # ---------------------------------------------------------
    # Default binary colour map
    # ---------------------------------------------------------

    if cmap is None:
        cmap = ListedColormap([
            "#eeeeee",   # 0 = no activity
            "#2166ac",   # 1 = activity
        ])

    # Require two colours
    if cmap.N < 2:
        raise ValueError("cmap must contain at least two colours.")

    # ---------------------------------------------------------
    # Determine months to display
    # ---------------------------------------------------------

    min_date = df["date"].min()
    max_date = df["date"].max()

    months = pd.period_range(
        min_date.to_period("M"),
        max_date.to_period("M"),
        freq="M"
    )

    nmonths = len(months)
    nrows = math.ceil(nmonths / ncols)

    # ---------------------------------------------------------
    # Figure
    # ---------------------------------------------------------

    fig, axes = plt.subplots(
        nrows=nrows,
        ncols=ncols,
        figsize=figsize,
        squeeze=False
    )

    axes = axes.flatten()

    # ---------------------------------------------------------
    # Calendar settings
    # ---------------------------------------------------------

    # Monday = 0 ... Sunday = 6
    calendar.setfirstweekday(calendar.MONDAY)

    weekday_names = [
        "Mon", "Tue", "Wed", "Thu",
        "Fri", "Sat", "Sun"
    ]

    # ---------------------------------------------------------
    # Draw each month
    # ---------------------------------------------------------

    for ax_idx, period in enumerate(months):

        ax = axes[ax_idx]

        year = period.year
        month = period.month

        cal = calendar.monthcalendar(year, month)

        nweeks = len(cal)

        # Calendar background
        ax.set_xlim(0, 7)
        ax.set_ylim(nweeks, 0)

        # -----------------------------------------------------
        # Month title
        # -----------------------------------------------------

        if month_label:
            month_name = period.strftime("%B %Y")

            ax.set_title(
                month_name,
                fontsize=11,
                fontweight="bold",
                pad=12
            )

        # -----------------------------------------------------
        # Weekday labels
        # -----------------------------------------------------

        ax.set_xticks(
            np.arange(7) + 0.5
        )

        ax.set_xticklabels(
            weekday_names,
            fontsize=8
        )

        ax.tick_params(
            axis="x",
            bottom=False,
            top=False,
            length=0
        )

        # Remove y axis
        ax.set_yticks([])

        # Remove spines
        for spine in ax.spines.values():
            spine.set_visible(False)

        # -----------------------------------------------------
        # Draw days
        # -----------------------------------------------------

        for week_idx, week in enumerate(cal):

            for weekday_idx, day in enumerate(week):

                # Empty cell before/after month
                if day == 0:
                    continue

                date = pd.Timestamp(
                    year=year,
                    month=month,
                    day=day
                )

                value = activity.get(
                    date.normalize(),
                    0
                )

                # -------------------------------------------------
                # FIXED COLOUR MAPPING
                #
                # This is the important part.
                #
                # 0 ALWAYS gets cmap[0]
                # 1 ALWAYS gets cmap[1]
                #
                # There is no per-month normalization.
                # -------------------------------------------------

                cell_color = cmap(value)

                rect = Rectangle(
                    (
                        weekday_idx,
                        week_idx
                    ),
                    1,
                    1,
                    facecolor=cell_color,
                    edgecolor="white",
                    linewidth=1.5
                )

                ax.add_patch(rect)

                # -------------------------------------------------
                # Day number
                # -------------------------------------------------

                if date_label:

                    # Choose text colour based on activity
                    text_color = (
                        "white"
                        if value == 1
                        else "#555555"
                    )

                    ax.text(
                        weekday_idx + 0.5,
                        week_idx + 0.5,
                        str(day),
                        ha="center",
                        va="center",
                        fontsize=8,
                        color=text_color
                    )

                # -------------------------------------------------
                # Activity value
                # -------------------------------------------------

                if value_label:

                    ax.text(
                        weekday_idx + 0.5,
                        week_idx + 0.78,
                        str(value),
                        ha="center",
                        va="center",
                        fontsize=6,
                        color="white" if value == 1 else "#777777"
                    )

        # -----------------------------------------------------
        # Optional week numbers
        # -----------------------------------------------------

        if weeknum_label:

            for week_idx, week in enumerate(cal):

                valid_days = [
                    d for d in week if d != 0
                ]

                if valid_days:

                    first_day = pd.Timestamp(
                        year=year,
                        month=month,
                        day=valid_days[0]
                    )

                    week_number = first_day.isocalendar().week

                    ax.text(
                        -0.18,
                        week_idx + 0.5,
                        str(week_number),
                        ha="right",
                        va="center",
                        fontsize=7,
                        color="#777777"
                    )

        # -----------------------------------------------------
        # Grid boundaries
        # -----------------------------------------------------

        ax.set_xlim(0, 7)
        ax.set_ylim(nweeks, 0)

    # ---------------------------------------------------------
    # Hide unused axes
    # ---------------------------------------------------------

    for i in range(nmonths, len(axes)):
        axes[i].set_visible(False)

    # ---------------------------------------------------------
    # Figure title
    # ---------------------------------------------------------

    if title is not None:

        fig.suptitle(
            title,
            fontsize=14,
            fontweight="bold",
            y=1.02
        )

    plt.tight_layout()

    # return axes



def calendar_plot_categorical(
    dates,
    data,
    cmap=None,
    category_colors=None,
    title=None,
    figsize=(12, 8),
    ncols=3,
    value_label=False,
    date_label=True,
    month_label=True,
    weeknum_label=False,
    legend=True,
    legend_title=None,
    missing_color="#F5F5F5",
    missing_label="No data",
):
    """
    Calendar heatmap for categorical data.

    Parameters
    ----------
    dates : array-like
        Dates corresponding to each data value.

    data : array-like
        Categorical values. Can contain any number of categories,
        provided there are at least 2.

        Examples:
            [0, 1]
            ["Good", "Neutral", "Alert"]
            ["Low", "Medium", "High", "Critical"]

    cmap : matplotlib colormap, list of colours, optional
        Colour map used to assign colours to categories.

        Examples:
            "RdYlGn"
            "viridis"
            ["#D32F2F", "#E0E0E0", "#388E3C"]

        If None, a default categorical palette is generated.

    category_colors : dict, optional
        Explicit mapping between categories and colours.

        Example:
            {
                "Alert": "#D32F2F",
                "Neutral": "#E0E0E0",
                "Good": "#388E3C"
            }

        When supplied, this takes precedence over cmap.

    title : str, optional
        Overall figure title.

    figsize : tuple
        Figure size.

    ncols : int
        Number of calendar months per row.

    value_label : bool
        Display category values inside each day cell.

    date_label : bool
        Display day numbers.

    month_label : bool
        Display month names.

    weeknum_label : bool
        Display ISO week numbers.

    legend : bool
        Whether to display a category legend.

    legend_title : str, optional
        Legend title.

    missing_color : str
        Colour for dates that are missing from the input data.

    missing_label : str
        Label used for missing dates in the legend.

    Returns
    -------
    axes : numpy.ndarray
        Array of matplotlib Axes objects.
    """

    # =========================================================
    # Prepare data
    # =========================================================

    df = pd.DataFrame({
        "date": pd.to_datetime(dates),
        "value": np.asarray(data)
    })

    # Remove rows with missing dates
    df = df.dropna(subset=["date"])

    if df.empty:
        raise ValueError("No valid dates were provided.")

    # Normalize dates so timestamps such as
    # 2026-01-01 12:00 and 2026-01-01 15:00
    # are treated as the same day.
    df["date"] = df["date"].dt.normalize()

    # =========================================================
    # Validate categories
    # =========================================================

    categories = pd.unique(
        df["value"].dropna()
    ).tolist()

    if len(categories) < 2:
        raise ValueError(
            "calendar_plot_categorical requires at least 2 categories."
        )

    # =========================================================
    # Handle duplicate dates
    # =========================================================
    #
    # If the same date occurs multiple times, this keeps
    # the LAST observed category.
    #
    # You can change this behaviour if needed.
    # =========================================================

    df = (
        df
        .drop_duplicates(
            subset="date",
            keep="last"
        )
        .reset_index(drop=True)
    )

    # Dictionary:
    #
    # date -> category
    #
    category_by_date = dict(
        zip(
            df["date"],
            df["value"]
        )
    )

    # =========================================================
    # Generate colours
    # =========================================================

    if category_colors is not None:

        missing_categories = [
            category
            for category in categories
            if category not in category_colors
        ]

        if missing_categories:
            raise ValueError(
                "Missing colours for categories: "
                f"{missing_categories}"
            )

        color_map = {
            category: category_colors[category]
            for category in categories
        }

    else:

        # -----------------------------------------------------
        # User supplied list of colours
        # -----------------------------------------------------

        if isinstance(cmap, (list, tuple)):

            if len(cmap) < len(categories):
                raise ValueError(
                    f"cmap contains {len(cmap)} colours, "
                    f"but {len(categories)} categories were found."
                )

            colors = list(cmap[:len(categories)])

        else:

            # -------------------------------------------------
            # Matplotlib colormap
            # -------------------------------------------------

            if cmap is None:

                # Default categorical colours
                default_colors = [
                    "#D32F2F",  # red
                    "#E0E0E0",  # grey
                    "#388E3C",  # green
                    "#1976D2",  # blue
                    "#F57C00",  # orange
                    "#7B1FA2",  # purple
                    "#00838F",  # teal
                    "#5D4037",  # brown
                    "#455A64",  # blue-grey
                    "#C2185B",  # pink
                ]

                if len(categories) > len(default_colors):
                    raise ValueError(
                        f"More than {len(default_colors)} categories "
                        "were supplied. Provide your own cmap or "
                        "category_colors."
                    )

                colors = default_colors[:len(categories)]

            else:

                # -------------------------------------------------
                # Convert string/name to Matplotlib cmap
                # -------------------------------------------------

                if isinstance(cmap, str):
                    cmap = plt.get_cmap(cmap)

                # Sample the colormap evenly
                colors = [
                    cmap(i / max(len(categories) - 1, 1))
                    for i in range(len(categories))
                ]

        color_map = dict(
            zip(categories, colors)
        )

    # =========================================================
    # Determine months
    # =========================================================

    min_date = df["date"].min()
    max_date = df["date"].max()

    months = pd.period_range(
        min_date.to_period("M"),
        max_date.to_period("M"),
        freq="M"
    )

    nmonths = len(months)

    nrows = math.ceil(
        nmonths / ncols
    )

    # =========================================================
    # Create figure
    # =========================================================

    fig, axes = plt.subplots(
        nrows=nrows,
        ncols=ncols,
        figsize=figsize,
        squeeze=False
    )

    axes = axes.flatten()

    # =========================================================
    # Calendar configuration
    # =========================================================

    calendar.setfirstweekday(
        calendar.MONDAY
    )

    weekday_names = [
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat",
        "Sun",
    ]

    # =========================================================
    # Draw months
    # =========================================================

    for ax_idx, period in enumerate(months):

        ax = axes[ax_idx]

        year = period.year
        month = period.month

        cal = calendar.monthcalendar(
            year,
            month
        )

        nweeks = len(cal)

        # -----------------------------------------------------
        # Calendar boundaries
        # -----------------------------------------------------

        ax.set_xlim(
            0,
            7
        )

        ax.set_ylim(
            nweeks,
            0
        )

        # -----------------------------------------------------
        # Month title
        # -----------------------------------------------------

        if month_label:

            ax.set_title(
                period.strftime("%B %Y"),
                fontsize=11,
                fontweight="bold",
                pad=12
            )

        # -----------------------------------------------------
        # Weekday labels
        # -----------------------------------------------------

        ax.set_xticks(
            np.arange(7) + 0.5
        )

        ax.set_xticklabels(
            weekday_names,
            fontsize=8
        )

        ax.tick_params(
            axis="x",
            bottom=False,
            top=False,
            length=0
        )

        # Remove y axis
        ax.set_yticks([])

        # Remove spines
        for spine in ax.spines.values():
            spine.set_visible(False)

        # =====================================================
        # Draw calendar cells
        # =====================================================

        for week_idx, week in enumerate(cal):

            for weekday_idx, day in enumerate(week):

                # -------------------------------------------------
                # Empty cells outside the month
                # -------------------------------------------------

                if day == 0:
                    continue

                date = pd.Timestamp(
                    year=year,
                    month=month,
                    day=day
                )

                # -------------------------------------------------
                # Get category
                # -------------------------------------------------

                category = category_by_date.get(
                    date,
                    None
                )

                # -------------------------------------------------
                # Determine colour
                # -------------------------------------------------

                if category is None:

                    cell_color = missing_color

                else:

                    cell_color = color_map[
                        category
                    ]

                # -------------------------------------------------
                # Draw rectangle
                # -------------------------------------------------

                rect = Rectangle(
                    (
                        weekday_idx,
                        week_idx
                    ),
                    1,
                    1,
                    facecolor=cell_color,
                    edgecolor="white",
                    linewidth=1.5
                )

                ax.add_patch(rect)

                # -------------------------------------------------
                # Determine text colour
                # -------------------------------------------------

                if category is None:

                    text_color = "#999999"

                else:

                    # White text generally works well for
                    # darker colours.
                    text_color = "white"

                    # Neutral/light colours need dark text.
                    if isinstance(
                        cell_color,
                        str
                    ):

                        # Simple handling for the default
                        # neutral grey.
                        if cell_color.upper() in [
                            "#E0E0E0",
                            "#EEEEEE",
                            "#F5F5F5",
                            "#FFFFFF",
                        ]:
                            text_color = "#555555"

                # -------------------------------------------------
                # Date label
                # -------------------------------------------------

                if date_label:

                    ax.text(
                        weekday_idx + 0.5,
                        week_idx + 0.5,
                        str(day),
                        ha="center",
                        va="center",
                        fontsize=8,
                        color=text_color
                    )

                # -------------------------------------------------
                # Category label
                # -------------------------------------------------

                if value_label and category is not None:

                    ax.text(
                        weekday_idx + 0.5,
                        week_idx + 0.78,
                        str(category),
                        ha="center",
                        va="center",
                        fontsize=5,
                        color=text_color
                    )

        # =====================================================
        # Week numbers
        # =====================================================

        if weeknum_label:

            for week_idx, week in enumerate(cal):

                valid_days = [
                    day
                    for day in week
                    if day != 0
                ]

                if not valid_days:
                    continue

                first_day = pd.Timestamp(
                    year=year,
                    month=month,
                    day=valid_days[0]
                )

                week_number = (
                    first_day.isocalendar().week
                )

                ax.text(
                    -0.18,
                    week_idx + 0.5,
                    str(week_number),
                    ha="right",
                    va="center",
                    fontsize=7,
                    color="#777777"
                )

    # =========================================================
    # Hide unused axes
    # =========================================================

    for i in range(
        nmonths,
        len(axes)
    ):
        axes[i].set_visible(False)

    # =========================================================
    # Legend
    # =========================================================

    if legend:

        handles = []

        for category in categories:

            handles.append(
                Line2D(
                    [0],
                    [0],
                    marker="s",
                    linestyle="",
                    markersize=10,
                    markerfacecolor=color_map[category],
                    markeredgecolor="white",
                    label=str(category)
                )
            )

        # Missing data
        handles.append(
            Line2D(
                [0],
                [0],
                marker="s",
                linestyle="",
                markersize=10,
                markerfacecolor=missing_color,
                markeredgecolor="white",
                label=missing_label
            )
        )

        fig.legend(
            handles=handles,
            title=legend_title,
            loc="upper center",
            bbox_to_anchor=(0.5, 0.01),
            ncol=min(
                len(handles),
                ncols * 2
            ),
            frameon=False
        )

    # =========================================================
    # Overall title
    # =========================================================

    if title is not None:

        fig.suptitle(
            title,
            fontsize=14,
            fontweight="bold",
            y=1.02
        )

    # Leave room for legend
    if legend:
        plt.tight_layout(
            rect=[0, 0.06, 1, 1]
        )
    else:
        plt.tight_layout()

    # return axes