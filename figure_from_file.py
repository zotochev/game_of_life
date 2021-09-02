def insert_figure(field: list, figure: list, x_left: int, y_top: int) -> list:
    x_field_size = len(field[0])
    y_field_size = len(field)
    x_figure_size = len(figure[0])
    y_figure_size = len(figure)

    if x_figure_size + x_left > x_field_size or y_figure_size + y_top > y_field_size:
        print("figure size is out of bounds of field")
        return field
    elif x_left < 0 or y_top < 0:
        print("invalid insert point")
        return field
    for index_y, y in enumerate(figure):
        for index_x, x in enumerate(y):
            field[index_y + y_top][index_x + x_left] = x
    return field


def figure_from_file(file: str) -> list:
    """
    http://www.radicaleye.com/lifepage/picgloss/picgloss.html
    """
    result = list()

    with open(file) as f:
        for row in f:
            result.append(list(map(lambda x: 1 if x == '*' else 0, list(row.strip()))))
    return result


fig = figure_from_file('figures/cross')
for i in fig:
    print(*i, sep='')

print()

cells = [[0 for y in range(20)] for x in range(20)]

insert_figure(cells, fig, 3, 3)

for i in cells:
    print(*i, sep='')
