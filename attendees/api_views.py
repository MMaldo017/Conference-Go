from django.http import JsonResponse
from common.json import ModelEncoder
from .models import Attendee
from django.views.decorators.http import require_http_methods
import json
from events.models import Conference
class AttendeeListEncoder(ModelEncoder):
    model = Attendee
    properties = [
        "name",
        "email",

    ]

class AttendeeDetailEncoder(ModelEncoder):
    model = Attendee
    properties = [
        "name",
        "email",
        # "city",
        # # "room_court",
        # "created",
        # "updated",
    ]
@require_http_methods(["GET", "POST"])
def api_list_attendees(request, conference_id):
    """
    Lists the attendees names and the link to the attendee
    for the specified conference id.

    Returns a dictionary with a single key "attendees" which
    is a list of attendee names and URLS. Each entry in the list
    is a dictionary that contains the name of the attendee and
    the link to the attendee's information.

    {
        "attendees": [
            {
                "name": attendee's name,
                "href": URL to the attendee,
            },
            ...
        ]
    }
    """
    if request.method == "GET":
        attendees = Attendee.objects.filter(conference=conference_id)
        return JsonResponse(
            {"attendees": attendees},
            encoder=AttendeeListEncoder,
        )
    else:
        content = json.loads(request.body)

    # Get the Conference object and put it in the content dict
        try:
            conference = Conference.objects.get(id=conference_id)
            content["conference"] = conference
        except Conference.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid conference id"},
                status=400,
            )

        attendee = Attendee.objects.create(**content)
        return JsonResponse(
            attendee,
            encoder=AttendeeDetailEncoder,
            safe=False,
        )

    # attendees = [
    #     {
    #         "name": a.name,
    #         "href": a.get_api_url(),
    #     }
    #         for a in Attendee.objects.filter(conference=conference_id)
    # ]

    # return JsonResponse({"attendees": attendees})

@require_http_methods(["DELETE", "GET", "PUT"])
def api_show_attendee(request, id):
    """
    Returns the details for the Attendee model specified
    by the id parameter.

    This should return a dictionary with email, name,
    company name, created, and conference properties for
    the specified Attendee instance.

    {
        "email": the attendee's email,
        "name": the attendee's name,
        "company_name": the attendee's company's name,
        "created": the date/time when the record was created,
        "conference": {
            "name": the name of the conference,
            "href": the URL to the conference,
        }
    }
    """
    # attendee = Attendee.objects.get(id=id)
    # return JsonResponse(
    #     {
    #         "email" : attendee.email,
    #         "name" : attendee.name,
    #         "company_name": attendee.company_name,
    #         "created" : attendee.created,
    #         "conference" : {
    #             "name" : attendee.conference.name,
    #             "href": attendee.conference.get_api_url(),

    #         },
    #     }
    # )
    if request.method =="GET":
        attendee = Attendee.objects.get(id=id)
        return JsonResponse(
            attendee,
            encoder=AttendeeDetailEncoder,
            safe=False,
        )
    elif request.method == "DELETE":
        count, _ = Attendee.objects.filter(id=id).delete()
        return JsonResponse({"deleted": count > 0})

    else:
    # copied from create
        content = json.loads(request.body)
        # try:
        # # new code
        #     if "state" in content:
        #         state = State.objects.get(abbreviation=content["state"])
        #         content["state"] = state
        # except State.DoesNotExist:
        #     return JsonResponse(
        #         {"message": "Invalid state abbreviation"},
        #         status=400,
        # )

    # new code
        Attendee.objects.filter(id=id).update(**content)

    # copied from get detail
        attendee = Attendee.objects.get(id=id)
        return JsonResponse(
            attendee,
            encoder=AttendeeDetailEncoder,
            safe=False,
    )
