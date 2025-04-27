class TableArray:
    def __init__(self, unique_id, data, arrangement, data_ids=None, default_value=None):
        self.unique_id = unique_id
        self.data = data
        self.arrangement = arrangement
        assert data_ids is not None
        self.data_ids = data_ids

        self._as_dict = dict(zip(self.data_ids, self.data))
        self.data_ids = set(data_ids)
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
        self._structure = {Table.COLUMN: dict(),
                           Table.ROW: dict()}
        for i, col_id in enumerate(column_ids):
            values = [row[i] for row in data]
            self._structure[Table.COLUMN][col_id] = TableArray(col_id, values, Table.COLUMN, data_ids=row_ids, default_value=default_value)
        for row_number, row_id in enumerate(row_ids):
            self._structure[Table.ROW][row_id] = TableArray(row_id, data[row_number], Table.ROW, data_ids=column_ids, default_value=default_value)

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
    bc = ["1111", "2222", "3333", "4444", "5555", "6666"]
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

test()