
htmx.onLoad(function (content) {
  var sortables = content.querySelectorAll(".sortable");
  for (var i = 0; i < sortables.length; i++) {
    var sortable = sortables[i];
    new Sortable(sortable, {
      handle: '.handle',
      animation: 150,
      ghostClass: 'blue-background-class',
      // onEnd: function (evt) {
      //   var itemEl = evt.item;  // dragged HTMLElement
      //   evt.to;    // target list
      //   evt.from;  // previous list
      //   evt.oldIndex;  // element's old index within old parent
      //   evt.newIndex;  // element's new index within new parent
      //   evt.oldDraggableIndex; // element's old index within old parent, only counting draggable elements
      //   evt.newDraggableIndex; // element's new index within new parent, only counting draggable elements
      //   evt.clone // the clone element
      //   evt.pullMode;  // when item is in another sortable: `"clone"` if cloning, `true` if moving

      //   let i = 0;

      //   Array.prototype.forEach.call(evt.from.children, child => {
      //     const indexInputElement = child.querySelector("input[name='index']");
      //     console.log(indexInputElement);
      //     //indexInputElement.value = i;
      //     i = i + 1;
      //   });

      // },
    });
  }
})


