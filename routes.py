from config import app
from controller_functions import index, registerRequest, loginRequest, registerUser, loginUser, dashboard, user_request, create_request, user_request_list, item_list, fulfill_request_form, add_fulfilled

app.add_url_rule("/", view_func=index)
app.add_url_rule("/register", view_func=registerRequest)
app.add_url_rule("/login", view_func=loginRequest)
app.add_url_rule("/register_user", view_func=registerUser, methods=["POST"])
app.add_url_rule("/login_user", view_func=loginUser, methods=["POST"])
app.add_url_rule("/dashboard", view_func=dashboard)
app.add_url_rule("/item_list", view_func=item_list, methods=["POST"])
app.add_url_rule("/request", view_func=user_request)
app.add_url_rule("/create_request", view_func=create_request, methods=["POST"])
app.add_url_rule("/user_request_list", view_func=user_request_list)
app.add_url_rule("/fulfill_request_form", view_func=fulfill_request_form, methods=["POST"])
app.add_url_rule("/create_fulfilled_request", view_func=add_fulfilled, methods=["POST"])