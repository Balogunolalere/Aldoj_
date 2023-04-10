import csv
import json
from django.http import HttpResponse

def user_to_dict(user):
    investments = [{'id': investment.id, 'name': investment.property.title} for investment in user.investment_set.all()]
    return {
        'id': user.id,
        'username': user.username,
        'investments': investments
    }


def export_to_json(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename=investors.json'

    data = [user_to_dict(obj) for obj in queryset]
    response.write(json.dumps(data))

    return response

def export_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=investors.csv'

    writer = csv.writer(response)
    writer.writerow(['id', 'username', 'investments'])

    for user in queryset:
        investments = ', '.join(str(investment.id) for investment in user.investment_set.all())
        writer.writerow([user.id, user.username, investments])

    return response
