def table(name, nomatch, fields, table, classes=[]):
    for field in fields:
        if field is str:
            raise TypeError("Fields must be a list of tuples or lists")
    for row in table:
        if len(row) != len(fields):
            raise IndexError("Length of all rows must be the same")

    from template_engine.main import render
    context = {
        "title": name,
        "thead": fields,
        "content": table,
        "table_classes": classes,
        "nomatch": nomatch,
    }
    return render("nodes/table.html", None, context)