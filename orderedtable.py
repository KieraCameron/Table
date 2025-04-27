"""
Rules:
table                       is a Table instance
table[row]                  returns a TableArray instance with unique_id row
table[column]               returns a TableArray instance with unique_id column
table[row][column]          returns a value at row, column
table[column][row]          is equivalent to table[row][column]
table_array[row_1:row_4]    returns a TableArray instance with rows from row_1 to row_4, and all columns
table_array[col_1:col_4]    returns a TableArray instance with columns from col_1 to col_4, and all rows
table[row_1:row_5]          returns a Table instance with a subset of the rows, and all columns
table[col_1:col_5]          returns a Table instance with all rows, and a subset of the columns
table[row_1:row_5][col_1:col_5]
                            returns a Table instance
table[row] = [...]          replaces TableArray.data with the array
table[column] = [...]       does the same
table_1[row_1] = table_2[row_2]
                            replaces the TableArray instance. row and column ids must match
table_1[col_1] = table_2[col_2]
                            replaces the TableArray instance. row and column ids must match
table_1[row_1] = table_2[col_1]
                            replaces the TableArray instance.
                            the unique id of row_1 must match the unique_id of col_1, and
                            same goes for data_ids.
table[row][column] = v      assigns the value at row, column with v
table[column][row] = v      is equivalent to assigning table[row][column]
table[row_1:row_3] = [[...],[...],[...]]
                            replaces the .data attribute in each TableArray from row_1 to row_3
                            with the values of each nested array
table[col_1:col_3] = [[...],[...],[...]]
                            does the same
table_1[row_1:row_3] = table_2
                            sets values of table_2 to table_1. row ids must match. column ids must match
table_1[col_1:col_3] = table_2
                            does the same
table_1[row_1:row_3][col_1:col_3] = table_2
                            does the same
table_1[row_1:row_3][col_1:col_3] =    [[a, b, c],
                                        [c, d, e],
                                        [f, g, h]]
                            does the same
table_1 + table_2           returns a Table. columns and rows can get added on.
                            values that do not exist get replaced by a default_value
table_1 - table_2           removes values all data, rows, and columns of table_2 from table_1.
                            row and column ids must match
Start with disallowing the return and assignment of lists.
See how feasible using only objects is.
I think using only objects will be easier for me and the user of this module.

self.data must have __len__, __iter__, be ordered,

"""
import csv


class TableArray:
    def __init__(self, unique_id, data, arrangement, data_ids=None, table=None, default_value=None):
        self.unique_id = unique_id
        self.data = data
        self.arrangement = arrangement
        self.table = table
        if table is not None and data_ids is not None:
            raise Exception("data ids are ambiguous. Both data_ids and table parameters are assigned.")
        elif table is not None:
            if arrangement is OrderedTable.COLUMN:
                self.data_ids = table._data_ids[OrderedTable.ROW]
            elif arrangement is OrderedTable.ROW:
                self.data_ids = table._data_ids[OrderedTable.COLUMN]
            else:
                assert False, "arrangement does not exist"
        elif data_ids is not None:
            self.data_ids = data_ids
        else:
            self.data_ids = range(len(self.data))
        self._as_dict = dict(zip(self.data_ids, self.data))
        self.default_value = default_value

    def _get_id_index(self, data_id):
        """gets index of column, returns None if None"""
        if data_id in self.data_ids:
            return self.data_ids.index(data_id)
        elif data_id is None:
            return None
        else:
            raise KeyError(f"The key '{data_id}' does not exist")

    def get_slice_section(self, slice_obj):
        start_index = self._get_id_index(slice_obj.start)
        stop_index = self._get_id_index(slice_obj.stop)
        step = slice_obj.step
        if not isinstance(step, int) and step is not None:
            raise TypeError("step must be None or of type 'int'")
        return slice(start_index, stop_index, step)

    def __getitem__(self, key):
        if isinstance(key, slice):
            section = self.get_slice_section(key)
            data_ids = self.data_ids[section]
            data = self.data[section]
            return TableArray(self.unique_id, data, self.arrangement, data_ids, None, self.default_value)
        elif key in self.data_ids:
            return self._as_dict[key]
        else:
            raise KeyError(f"The key '{key}' does not exist")

    def __iter__(self):
        return iter(self.data)

    def __repr__(self):
        s = ""
        if self.arrangement is OrderedTable.COLUMN:
            s = self.unique_id.__repr__() + "\t"
        return f"TableArray({self.data})"

class OrderedTable:
    ROW = object()
    COLUMN = object()
    def __init__(self, column_ids: list, row_ids: list, data, default_value=None):
        if len(row_ids) != len(data):
            raise ValueError("row ids do not have the same length as data")
        elif len(column_ids) != len(data[0]):  # assume data has values in it
            raise ValueError("number of columns in data should match column ids")
        self.default_value = default_value
        self._data_ids = {OrderedTable.COLUMN: column_ids,
                          OrderedTable.ROW: row_ids}
        self._structure = {OrderedTable.COLUMN: dict(),
                           OrderedTable.ROW: dict()}
        for i, col_id in enumerate(column_ids):
            values = [row[i] for row in data]
            self._structure[OrderedTable.COLUMN][col_id] = TableArray(col_id, values, OrderedTable.COLUMN, table=self, default_value=default_value)
        for row_number, row_id in enumerate(row_ids):
            self._structure[OrderedTable.ROW][row_id] = TableArray(row_id, data[row_number], OrderedTable.ROW, table=self, default_value=default_value)

    @property
    def data(self):
        return [row.data for row in self.rows.values()]

    @property
    def transposed_data(self):
        return[column.data for column in self.columns.values()]

    @property
    def row_ids(self):
        return self._data_ids[OrderedTable.ROW]

    @property
    def column_ids(self):
        return self._data_ids[OrderedTable.COLUMN]

    @property
    def rows(self):
        return self._structure[OrderedTable.ROW]

    @property
    def columns(self):
        return self._structure[OrderedTable.COLUMN]

    @staticmethod
    def extract_csv(filepath, parse_row=None, parse_column=None, parse_data=None, default_value=None):
        with open(filepath) as rawfile:
            rawfile = list(csv.reader(rawfile))
            headings = rawfile[0]
            del rawfile[0]
            if len(headings) == len(rawfile[0]):
                del headings[0]
            else:
                raise ValueError("length of heading must match data")
            if parse_column:
                headings = [parse_column(heading) for heading in headings]
            row_ids = list()
            if parse_row and parse_data:
                for row_number, row in enumerate(rawfile):
                    row_ids.append(parse_row(row[0]))
                    del rawfile[row_number][0]
                    for i, value in enumerate(rawfile[row_number]):
                        rawfile[row_number][i] = parse_data(value)
            elif parse_row:
                for row_number, row in enumerate(rawfile):
                    row_ids.append(parse_row(row[0]))
                    del rawfile[row_number][0]
            elif parse_data:
                for row_number, row in enumerate(rawfile):
                    row_ids.append(row[0])
                    del rawfile[row_number][0]
                    for i, value in enumerate(rawfile[row_number]):
                        rawfile[row_number][i] = parse_data(value)
            else:
                for row_number, row in enumerate(rawfile):
                    row_ids.append(row[0])
                    del rawfile[row_number][0]
            return OrderedTable(headings, row_ids, rawfile, default_value)


    def _get_slice_section(self, slice_obj):
        start_index = self._get_key_index(slice_obj.start)
        stop_index = self._get_key_index(slice_obj.stop)
        step = slice_obj.step
        if not isinstance(step, int) and step is not None:
            raise TypeError("step must be None or of type 'int'")
        return slice(start_index, stop_index, step)

    def _get_key_index(self, key):
        if key in self.column_ids:
            return self.column_ids.index(key)
        elif key in self.row_ids:
            return self.row_ids.index(key)
        elif key is None:
            return None
        else:
            raise KeyError(f"the key {key} does not exist")

    def __getitem__(self, key):
        if isinstance(key, slice):
            if key.start in self.column_ids and key.stop in self.row_ids or \
                key.start in self.row_ids and key.stop in self.column_ids:
                raise KeyError("start and stop slices must be both rows or columns")
            section = self._get_slice_section(key)
            if key.start is None and key.stop is None:
                if key.step is None:
                    return OrderedTable(self.column_ids, self.row_ids, self.data, self.default_value)
                else:
                    raise KeyError("step is defined without targeting rows or columns")
            elif key.start in self.column_ids or key.stop in self.column_ids:
                data = list()
                for row in self.data:
                    data.append(row[section])
                column_ids = self.column_ids[section]
                return OrderedTable(column_ids, self.row_ids, data, self.default_value)
            elif key.start in self.row_ids or key.stop in self.row_ids:
                data = self.data[section]
                row_ids = self.row_ids[section]
                return OrderedTable(self.column_ids, row_ids, data, self.default_value)
            assert False, "slice start, stop, and step not accounted for"
        elif key in self.column_ids:
            return self.columns[key]
        elif key in self.row_ids:
            return self.rows[key]
        else:
            raise KeyError(f"The key '{key}' does not exist")

    def transpose(self):
        return OrderedTable(self.row_ids, self.column_ids, self.transposed_data, self.default_value)

    def _split_row_ids(self, other):
        other_only_row_ids = list()
        matching_row_ids = list()
        for row_id in other.row_ids:
            if row_id in self.row_ids:
                matching_row_ids.append(row_id)
            else:
                other_only_row_ids.append(row_id)
        return other_only_row_ids, matching_row_ids

    def _has_conflicting_data(self, other, matching_column_ids, matching_row_ids):
        if matching_column_ids == [] or matching_row_ids == []:
            return False, None, None
        else:
            for row_id, column_id in zip(matching_row_ids, matching_column_ids):
                if self[row_id][column_id] != other[row_id][column_id]:
                    return True, row_id, column_id
            return False, None, None

    def _split_column_ids(self, other):
        other_only_column_ids = list()
        matching_column_ids = list()
        for column_id in other.column_ids:
            if column_id in self.column_ids:
                matching_column_ids.append(column_id)
            else:
                other_only_column_ids.append(column_id)
        return other_only_column_ids, matching_column_ids

    def _merge_data(self, other):
        other_only_column_ids, matching_column_ids = self._split_column_ids(other)
        other_only_row_ids, matching_row_ids = self._split_row_ids(other)
        has_conflicts, row_id, column_id = self._has_conflicting_data(other, matching_column_ids, matching_row_ids)
        if has_conflicts:
            raise ValueError(f"can not add tables with conflicting values at {row_id} and {column_id}")

        merged_data = self.data
        for row_id, column_id in zip(matching_row_ids, matching_column_ids):
            pass

    def __repr__(self):
        s = "\t"
        for c in self.column_ids:
            s += c.__str__() + "\t"
        s += "\n"
        for r in self.row_ids:
            s += r.__str__() + "\t" * 2
            for d in self.rows[r].data:
                s += d.__str__() + "\t" * 2
            s += "\n"
        return s




def test():
    bc = ["Date", "1 Mo", "1.5 Mo", "2 Mo", "3 Mo", "4 Mo"]
    br = ["a", "b", "c", "d"]
    bt = [list(range(row * len(bc) + 2, len(bc) + row * len(bc) + 2)) \
          for row in range(len(br))]
    t = OrderedTable(bc, br, bt)
    print("Table", t)
    print("rows")
    for r in br:
        print(t[r])
    print("columns")
    for c in bc:
        print(t[c])
    print(t["b"]["1.5 Mo"])
    print(t["1.5 Mo"]["b"])
    print(t["c":])
    t2 = t["1 Mo":"3 Mo"]
    print(t2)
    print(t2.transpose())
    print(t2["1 Mo"]["a"])
    print(t2.transpose().transposed_data)
    print(t)
    print(t["Date"::2]["a"::3])
    print(t["d"]["3 Mo":])
    print(t["Date"]["d":])

test()