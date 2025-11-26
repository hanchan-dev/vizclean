# from gui.app_window import AppWindow
from app.core import charting as ct, data_loader as dl, data_cleaner as dc


def menu():
    print("\n========== VIZCLEAN CONSOLE ==========")
    print("1. Load dataset")
    print("2. Clean dataset (available after load dataset)")
    print("3. Show cleaning log (available after cleaning)")
    print("4. Save cleaned dataset (available after cleaning)")
    print("5. Generate chart (available after cleaning)")
    print("0. Exit")
    print("======================================")

def chart_menu():
    print("\n--- Chart Types ---")
    print("1. Line")
    print("2. Bar")
    print("3. Pie")
    print("4. Histogram")
    print("5. Scatter (2 columns)")
    print("-------------------")



CHART_FIELDS = {
    "line": [
        ("Column", "col"),
        ("Title", "title"),
        ("Color", "color1"),
        ("Grid (yes/no)", "grid"),
        ("X Label", "x_label"),
        ("Y Label", "y_label"),
        ("Marker", "marker"),
        ("Marker Size", "markersize"),
        ("Max Items (optional)", "limit")
    ],

    "bar": [
        ("Column", "col"),
        ("Title", "title"),
        ("X Label", "x_label"),
        ("Y Label", "y_label"),
        ("Color", "color1"),
        ("Grid (yes/no)", "grid"),
        ("Max Items (optional)", "limit")
    ],

    "pie": [
        ("Column", "col"),
        ("Title", "title"),
        ("Max Items (optional)", "limit")
    ],

    "scatter": [
        ("Column 1", "col_1"),
        ("Column 2", "col_2"),
        ("Title", "title"),
        ("X Label", "x_label"),
        ("Y Label", "y_label"),
        ("Color 1", "color1"),
        ("Color 2", "color2"),
        ("Marker 1", "marker"),
        ("Marker 2", "marker2"),
        ("Size", "markersize"),
        ("Grid (yes/no)", "grid"),
        ("Max Items (optional)", "limit")
    ],

    "histogram": [
        ("Column", "col"),
        ("Title", "title"),
        ("Bins", "bins"),
        ("Color", "color1"),
        ("X Label", "x_label"),
        ("Y Label", "y_label"),
        ("Grid (yes/no)", "grid"),
        ("Max Items (optional)", "limit")
    ]
}


def ask_chart_params(chart_type, df):
    print("\n=== Chart Parameters ===")

    params = {}

    COLUMN_KEYS = {"col", "col_1", "col_2"}
    for label, key in CHART_FIELDS[chart_type]:
        # Tampilkan list column jika field butuh column
        if key in COLUMN_KEYS:
            print(f"\nAvailable columns: {list(df.columns)}")

        val = input(f"{label}: ").strip()

        # ==== Convert otomatis ====
        if key == "grid":
            params[key] = (val.lower() == "yes")

        elif key == "bins":
            params[key] = int(val) if val.isdigit() else 10

        elif key == "markersize":
            params[key] = int(val) if val.isdigit() else 6

        elif key == "limit":
            params[key] = int(val) if val.isdigit() else None

        else:
            params[key] = val

    return params


def main():
    df_raw = None
    df_clean = None
    log_clean = None

    while True:
        menu()
        choice = input("Choose an option: ")

        # ------------------------------------------------------------
        # 1. LOAD DATASET
        # ------------------------------------------------------------
        if choice == "1":
            path = input("Enter file path: ")
            df_raw = dl.load_file(path)

            if df_raw is not None:
                print("\nDataset loaded successfully!")
                # print(df_raw.head().to_string())
            else:
                print("Failed to load file.")

            input("Press Enter to continue...")

        # ------------------------------------------------------------
        # 2. CLEAN DATASET
        # ------------------------------------------------------------
        elif choice == "2":
            if df_raw is None:
                print("You must load a dataset first!")
                continue

            df_clean, log_clean = dc.clean_data(df_raw)
            print("\nData cleaned successfully!")
            # print(df_clean.head().to_string())

            input("Press Enter to continue...")

        # ------------------------------------------------------------
        # 3. CLEANING LOG
        # ------------------------------------------------------------
        elif choice == "3":
            if log_clean is None:
                print("Clean the dataset first!")
                continue

            print("\n--- Cleaning Log ---")
            print(log_clean)

            input("Press Enter to continue...")

        # ------------------------------------------------------------
        # 4. SAVE CLEANED
        # ------------------------------------------------------------
        elif choice == "4":
            if df_clean is None:
                print("Clean the data first!")
                continue

            save_path = input("Enter filename: ")
            ext = input("Choose the type of cleaning (excel/csv/parquet): ")

            match(ext):
                case "excel":
                    df_clean.to_excel(save_path + ".xlsx", index=False)
                case "csv":
                    df_clean.to_csv(save_path + ".csv", index=False)
                case "parquet":
                    df_clean.to_parquet(save_path + ".parquet", index=False)
                case _:
                    print("Unsupported file type.")
                    continue

            print(f"Saved to {save_path}")

            input("Press Enter to continue...")

        # ------------------------------------------------------------
        # 5. GENERATE CHART (HANYA SETELAH CLEAN)
        # ------------------------------------------------------------
        elif choice == "5":
            if df_clean is None:
                print("Clean the data first, you impatient rascal.")
                continue

            chart_menu()
            ch = input("Chart type: ")

            mapping = {
                "1": "line",
                "2": "bar",
                "3": "pie",
                "4": "histogram",
                "5": "scatter"
            }

            if ch not in mapping:
                print("Invalid chart option.")
                continue

            chart_type = mapping[ch]

            params = ask_chart_params(chart_type, df_clean)

            # GENERATE FIGURE
            fig = ct.create_chart(chart_type, df_clean, **params)
            fig.show()

            input("Press Enter to continue...")

            # plt.show()

            # # LINE
            # if ch == "1":
            #     col = input("Column for line chart: ")
            #     fig = ct.create_chart("line", df_clean, col=col)
            #     plt.show()
            #
            # # BAR
            # elif ch == "2":
            #     col = input("Column for bar chart: ")
            #     fig = ct.create_chart("bar", df_clean, col=col)
            #     plt.show()
            #
            # # PIE
            # elif ch == "3":
            #     col = input("Column for pie chart: ")
            #     fig = ct.create_chart("pie", df_clean, col=col)
            #     plt.show()
            #
            # # HISTOGRAM
            # elif ch == "4":
            #     col = input("Numeric column: ")
            #     fig = ct.create_chart("histogram", df_clean, col=col)
            #     plt.show()
            #
            # # SCATTER
            # elif ch == "5":
            #     col_x = input("X column: ")
            #     col_y = input("Y column: ")
            #     fig = ct.create_chart("scatter", df_clean, col_1=col_x, col_2=col_y)
            #     plt.show()
            #
            # else:
            #     print("Invalid chart option.")

        # ------------------------------------------------------------
        # EXIT
        # ------------------------------------------------------------
        elif choice == "0":
            print("Goodbye.")
            break

        else:
            print("Invalid menu.")

if __name__ == '__main__':
    main()