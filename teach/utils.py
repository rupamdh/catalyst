from django.core.paginator import Paginator

def create_pagination(object_list, page_number, item_to_show=10, ):
    paginator = Paginator(object_list, item_to_show)
    items = paginator.get_page(page_number)
    return items
