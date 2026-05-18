import pandas as pd
from database import add_item, clear_all, get_all_items

def import_from_excel(file_path, overwrite=True):
    try:
        # Load the excel file
        # header=0 tells pandas to use the first row as headers (skipping it for data)
        df = pd.read_excel(file_path, header=0)
        
        if overwrite:
            clear_all()
        
        count = 0
        duplicates = 0
        
        for _, row in df.iterrows():
            try:
                # C# Logic Mapping:
                # A1 (Col 1) -> row[0]
                # A2 (Col 2) -> row[1]
                # A3 (Col 3) -> row[2]
                # A4 (Col 4) -> row[3]
                # A5 (Col 6) -> row[5] (Note: C# skips index 5/Col 5 which is 'Tong')
                
                item_id = str(row.iloc[0]).upper()
                name = str(row.iloc[1])
                qty = int(row.iloc[2])
                price = int(row.iloc[3])
                total = qty * price
                note = str(row.iloc[5]) if len(row) > 5 else ""

                success = add_item(item_id, name, qty, price, total, note)
                if success:
                    count += 1
                else:
                    duplicates += 1
            except Exception:
                continue # Skip rows with bad data format
                
        return count, duplicates
    except Exception as e:
        print(f"Error importing: {e}")
        return -1, 0

def export_to_excel(file_path):
    try:
        data = get_all_items()
        df = pd.DataFrame(data, columns=["Mã hàng", "Tên hàng", "Số lượng", "Giá tiền", "Tổng tiền", "Ghi chú"])
        df.to_excel(file_path, index=False)
        return True
    except Exception as e:
        print(f"Error exporting: {e}")
        return False