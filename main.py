from app.core import charting as ct, data_loader as dl, data_cleaner as dc


def menu():
    print("\n========== VIZCLEAN CONSOLE ==========")
    print("1. Load dataset")
    print("2. Clean dataset (available after load dataset)")
    print("3. Show cleaning log (available after cleaning)")
    print("4. Save cleaned dataset (available after cleaning)")
    print("5. Generate chart (available for raw or cleaned dataset)")
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
        ("Legend 1", "legend1"),
        ("Legend 2", "legend2"),
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

        # 1. LOAD DATASET

        if choice == "1":
            path = input("Enter file path: ")
            df_raw = dl.load_file(path)

            if df_raw is not None:
                print("\nDataset loaded successfully!")
                # print(df_raw.head().to_string())
            else:
                print("Failed to load file.")

            input("Press Enter to continue...")



        # 2. CLEAN DATASET

        elif choice == "2":
            if df_raw is None:
                print("You must load a dataset first!")
                continue

            df_clean, log_clean = dc.clean_data(df_raw)
            print("\nData cleaned successfully!")
            # print(df_clean.head().to_string())

            input("Press Enter to continue...")



        # 3. CLEANING LOG

        elif choice == "3":
            if log_clean is None:
                print("Clean the dataset first!")
                continue

            print("\n--- Cleaning Log ---")
            print(log_clean)

            input("Press Enter to continue...")



        # 4. SAVE CLEANED

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



        # 5. GENERATE CHART (HANYA SETELAH CLEAN)

        elif choice == "5":
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

            if df_clean is None:
                params = ask_chart_params(chart_type, df_raw)
                fig = ct.create_chart(chart_type, df_raw, **params)


            else:
                params = ask_chart_params(chart_type, df_clean)
                fig = ct.create_chart(chart_type, df_clean, **params)

            # GENERATE FIGURE
            fig.show()

            save = input("\nSave chart as image? (yes/no): ").strip().lower()

            if save == "yes":
                filename = input("Enter filename (without extension): ").strip()
                ext = input("Choose format (png/jpg/svg): ").strip().lower()

                if ext not in {"png", "jpg", "svg"}:
                    print("Unsupported format. Using PNG instead.")
                    ext = "png"

                fullpath = f"{filename}.{ext}"
                try:
                    fig.savefig(fullpath, dpi=300, bbox_inches="tight")
                    print(f"Chart saved as: {fullpath}")
                except Exception as e:
                    print("Failed to save chart:", e)

            input("Press Enter to continue...")


        # EXIT

        elif choice == "0":
            print("Goodbye.")
            break

        else:
            print("Invalid menu.")

if __name__ == '__main__':
    main()