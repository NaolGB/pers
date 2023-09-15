def user_context(request):
    # get the request.user to any page without passing again
    # used for creating websocket in templates
    return {'user': request.user}
