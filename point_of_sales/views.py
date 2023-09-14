from weasyprint import HTML, Attachment
from django.http import HttpResponse
from django.template.loader import get_template
from . import models

# Create your views here.


def print_invoice(request):
    if request.method == "GET":
        invoice_header_id = request.GET.get("invoice_header_id", None)

        if invoice_header_id:
            invoice_header_id = int(invoice_header_id)
            papel_size = request.GET.get("papel_size", "A4")

            invoice_header_instance = models.InvoiceHeader.objects.get(
                pk=invoice_header_id
            )
            invoice_details_intance = invoice_header_instance.invoice_detail.all()
            payment_instance = invoice_header_instance.payment.filter(status=True)
            company_instance = models.Company.objects.get(pk=1)

            template_path = "invoice.html"

            template = get_template(template_path)

            context = {
                "header": invoice_header_instance,
                "details": invoice_details_intance,
                "payments": payment_instance,
                "papel_size": papel_size,
                "company": company_instance,
            }

            return HttpResponse(template.render(context))

        return HttpResponse("No existe factura.")


def logout(request):
    pass
