# from django.shortcuts import render
# from django.http import HttpResponse
# from . import models
# from master_data.models import Company

# # Create your views here.


# def print_payment_invoice(request):
#     if request.method == "GET":
#         payment_id = request.GET.get("payment_id", None)

#         if payment_id:
#             payment_id = int(payment_id)
#             papel_size = request.GET.get("papel_size", "a4")

#             payment_instance = models.Payment.objects.get(pk=payment_id)
#             company_instance = Company.objects.get(pk=1)

#             context = {
#                 "header": payment_instance,
#                 "papel_size": papel_size,
#                 "company": company_instance,
#             }

#             return render(request, "payment_invoice_a4.html", context)

#         return HttpResponse("Este pago no existe.")
