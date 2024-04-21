links = [
    {
        "label": "Home",
        "href": "/",
        "icon": "bi bi-house-door"
    },
]

def navbar(request):
    def add_active(link):
        copy = link.copy()

        if copy["href"] == "/":
            copy["active"] = request.path == "/"
        else:
            copy["active"] = request.path.startswith(copy.get("href", ""))

        return copy

    return {
        "links": map(add_active, links)
    }