# from django.http import HttpResponse
# from django.contrib.auth.models import User
# from . import models
# from master_data.models import Company
# from django.template.loader import get_template
# from datetime import datetime
# import locale


# def print_invoice(request):
#     if request.method == "GET":
#         invoice_header_id = request.GET.get("invoice_header_id", None)

#         if invoice_header_id:
#             invoice_header_id = int(invoice_header_id)
#             papel_size = request.GET.get("papel_size", "a4")

#             invoice_header_instance = models.InvoiceHeader.objects.get(
#                 pk=invoice_header_id
#             )
#             invoice_details_intance = invoice_header_instance.invoice_detail.all()
#             payment_instance = invoice_header_instance.payment.filter(status=True)
#             company_instance = Company.objects.get(pk=1)

#             template_path = "invoice.html"

#             template = get_template(template_path)

#             context = {
#                 "header": invoice_header_instance,
#                 "details": invoice_details_intance,
#                 "payments": payment_instance,
#                 "papel_size": papel_size,
#                 "company": company_instance,
#             }

#             return HttpResponse(template.render(context))

#         return HttpResponse("No existe factura.")


# def print_invoice_60mm(request):
#     if request.method == "GET":
#         invoice_header_id = request.GET.get("invoice_header_id", None)

#         if invoice_header_id:
#             invoice_header_id = int(invoice_header_id)
#             papel_size = request.GET.get("papel_size", "60mm")

#             invoice_header_instance = models.InvoiceHeader.objects.get(
#                 pk=invoice_header_id
#             )
#             invoice_details_intance = invoice_header_instance.invoice_detail.all()
#             payment_instance = invoice_header_instance.payment.filter(status=True)
#             company_instance = Company.objects.get(pk=1)

#             template_path = "invoice_60mm.html"

#             template = get_template(template_path)

#             context = {
#                 "header": invoice_header_instance,
#                 "details": invoice_details_intance,
#                 "payments": payment_instance,
#                 "papel_size": papel_size,
#                 "company": company_instance,
#             }

#             return HttpResponse(template.render(context))

#         return HttpResponse("No existe factura.")


# def print_quotation(request):
#     if request.method == "GET":
#         quotation_header_id = request.GET.get("quotation_header_id", None)

#         if quotation_header_id:
#             quotation_header_id = int(quotation_header_id)
#             papel_size = request.GET.get("papel_size", "A4")

#             quotation_header_instance = models.QuotationHeader.objects.get(
#                 pk=quotation_header_id
#             )
#             quotation_details_intance = quotation_header_instance.quotation_detail.all()
#             company_instance = Company.objects.get(pk=1)

#             template_path = "quotation.html"

#             template = get_template(template_path)

#             context = {
#                 "header": quotation_header_instance,
#                 "details": quotation_details_intance,
#                 "papel_size": papel_size,
#                 "company": company_instance,
#             }

#             return HttpResponse(template.render(context))

#         return HttpResponse("No existe cotizacion.")


# def print_quotation_60mm(request):
#     if request.method == "GET":
#         quotation_header_id = request.GET.get("quotation_header_id", None)

#         if quotation_header_id:
#             quotation_header_id = int(quotation_header_id)
#             papel_size = request.GET.get("papel_size", "60mm")

#             quotation_header_instance = models.QuotationHeader.objects.get(
#                 pk=quotation_header_id
#             )
#             quotation_details_intance = quotation_header_instance.quotation_detail.all()
#             company_instance = Company.objects.get(pk=1)

#             template_path = "quotation_60mm.html"

#             template = get_template(template_path)

#             context = {
#                 "header": quotation_header_instance,
#                 "details": quotation_details_intance,
#                 "papel_size": papel_size,
#                 "company": company_instance,
#             }

#             return HttpResponse(template.render(context))

#         return HttpResponse("No existe cotizacion.")


# def print_sales_report(request):
#     def amount_per_payment_method(payment, resumen_sales):
#         if payment.payment_method.name in resumen_sales:
#             resumen_sales[payment.payment_method.name] += payment.amount
#         else:
#             resumen_sales[payment.payment_method.name] = payment.amount

#     if request.method == "GET":
#         date_from = request.GET.get("from", None)
#         date_to = request.GET.get("to", None)
#         user_id = request.GET.get("user_id", None)

#         if date_from and date_to and user_id:
#             from_year = int(date_from[0:4])
#             from_month = int(date_from[5:7])
#             from_day = int(date_from[8:10])
#             to_year = int(date_to[0:4])
#             to_month = int(date_to[5:7])
#             to_day = int(date_to[8:10])
#             date_from = datetime(from_year, from_month, from_day).date()
#             date_to = datetime(to_year, to_month, to_day, 23, 59, 59)

#             invoice_header_instances = models.InvoiceHeader.objects.filter(
#                 date_created__range=(date_from, date_to)
#             )
#             company_instance = Company.objects.get(pk=1)
#             user_instance = User.objects.get(pk=user_id)

#             resumen_sales = {}

#             for invoice_header in invoice_header_instances:
#                 for payment in invoice_header.payment.filter(status=True):
#                     amount_per_payment_method(payment, resumen_sales)

#             for key, value in resumen_sales.items():
#                 resumen_sales[key] = locale.currency(value, grouping=True)

#             template_path = "sales_report.html"

#             template = get_template(template_path)

#             context = {
#                 "header": invoice_header_instances,
#                 "company": company_instance,
#                 "user": user_instance,
#                 "amounts": resumen_sales,
#             }

#             return HttpResponse(template.render(context))

#         return HttpResponse(f"Hubo un error.")
