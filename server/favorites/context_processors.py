from .controller import FavoritesController


def favorites_processor(request):
    controller = FavoritesController(request)
    return {
        'favorites': controller
    }