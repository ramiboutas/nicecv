$((function(){$(document).on("drop dragover",(function(e){e.preventDefault()})),$("#fileupload").fileupload({dataType:"html",sequentialUploads:!0,dropZone:$(".drop-zone"),add:function(e,a){var t=$(this),s=t.data("blueimp-fileupload")||t.data("fileupload"),o=$($("#upload-list-item").html()).addClass("upload-uploading"),l=s.options;$("#upload-list").append(o),a.context=o,a.process((function(){return t.fileupload("process",a)})).always((function(){a.context.removeClass("processing"),a.context.find(".left").each((function(e,t){$(t).append(escapeHtml(a.files[e].name))}))})).done((function(){a.context.find(".start").prop("disabled",!1),!1!==s._trigger("added",e,a)&&(l.autoUpload||a.autoUpload)&&!1!==a.autoUpload&&a.submit()})).fail((function(){a.files.error&&a.context.each((function(e){var t=a.files[e].error;t&&$(this).find(".error_messages").text(t)}))}))},processfail:function(e,a){$(a.context).removeClass("upload-uploading").addClass("upload-failure")},progress:function(e,a){if(e.isDefaultPrevented())return!1;var t=Math.floor(a.loaded/a.total*100);a.context.each((function(){$(this).find(".progress").addClass("active").attr("aria-valuenow",t).find(".bar").css("width",t+"%").html(t+"%")}))},progressall:function(e,a){var t=parseInt(a.loaded/a.total*100,10);$("#overall-progress").addClass("active").attr("aria-valuenow",t).find(".bar").css("width",t+"%").html(t+"%"),t>=100&&$("#overall-progress").removeClass("active").find(".bar").css("width","0%")},formData:function(e){var a=this.files[0].name,t={title:a.replace(/\.[^.]+$/,"")},s=window.fileupload_opts.max_title_length;return e.get(0).dispatchEvent(new CustomEvent("wagtail:documents-upload",{bubbles:!0,cancelable:!0,detail:{data:t,filename:a,maxTitleLength:s}}))?e.serializeArray().concat({name:"title",value:t.title}):e.serializeArray()},done:function(e,a){var t=$(a.context),s=JSON.parse(a.result);s.success?(t.addClass("upload-success"),$(".right",t).append(s.form)):(t.addClass("upload-failure"),$(".right .error_messages",t).append(s.error_message))},fail:function(e,a){$(a.context).addClass("upload-failure")},always:function(e,a){$(a.context).removeClass("upload-uploading").addClass("upload-complete")}}),$("#upload-list").on("submit","form",(function(e){var a=$(this),t=new FormData(this),s=a.closest("#upload-list > li");e.preventDefault(),$.ajax({contentType:!1,data:t,processData:!1,type:"POST",url:this.action}).done((function(e){if(e.success){var t=$(".status-msg.update-success").text();addMessage("success",t),s.slideUp((function(){$(this).remove()}))}else a.replaceWith(e.form),$(".tag_field input",a).tagit(window.tagit_opts)}))})),$("#upload-list").on("click",".delete",(function(e){var a=$(this).closest("form"),t=a.closest("#upload-list > li");e.preventDefault();var s=$('input[name="csrfmiddlewaretoken"]',a).val();$.post(this.href,{csrfmiddlewaretoken:s},(function(e){e.success&&t.slideUp((function(){$(this).remove()}))}))}))}));
