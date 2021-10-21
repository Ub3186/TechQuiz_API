def convert_question(response):
        response["_id"] = str(response["_id"])
        return response