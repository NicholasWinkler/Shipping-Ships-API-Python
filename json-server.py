import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status


# Add your imports below this line
from views import list_docks, retrieve_dock, delete_dock, update_dock
from views import list_haulers, retrieve_hauler, delete_hauler, update_hauler
from views import list_ships, retrieve_ship, delete_ship, update_ship, create_ship


class JSONServer(HandleRequests):
    """Server class to handle incoming HTTP requests for shipping ships"""

    def do_GET(self):
        """Handle GET requests from a client"""

        response_body = ""  # This is where a function first starts in the code
        url = self.parse_url(self.path)

        if url["requested_resource"] == "docks":
            if url["pk"] != 0:
                response_body = retrieve_dock(url["pk"])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

            response_body = list_docks()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "haulers":
            if url["pk"] != 0:
                response_body = retrieve_hauler(url["pk"])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

            response_body = list_haulers()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "ships":
            if url["pk"] != 0:
                response_body = retrieve_ship(url["pk"], url)
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

            response_body = list_ships(url) #pass an argument to list_ships to expand
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        else:
            return self.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def do_PUT(self):
        """Handle PUT requests from a client"""

        # Parse the URL and get the primary key
        url = self.parse_url(self.path)
        pk = url["pk"]

        # Get the request body JSON for the new data
        content_len = int(self.headers.get('content-length', 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)

        if url["requested_resource"] == "ships":
            if pk != 0:
                successfully_updated = update_ship(pk, request_body)
                if successfully_updated:
                    return self.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)

        elif url["requested_resource"] == "docks":
            if pk != 0:
                successfully_updated = update_dock(pk, request_body)
                if successfully_updated:
                    return self.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)

        if url["requested_resource"] == "haulers":
            if pk != 0:
                successfully_updated = update_hauler(pk, request_body)
                if successfully_updated:
                    return self.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)

        return self.response("Requested resource not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def do_DELETE(self):
        """Handle DELETE requests from a client"""

        url = self.parse_url(self.path)
        pk = url["pk"]

        if url["requested_resource"] == "ships":
            if pk != 0:
                successfully_deleted = delete_ship(pk)
                if successfully_deleted:
                    return self.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)

                return self.response("Requested resource not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

        elif url["requested_resource"] == "haulers":
            if pk != 0:
                successfully_deleted = delete_hauler(pk)
                if successfully_deleted:
                    return self.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)

                return self.response("Requested resource not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

        elif url["requested_resource"] == "docks":
            if pk != 0:
                successfully_deleted = delete_dock(pk)
                if successfully_deleted:
                    return self.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)

                return self.response("Requested resource not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

        else:
            return self.response("Not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)
    def do_POST(self):
        """Handle POST requests from a client"""
        # Parse the URL and get the requested resource
        url = self.parse_url(self.path)
        requested_resource = url["requested_resource"]

        # Get the request body JSON for the new resource data
        content_len = int(self.headers.get('content-length', 0)) # line of code checks how much data is coming in with the request.
        request_body = self.rfile.read(content_len) # line reads the actual data that was sent.
        request_body = json.loads(request_body) # line takes the raw data and turns it into a structured format that your program can understand.

        if requested_resource == "ships":
            # Create a new ship
            new_ship = create_ship(request_body)
            if new_ship:
                # Assuming the function returns the created ship with a new ID
                return self.response(json.dumps(new_ship), status.HTTP_201_SUCCESS_CREATED.value)
            
        elif requested_resource == "haulers"
            new_hauler = create_hauler(request_body)
            if new_hauler:
                return self.response(json.dumps(new_hauler), status.HTTP_201_SUCCESS_CREATED.value)

        elif requested_resource == "docks"
            new_dock = create_dock(request_body)
            if new_dock:
                return self.response(json.dumps(new_dock), status.HTTP_201_SUCCESS_CREATED.value)

        else:
            return self.response("Not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

#
# THE CODE BELOW THIS LINE IS NOT IMPORTANT FOR REACHING YOUR LEARNING OBJECTIVES
#
def main():
    host = ''
    port = 8000
    HTTPServer((host, port), JSONServer).serve_forever()

if __name__ == "__main__":
    main()