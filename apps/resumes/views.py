# from __future__ import annotations

# from django.shortcuts import render


# # THE FOLLOWING FUNCTIONS WERE COPIED FROM THE PROFILES APP


# @never_cache
# @login_required
# def generate_resumes_view(request, pk):
#     profile = get_object_or_404(Profile, pk=pk, user=request.user)
#     result = create_resume_objects.delay(pk=pk)
#     profile.task_id = result.task_id
#     profile.save()
#     context = {"object": profile}
#     return render(request, "profiles/resume_partials/resume_progress_bar.html", context)


# @never_cache
# @login_required
# def resume_creation_status_view(request, pk, task_id):
#     profile = get_object_or_404(Profile, pk=pk, user=request.user)
#     progress_object = Progress(AsyncResult(profile.task_id))

#     progress = progress_object.get_info().get("progress")
#     percent = progress.get("percent")
#     success = progress_object.get_info().get("success")

#     context = {"progress": progress, "object": profile}

#     if percent == 100 and success:
#         messages.success(request, _("Resumes created successfully"))
#         return render(
#             request, "profiles/resume_partials/view_resumes_button.html", context
#         )

#     if success == False:
#         messages.error(request, _("Unespected error, try again or later"))
#         return render(
#             request, "profiles/resume_partials/generate_resumes_button.html", context
#         )

#     return render(request, "profiles/resume_partials/resume_progress_bar.html", context)


# @login_required
# def resume_file_list_view(request, pk):
#     object = get_object_or_404(Profile, pk=pk, user=request.user)
#     # qs = Resume.objects.filter(profile__user=request.user, profile__pk=pk)
#     context = {"object": object}
#     return render(request, "profiles/resume_list.html", context)


# @login_required
# def download_resume_pdf_view(request, pk_parent, pk):
#     profile = get_object_or_404(Profile, pk=pk_parent, user=request.user)
#     resume = get_object_or_404(Resume, profile=profile, pk=pk)
#     return FileResponse(open(resume.pdf.path, "rb"))


# @login_required
# def download_resume_image_view(request, pk_parent, pk):
#     profile = get_object_or_404(Profile, pk=pk_parent, user=request.user)
#     resume = get_object_or_404(Resume, profile=profile, pk=pk)
#     return FileResponse(open(resume.image.path, "rb"))


# from django_tex.shortcuts import render_to_pdf
# from apps.tex.models import ResumeTemplate


# def generate_resume_testing_view(request, pk):
#     tex_template_id = request.POST.get("tex_template_id")
#     resume_template = ResumeTemplate.objects.get(id=tex_template_id)
#     profile = get_object_or_404(Profile, pk=pk)
#     template_name = resume_template.template_name
#     context = {"object": profile}
#     return render_to_pdf(
#         request,
#         template_name,
#         context,
#         filename=f"{template_name}_test.pdf",
#     )
