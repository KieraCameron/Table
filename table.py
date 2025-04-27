class TableArray:
    def __init__(self, unique_id, data, arrangement, data_ids=None, table=None, default_value=None):
        self.unique_id = unique_id
        self.data = data
        self.arrangement = arrangement
        self.table = table
        if table is not None and data_ids is not None:
            raise Exception("data ids are ambiguous. Both data_ids and table parameters are assigned.")
        elif table is not None:
            if arrangement is Table.COLUMN:
                self.data_ids = table._data_ids[Table.ROW]
            elif arrangement is Table.ROW:
                self.data_ids = table._data_ids[Table.COLUMN]
            else:
                assert False, "arrangement does not exist"
        elif data_ids is not None:
            self.data_ids = data_ids
        else:
            self.data_ids = range(len(self.data))


        self._as_dict = dict(zip(self.data_ids, self.data))
        self.default_value = default_value

    def __getitem__(self, key):
        if key in self.data_ids:
            return self._as_dict[key]
        else:
            raise KeyError(f"The key '{key}' does not exist")

    def __iter__(self):
        return iter(self.data)

    def __repr__(self):
        s = ""
        if self.arrangement is Table.COLUMN:
            s = self.unique_id.__repr__() + "\t"
        return f"TableArray({self.data})"

class Table:
    ROW = object()
    COLUMN = object()
    def __init__(self, column_ids: iter, row_ids: iter, data, default_value=None):
        if len(row_ids) != len(data):
            raise ValueError("row ids do not have the same length as data")
        elif len(column_ids) != len(data[0]):  # assume data has values in it
            raise ValueError("number of columns in data should match column ids")
        self.default_value = default_value
        self._data_ids = {Table.COLUMN: set(column_ids),
                          Table.ROW: set(row_ids)}
        self._ordered_data_ids = {Table.COLUMN: column_ids,
                                  Table.ROW: row_ids}
        self._structure = {Table.COLUMN: dict(),
                           Table.ROW: dict()}
        for i, col_id in enumerate(column_ids):
            values = [row[i] for row in data]
            self._structure[Table.COLUMN][col_id] = TableArray(col_id, values, Table.COLUMN, table=self, default_value=default_value)
        for row_number, row_id in enumerate(row_ids):
            self._structure[Table.ROW][row_id] = TableArray(row_id, data[row_number], Table.ROW, table=self, default_value=default_value)

    @property
    def row_ids(self):
        return self._data_ids[Table.ROW]

    @property
    def column_ids(self):
        return self._data_ids[Table.COLUMN]

    @property
    def rows(self):
        return self._structure[Table.ROW]

    @property
    def columns(self):
        return self._structure[Table.COLUMN]

    def __getitem__(self, key) -> TableArray:
        if key in self.column_ids:
            return self.columns[key]
        elif key in self.row_ids:
            return self.rows[key]
        else:
            raise KeyError(f"The key '{key}' does not exist")

    def __repr__(self):
        s = "\t"
        for c in self.column_ids:
            s += c.__str__() + "\t"
        s += "\n"
        for r in self.row_ids:
            s += r.__str__() + "\t" * 2
            for c in self.column_ids:
                s += self[r][c].__str__() + "\t" * 2
            s += "\n"
        return s

def test():
    bc = ["Date", "1 Mo", "1.5 Mo", "2 Mo", "3 Mo", "4 Mo"]
    br = ["a", "b", "c", "d"]
    bt = [list(range(row * len(bc) + 2, len(bc) + row * len(bc) + 2)) \
          for row in range(len(br))]
    t = Table(bc, br, bt)
    print(t.column_ids)
    print(t.column_ids)
    print(t.row_ids)
    print(t.row_ids)
    print("Table", t)
    print("rows")
    for r in t.row_ids:
        print(t[r])
    print("columns")
    for c in bc:
        print(t[c])
    print(t["b"]["1.5 Mo"])
    print(t["1.5 Mo"]["b"])

test()