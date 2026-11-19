
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Clipboard


def home(request):
    if request.method == "POST":
        text = request.POST.get("text", "").strip()
        expiry_hours = request.POST.get("expiry_hours", "24")

        if not text:
            return JsonResponse({"error": "Please enter some text."}, status=400)

        try:
            expiry_hours = int(expiry_hours)
            if expiry_hours not in [1, 24, 168, 0]:
                raise ValueError
        except (ValueError, TypeError):
            return JsonResponse({"error": "Invalid expiry option."}, status=400)

        clipboard = Clipboard.objects.create(
            text=text,
            expiry_hours=expiry_hours
        )

        return JsonResponse({
            "success": True,
            "share_url": request.build_absolute_uri(f"/share/{clipboard.share_id}/")
        })

    return render(request, "clipboard/home.html")


def share_clipboard(request, share_id):
    clipboard = get_object_or_404(Clipboard, share_id=share_id)

    if clipboard.is_expired():
        return render(request, "clipboard/expired.html", status=410)

    return render(request, "clipboard/share.html", {"clipboard": clipboard})
