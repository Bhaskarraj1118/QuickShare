
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.http import url_has_allowed_host_and_scheme
from .models import Clipboard


@ensure_csrf_cookie
@require_http_methods(["GET", "POST"])
def home(request):
    if request.method == "POST":

        text = request.POST.get("text", "").strip()
        expiry_hours = request.POST.get("expiry_hours", "24")

        if not text:
            return JsonResponse({
                "success": False,
                "error": "Please enter some text."
            }, status=400)

        if len(text) > 100000:
            return JsonResponse({
                "success": False,
                "error": "Text cannot exceed 100,000 characters."
            }, status=400)

        try:
            expiry_hours = int(expiry_hours)

            if expiry_hours not in [1, 24, 168, 0]:
                raise ValueError

        except (ValueError, TypeError):
            return JsonResponse({
                "success": False,
                "error": "Invalid expiry option."
            }, status=400)

        try:
            clipboard = Clipboard.objects.create(
                text=text,
                expiry_hours=expiry_hours
            )

            share_url = request.build_absolute_uri(
                f"/share/{clipboard.share_id}/"
            )

            return JsonResponse({
                "success": True,
                "share_url": share_url
            })

        except Exception:
            return JsonResponse({
                "success": False,
                "error": "Unable to save clipboard. Please try again."
            }, status=500)

    return render(request, "clipboard/home.html")


def share_clipboard(request, share_id):
    clipboard = get_object_or_404(
        Clipboard,
        share_id=share_id
    )

    if clipboard.is_expired():
        return render(
            request,
            "clipboard/expired.html",
            status=410
        )

    return render(
        request,
        "clipboard/share.html",
        {"clipboard": clipboard}
    )
