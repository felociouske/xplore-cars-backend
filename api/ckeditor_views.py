# Add this file as api/ckeditor_views.py (or wherever your `api` app keeps views).
#
# WHY THIS EXISTS:
# django_ckeditor_5==0.2.20 has a real bug in its bundled upload_file view.
# It calls PIL's `Image.open(f).verify()` to check the upload is a real image,
# but never resets the file's read pointer afterward. Image.open().verify()
# reads through the entire stream to validate it, leaving the pointer at EOF.
# The same file object is then handed straight to Cloudinary, which reads
# zero actual bytes and correctly rejects it with "Invalid image file" —
# on literally every upload, regardless of the file's real content.
#
# Django's `f.size` attribute is cached separately from stream position,
# which is why size reports correctly (e.g. 250968) even though the actual
# bytes available to read are gone by the time Cloudinary gets the file.
#
# This view is an exact copy of django_ckeditor_5's upload_file, with one
# added line: f.seek(0) directly after image_verify(), before the file is
# saved to storage.

from django import get_version
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from django_ckeditor_5.exceptions import NoImageException
from django_ckeditor_5.forms import UploadFileForm
from django_ckeditor_5.storage_utils import image_verify, handle_uploaded_file

if get_version() >= "4.0":
    from django.utils.translation import gettext_lazy as _
else:
    from django.utils.translation import ugettext_lazy as _


def _check_upload_permission(request):
    """Mirrors django_ckeditor_5.permissions.check_upload_permission's logic."""
    permission = getattr(settings, "CKEDITOR_5_FILE_UPLOAD_PERMISSION", "staff")
    if permission == "staff" and not request.user.is_staff:
        return JsonResponse(
            {"error": {"message": _("You do not have permission to upload files.")}},
            status=403,
        )
    if permission == "authenticated" and not request.user.is_authenticated:
        return JsonResponse(
            {"error": {"message": _("You must be logged in to upload files.")}},
            status=403,
        )
    return None


@require_POST
def upload_file_fixed(request):
    permission_error = _check_upload_permission(request)
    if permission_error:
        return permission_error

    form = UploadFileForm(request.POST, request.FILES)
    allow_all_file_types = getattr(settings, "CKEDITOR_5_ALLOW_ALL_FILE_TYPES", False)

    uploaded_file = request.FILES.get("upload")

    if not allow_all_file_types and uploaded_file is not None:
        try:
            image_verify(uploaded_file)
        except NoImageException as ex:
            return JsonResponse({"error": {"message": f"{ex}"}}, status=400)

        # --- THE ACTUAL FIX ---
        # image_verify() read through the whole stream to validate it.
        # Reset the pointer so the storage backend (Cloudinary) can read
        # the real content instead of an exhausted, empty stream.
        uploaded_file.seek(0)

    if form.is_valid():
        url = handle_uploaded_file(request.FILES["upload"])
        return JsonResponse({"url": url})

    if form.errors.get("upload"):
        return JsonResponse(
            {"error": {"message": form.errors["upload"][0]}},
            status=400,
        )

    return JsonResponse({"error": {"message": _("Invalid form data")}}, status=400)