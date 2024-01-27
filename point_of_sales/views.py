import io
from django.http import FileResponse, HttpResponse
from reportlab.pdfgen import canvas
from . import models
from django.template.loader import get_template
from weasyprint import HTML


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

            buffer = io.BytesIO()

            pdf = canvas.Canvas(buffer)

            pdf.drawImage(company_instance.logo.path, 25, 750, width=110, height=25)
            pdf.drawString(150, 780, f"{company_instance.name}")

            pdf.showPage()
            pdf.save()

            context = {
                "header": invoice_header_instance,
                "details": invoice_details_intance,
                "payments": payment_instance,
                "papel_size": papel_size,
                "company": company_instance,
            }

            buffer.seek(0)

            response = FileResponse(buffer, as_attachment=True, filename="hello.pdf")
            response["Content-Disposition"] = "inline"
            return response

        return HttpResponse("No existe factura.")


def print_quotation(request):
    if request.method == "GET":
        quotation_header_id = request.GET.get("quotation_header_id", None)

        if quotation_header_id:
            quotation_header_id = int(quotation_header_id)
            papel_size = request.GET.get("papel_size", "A4")

            quotation_header_instance = models.QuotationHeader.objects.get(
                pk=quotation_header_id
            )
            quotation_details_intance = quotation_header_instance.quotation_detail.all()
            company_instance = models.Company.objects.get(pk=1)

            template_path = "quotation.html"

            template = get_template(template_path)

            context = {
                "header": quotation_header_instance,
                "details": quotation_details_intance,
                "papel_size": papel_size,
                "company": company_instance,
            }

            response = HttpResponse(content_type="application/pdf")
            response["Content-Disposition"] = "inline"
            HTML(
                string=template.render(context), base_url=request.build_absolute_uri()
            ).write_pdf(response)

            return response

            # return HttpResponse(template.render(context))

        return HttpResponse("No existe cotizacion.")


def print_invoice_60mm(request):
    if request.method == "GET":
        invoice_header_id = request.GET.get("invoice_header_id", None)

        if invoice_header_id:
            invoice_header_id = int(invoice_header_id)
            papel_size = request.GET.get("papel_size", "60mm")

            invoice_header_instance = models.InvoiceHeader.objects.get(
                pk=invoice_header_id
            )
            invoice_details_intance = invoice_header_instance.invoice_detail.all()
            payment_instance = invoice_header_instance.payment.filter(status=True)
            company_instance = models.Company.objects.get(pk=1)

            template_path = "invoice_60mm.html"

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
