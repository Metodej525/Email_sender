#prohledavani excelu, vraci prvnich jako list 5 hodnot podle value
def excel_search(value,excel_load):
    if excel_load[0]:
        df = excel_load[1]
        slice_df = df.loc[df['name'].str.contains(value, case=False, na=False)].head(5)
        return list(zip(slice_df['name'], slice_df['date']))
    return None
def excel_path_load():
    pass