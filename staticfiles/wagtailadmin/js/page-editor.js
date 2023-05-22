(()=>{"use strict";var t,e={5062:(t,e,i)=>{var n=i(5311),o=i.n(n),a=i(5447);const r=(t,e=!("true"===t.getAttribute("aria-expanded")))=>{const i=document.querySelector(`#${t.getAttribute("aria-controls")}`);i&&(t.setAttribute("aria-expanded",`${e}`),e?i.removeAttribute("hidden"):"onbeforematch"in document.body?i.setAttribute("hidden","until-found"):i.setAttribute("hidden",""),t.dispatchEvent(new CustomEvent("commentAnchorVisibilityChange",{bubbles:!0})),t.dispatchEvent(new CustomEvent("wagtail:panel-toggle",{bubbles:!0,cancelable:!1,detail:{expanded:e}})))};function s(t){const e=t.closest("[data-panel]"),i=document.querySelector(`#${t.getAttribute("aria-controls")}`);if(!i||!e||e.collapsibleInitialised)return;e.collapsibleInitialised=!0;const n=r.bind(null,t),o=e.classList.contains("collapsed"),a=i.querySelector('[aria-invalid="true"], .error, .w-field--error'),s=o&&!a;s&&n(!1),t.addEventListener("click",n.bind(null,void 0));const l=e.querySelector("[data-panel-heading]");l&&l.addEventListener("click",n.bind(null,void 0)),i.addEventListener("beforematch",n.bind(null,!0)),t.dispatchEvent(new CustomEvent("wagtail:panel-init",{bubbles:!0,cancelable:!1,detail:{expanded:!s}}))}var l=i(4038);class d extends l.p{constructor(t){super(t.formsetPrefix,t),this.formsElt=o()("#"+t.formsetPrefix+"-FORMS");for(let t=0;t<this.formCount;t+=1){const e=this.opts.emptyChildFormPrefix.replace(/__prefix__/g,t);this.initChildControls(e)}this.updateControlStates()}updateControlStates(){this.updateChildCount(),this.updateMoveButtonDisabledStates(),this.updateAddButtonState()}initChildControls(t){const e="inline_child_"+t,i="id_"+t+"-DELETE",n=o()("#"+e),a=n.find("[data-inline-panel-child-move-up]"),r=n.find("[data-inline-panel-child-move-down]");o()("#"+i+"-button").on("click",(()=>{o()("#"+i).val("1"),n.addClass("deleted").slideUp((()=>{this.updateControlStates()}))})),this.opts.canOrder&&(a.on("click",(()=>{const e=n.find(`input[name="${t}-ORDER"]`),i=e.val(),o=n.prevAll(":not(.deleted)").first();if(!o.length)return;const a=o[0].id.replace("inline_child_",""),r=o.find(`input[name="${a}-ORDER"]`),s=r.val();this.animateSwap(n,o),n.insertBefore(o),e.val(s),r.val(i),this.updateControlStates()})),r.on("click",(()=>{const e=n.find(`input[name="${t}-ORDER"]`),i=e.val(),o=n.nextAll(":not(.deleted)").first();if(!o.length)return;const a=o[0].id.replace("inline_child_",""),r=o.find(`input[name="${a}-ORDER"]`),s=r.val();this.animateSwap(n,o),n.insertAfter(o),e.val(s),r.val(i),this.updateControlStates()}))),"1"===o()("#"+i).val()&&(o()("#"+e).addClass("deleted").hide(0,(()=>{this.updateControlStates()})),o()("#"+e).find(".error-message").remove())}updateMoveButtonDisabledStates(){if(this.opts.canOrder){const t=this.formsElt.children(":not(.deleted)");t.each((function(e){const i=0===e,n=e===t.length-1;o()("[data-inline-panel-child-move-up]",this).prop("disabled",i),o()("[data-inline-panel-child-move-down]",this).prop("disabled",n)}))}}updateChildCount(){this.formsElt.children(":not(.deleted)").each((function(t){o()("[data-inline-panel-child-count]",this).first().text(` ${t+1}`)}))}getChildCount(){return o()("> [data-inline-panel-child]",this.formsElt).not(".deleted").length}updateAddButtonState(){if(this.opts.maxForms){const t=o()("#"+this.opts.formsetPrefix+"-ADD");this.getChildCount()>=this.opts.maxForms?t.prop("disabled",!0):t.prop("disabled",!1)}}animateSwap(t,e){const i=this.formsElt,n=i.children(":not(.deleted)");i.css({position:"relative",height:i.height()}),n.each((function(){o()(this).css("top",o()(this).position().top)})).css({position:"absolute",width:"100%"}),t.animate({top:e.position().top},200,(()=>{i.removeAttr("style"),n.removeAttr("style")})),e.animate({top:t.position().top},200,(()=>{i.removeAttr("style"),n.removeAttr("style")}))}addForm(t={}){super.addForm({runCallbacks:!1});const e=this.formCount-1,i=this.opts.emptyChildFormPrefix.replace(/__prefix__/g,e);this.initChildControls(i),this.opts.canOrder&&o()("#id_"+i+"-ORDER").val(e+1),this.updateControlStates(),function(t=document.querySelectorAll("[data-panel-toggle]")){t.forEach(s)}(document.querySelectorAll(`#inline_child_${i} [data-panel-toggle]`)),"runCallbacks"in t&&!t.runCallbacks||(this.opts.onAdd&&this.opts.onAdd(e),this.opts.onInit&&this.opts.onInit(e))}}var c=i(9408);function u(){let t=!1;o()("#id_title").on("focus",(function(){const e=o()("#id_slug").val(),i=(0,a.J)(this.value,!0);t=e===i})),o()("#id_title").on("keyup keydown keypress blur",(function(){if(t){const t=(0,a.J)(this.value,!0);o()("#id_slug").val(t)}}))}function p(){o()("#id_slug").on("blur",(function(){o()(this).val((0,a.J)(o()(this).val(),!1))}))}function h(){const t={};o()(".error-message,.help-critical").each((function(){const e=o()(this).closest('section[role="tabpanel"]');t[e.attr("id")]||(t[e.attr("id")]=0),t[e.attr("id")]=t[e.attr("id")]+1})),Object.entries(t).forEach((([t,e])=>{const i=o()(`[data-tabs] a[href="#${t}"]`).find("[data-tabs-errors]");i.addClass("!w-flex").find("[data-tabs-errors-count]").text(e),i.find("[data-tabs-errors-statement]").text((0,c.qP)("(%(errorCount)s error)","(%(errorCount)s errors)",e).replace("%(errorCount)s",e))}))}function f(){Mousetrap.bind(["mod+p"],(()=>{const t=document.querySelector('[data-side-panel-toggle="preview"]');return t&&t.click(),!1})),Mousetrap.bind(["mod+s"],(()=>(o()(".action-save").trigger("click"),!1)))}window.InlinePanel=d,window.MultipleChooserPanel=class extends d{constructor(t){super(t),this.chooserWidgetFactory=window.telepath.unpack(JSON.parse(document.getElementById(`${t.formsetPrefix}-CHOOSER_WIDGET`).textContent)),document.getElementById(`${t.formsetPrefix}-OPEN_MODAL`).addEventListener("click",(()=>{this.chooserWidgetFactory.openModal((e=>{e.forEach((e=>{if(t.maxForms&&this.getChildCount()>=t.maxForms)return;this.addForm();const i=this.formCount-1,n=`${t.formsetPrefix}-${i}-${t.chooserFieldName}`;this.chooserWidgetFactory.getById(n).setStateFromModalData(e)}))}),{multiple:!0})}))}updateOpenModalButtonState(){if(this.opts.maxForms){const t=document.getElementById(`${this.opts.formsetPrefix}-OPEN_MODAL`);this.getChildCount()>=this.opts.maxForms?(t.setAttribute("disabled","true"),t.setAttribute("data-force-disabled","true")):(t.removeAttribute("disabled"),t.removeAttribute("data-force-disabled"))}}updateControlStates(){super.updateControlStates(),this.updateOpenModalButtonState()}},window.cleanForSlug=a.J,window.initSlugAutoPopulate=u,window.initSlugCleaning=p,window.initErrorDetection=h,window.initKeyboardShortcuts=f,o()((()=>{o()("body").hasClass("page-is-live")||u(),p(),h(),f()}));let m=-1;window.updateFooterSaveWarning=(t,e)=>{const i=o()("[data-unsaved-warning]"),n=i.find("[data-unsaved-type]"),a=t||e,r={all:t&&e,any:a,comments:e&&!t,edits:t&&!e};let s=!1;a?i.removeClass("footer__container--hidden"):(i.hasClass("footer__container--hidden")||(s=!0),i.addClass("footer__container--hidden")),clearTimeout(m);const l=()=>{n.each(((t,e)=>{const i=r[e.dataset.unsavedType];e.hidden=!i}))};s?m=setTimeout(l,1050):l()}},5311:t=>{t.exports=jQuery}},i={};function n(t){var o=i[t];if(void 0!==o)return o.exports;var a=i[t]={exports:{}};return e[t](a,a.exports,n),a.exports}n.m=e,t=[],n.O=(e,i,o,a)=>{if(!i){var r=1/0;for(c=0;c<t.length;c++){for(var[i,o,a]=t[c],s=!0,l=0;l<i.length;l++)(!1&a||r>=a)&&Object.keys(n.O).every((t=>n.O[t](i[l])))?i.splice(l--,1):(s=!1,a<r&&(r=a));if(s){t.splice(c--,1);var d=o();void 0!==d&&(e=d)}}return e}a=a||0;for(var c=t.length;c>0&&t[c-1][2]>a;c--)t[c]=t[c-1];t[c]=[i,o,a]},n.n=t=>{var e=t&&t.__esModule?()=>t.default:()=>t;return n.d(e,{a:e}),e},n.d=(t,e)=>{for(var i in e)n.o(e,i)&&!n.o(t,i)&&Object.defineProperty(t,i,{enumerable:!0,get:e[i]})},n.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(t){if("object"==typeof window)return window}}(),n.o=(t,e)=>Object.prototype.hasOwnProperty.call(t,e),n.r=t=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},n.j=607,(()=>{var t={607:0};n.O.j=e=>0===t[e];var e=(e,i)=>{var o,a,[r,s,l]=i,d=0;if(r.some((e=>0!==t[e]))){for(o in s)n.o(s,o)&&(n.m[o]=s[o]);if(l)var c=l(n)}for(e&&e(i);d<r.length;d++)a=r[d],n.o(t,a)&&t[a]&&t[a][0](),t[a]=0;return n.O(c)},i=globalThis.webpackChunkwagtail=globalThis.webpackChunkwagtail||[];i.forEach(e.bind(null,0)),i.push=e.bind(null,i.push.bind(i))})();var o=n.O(void 0,[751],(()=>n(5062)));o=n.O(o)})();
