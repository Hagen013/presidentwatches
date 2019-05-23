from .controller import FavoritesController


def favorites_processor(request):
    controller = FavoritesController(request)
    print(controller.items_list)
    return {
        'favorites': controller
    }