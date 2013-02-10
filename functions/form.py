def form(name, fields, top="", bottom="", err="", submit=None):
    if submit == None:
        submit = name
    finalfields = []
    for field in fields:
        if len(field) < 3:
            raise SyntaxError("Not enough arguments to field")
        attr = {}
        if field[0] not in [0, 1, False, True]:
            raise SyntaxError("required is not a boolean")
        if field[0]:
            attr["required"] = ""

        attr["placeholder"] = field[1]
        attr["name"] = field[2]
        field = field[3:]
        if field and isinstance(field[0], str):
            attr["type"] = field[0]
            field = field[1:]

        for item in field:
            if not isinstance(item, tuple) and len(item) == 2:
                raise SyntaxError("Additional arguments must be a tuple of length 2")
            attr[item[0]] = item[1]

        finalfields.append(attr)
    from template_engine.main import render
    context = {
        "fields": finalfields,
        "name": name,
        "top": top,
        "bottom": bottom,
        "err": err,
        "submit": submit
    }
    return render("nodes/form.html", None, context)